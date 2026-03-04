# CLAUDE.md - AI Operation Manual

## Overview

This document contains rules and constraints for the Amazon Product Extractor skill.

---

## Skill Rules

### Rule 1: Use firecrawl API via curl (CRITICAL)

**ALWAYS** use the firecrawl API v1 `/scrape` endpoint with `extract` format for Amazon product pages.

**DO NOT use:**
- firecrawl CLI (`firecrawl scrape ...`) - has interactive auth issues
- firecrawl-py Python library - requires pip install
- requests + BeautifulSoup - won't bypass Amazon anti-bot
- Any other scraping method

**Working Implementation:**
```python
import subprocess
import json
import os

# Load API key from environment
api_key = os.environ.get("FIRECRAWL_API_KEY", "fc-00060b1e6685454d81c19f572ec3f519")

# Define extraction schema for 27 fields
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "brand": {"type": "string", "description": "The brand/manufacturer name"},
        "product_name": {"type": "string", "description": "Full product title"},
        "asin": {"type": "string", "description": "Amazon ASIN (10 chars)"},
        "price": {"type": "string", "description": "Current price"},
        # ... add all 27 fields
    },
    "required": ["brand", "asin"]
}

# Call firecrawl API via curl
def scrape_with_firecrawl_api(url, api_key):
    curl_command = [
        "curl", "-s", "-X", "POST",
        "https://api.firecrawl.dev/v1/scrape",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "url": url,
            "formats": ["extract"],
            "extract": {"schema": EXTRACTION_SCHEMA}
        })
    ]

    result = subprocess.run(
        curl_command,
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode == 0:
        response = json.loads(result.stdout)
        if response.get("success") and "data" in response:
            return response["data"].get("extract", {})

    return None
```

**Why this approach:**
1. firecrawl CLI has interactive auth prompts that break scripts
2. Standard scrape returns only navigation (Amazon anti-bot)
3. Extract mode with schema uses firecrawl's managed infrastructure
4. curl avoids Python library dependencies

**Reference:** See LESSONS.md for complete problem-solving timeline.

---

### Rule 2: API Request Format (CRITICAL)

**DO:**
- Use `formats: ["extract"]` (not "markdown" or "html")
- Include complete JSON schema with all 27 fields
- Set `required` fields in schema for better extraction
- Use timeout of 60 seconds (Amazon pages are large)

**DO NOT:**
- Include `cache: false` parameter - API returns error
- Include any parameters not documented in firecrawl API v1
- Use firecrawl API v2 endpoints (different format)

**Working Request Body:**
```json
{
  "url": "https://www.amazon.com/dp/B0DN6B3Z6Z/",
  "formats": ["extract"],
  "extract": {
    "schema": {
      "type": "object",
      "properties": {
        "brand": {"type": "string"},
        "product_name": {"type": "string"},
        "asin": {"type": "string"},
        "price": {"type": "string"}
      },
      "required": ["brand", "asin"]
    }
  }
}
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "metadata": {...},
    "extract": {
      "brand": "Soundcore",
      "product_name": "AeroClip by Anker",
      "asin": "B0DN6B3Z6Z",
      "price": "$109.99"
    }
  }
}
```

---

### Rule 3: Retry Logic

**ALWAYS** implement retry logic for extraction:
1. First attempt fails → wait 2 seconds, retry
2. Second attempt fails → stop and notify user
3. Log all failures with URL and error message

**Implementation:**
```python
def scrape_with_retry(url, max_attempts=2):
    api_key = os.environ.get("FIRECRAWL_API_KEY")

    for attempt in range(1, max_attempts + 1):
        data = scrape_with_firecrawl_api(url, api_key)
        if data:
            return data

        if attempt < max_attempts:
            print(f"  ⚠ Extraction failed (attempt {attempt}/{max_attempts})")
            print("    Retrying in 2 seconds...")
            time.sleep(2)

    return None
```

---

### Rule 4: Field Mapping

The firecrawl API returns field names that may differ from our target format.

**ALWAYS** map API response fields to our 27 standard fields:

```python
FIELD_MAPPING = {
    "brand": "Brand",
    "product_name": "Product Name",
    "productName": "Product Name",
    "asin": "ASIN",
    "price": "Price",
    # ... complete mapping
}

def normalize_extracted_data(data):
    normalized = {field: None for field in FIELDS}
    for api_key, value in data.items():
        if api_key in FIELD_MAPPING:
            normalized[FIELD_MAPPING[api_key]] = value
    return normalized
```

---

### Rule 5: XLSX Output Format

**ALWAYS** save extracted data to XLSX format:
- Use `openpyxl` library
- File naming: `amazon_products_YYYYMMDD_HHMMSS.xlsx`
- Save to current working directory
- Include all 27 column headers (even if some are empty)

---

### Rule 6: URL Validation

**ALWAYS** validate URLs before processing:
- Must be Amazon.com domain (US only)
- Reject non-US Amazon URLs with clear message
- Support both single URL and batch input

---

### Rule 7: API Key Management

**ALWAYS** load API key from environment:
```python
api_key = os.environ.get("FIRECRAWL_API_KEY", "fc-00060b1e6685454d81c19f572ec3f519")
```

**NEVER** hardcode API keys in source code (use .env file)

---

### Rule 8: Documentation Updates

When problems are solved, update in this order:
1. **LESSONS.md** - Document the problem and solution (detailed timeline)
2. **progress.txt** - Record the completed step
3. **CLAUDE.md** - Add/modify rules if needed (requires approval)

---

## Debugging Checklist

If extraction fails:

1. **Check API key:**
   ```bash
   echo $FIRECRAWL_API_KEY
   ```

2. **Test API directly:**
   ```bash
   curl -X POST https://api.firecrawl.dev/v1/scrape \
     -H "Authorization: Bearer YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"url":"https://amazon.com/dp/B0DN6B3Z6Z/","formats":["extract"],"extract":{"schema":{...}}}'
   ```

3. **Check error response:**
   - `"success":false` → Check API key and request format
   - Timeout → Increase timeout or check network
   - Empty extract → Schema may not match page content

4. **Verify JSON schema:**
   - All field names should be snake_case
   - Include descriptions for better extraction
   - Mark critical fields as required

---

## Testing Checklist

- [ ] Single URL extraction works
- [ ] Batch URL extraction works
- [ ] Invalid URLs are rejected
- [ ] Retry logic functions correctly
- [ ] XLSX output is valid and readable
- [ ] All 27 fields are extracted when available
- [ ] Error messages are clear and helpful

---

## Quick Reference

| Component | Value |
|-----------|-------|
| API Endpoint | `https://api.firecrawl.dev/v1/scrape` |
| Auth Method | Bearer token |
| Extract Format | `formats: ["extract"]` |
| Timeout | 60 seconds |
| Retry | 2 attempts |
| Fields | 27 product specifications |
