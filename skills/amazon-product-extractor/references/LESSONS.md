# Lessons Learned

## Overview

This document tracks problems encountered and solutions discovered during development of the Amazon Product Extractor skill.

---

## Session: Initial Setup (2026-03-04)

### Lesson 1: Use firecrawl Skill, Not firecrawl-py Library

**Problem:** Initial TECH_STACK.md specified installing `firecrawl-py` Python library via pip.

**User Requirement:** User explicitly stated to use the existing firecrawl **skill** instead of installing any Python library.

**Solution:** Updated TECH_STACK.md to:
- Remove `firecrawl-py` from dependencies
- Use subprocess to call `firecrawl scrape -f markdown <url>` command
- Remove FIRECRAWL_API_KEY environment variable (firecrawl skill manages its own auth)
- Simplify requirements.txt to only `openpyxl` and `python-dateutil`

**Takeaway:** Always check for existing Claude Code skills before adding Python library dependencies. The firecrawl skill is already available and handles authentication internally.

**Code Pattern:**
```python
import subprocess

result = subprocess.run(
    ['firecrawl', 'scrape', '-f', 'markdown', url],
    capture_output=True,
    text=True,
    timeout=30
)
content = result.stdout
```

---

### Lesson 2: Amazon Anti-Scraping Protection - RESOLVED

**Problem:** firecrawl scrape command returns mostly navigation elements from Amazon product pages, not actual product data (price, brand, ratings, etc.). Amazon's anti-bot protection is very aggressive.

**Testing Timeline:**

| Test | Command | Result |
|------|---------|--------|
| 1 | `firecrawl scrape -f markdown <url>` | Only navigation, no product data |
| 2 | `firecrawl scrape --only-main-content -f markdown` | Same issue |
| 3 | `firecrawl scrape --country US -f markdown` | Same issue |
| 4 | `firecrawl scrape -f html` | Same issue |
| 5 | `firecrawl agent <prompt>` | Async job, needs polling |

**Root Cause:** Amazon product pages are heavily JavaScript-rendered and protected. Standard scraping returns navigation/framework but not dynamic product content.

**Solution:** Use firecrawl API v1 `/scrape` endpoint with `extract` format and a JSON schema.

**Implementation:**
- Call API directly via curl (not CLI which has auth issues)
- Use `formats: ["extract"]` with a defined schema
- Schema defines all 27 fields with types and descriptions
- API returns structured JSON with extracted data

**Working Code Pattern:**
```python
import subprocess
import json

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "brand": {"type": "string"},
        "product_name": {"type": "string"},
        "price": {"type": "string"},
        "asin": {"type": "string"},
        # ... all 27 fields
    },
    "required": ["brand", "asin"]
}

def scrape_with_firecrawl_api(url, api_key):
    response = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "https://api.firecrawl.dev/v1/scrape",
         "-H", f"Authorization: Bearer {api_key}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({
             "url": url,
             "formats": ["extract"],
             "extract": {"schema": EXTRACTION_SCHEMA}
         })],
        capture_output=True, text=True, timeout=60
    )
    data = json.loads(response.stdout)
    return data["data"]["extract"] if data.get("success") else None
```

**Test Result:** Successfully extracted all 27 fields from Amazon product page.

**Takeaway:** firecrawl's extract mode with structured schema bypasses Amazon's anti-scraping by using their managed infrastructure.

---

### Lesson 3: firecrawl CLI Authentication Issues

**Problem:** firecrawl CLI prompts for interactive authentication even when `FIRECRAWL_API_KEY` is set as environment variable.

**Testing:**
```bash
# These all failed - CLI prompted for interactive auth:
FIRECRAWL_API_KEY=xxx firecrawl scrape ...
firecrawl scrape -k xxx ...
```

**Root Cause:** firecrawl CLI v1.7.1 stores authentication in `~/.firecrawl/config` and doesn't properly read from environment variables for some commands.

**Solution:** Call firecrawl API directly via curl instead of using the CLI.

**Benefits:**
- No interactive prompts
- Full control over request parameters
- Better error handling
- Faster execution (no CLI overhead)
- Works reliably in scripts

**API Key Management:** Store in .env file, load at runtime in Python.

**Code Pattern:**
```python
# Load API key from environment
api_key = os.environ.get("FIRECRAWL_API_KEY", "default_key")

# Use in curl command
curl_command = [
    "curl", "-s", "-X", "POST",
    "https://api.firecrawl.dev/v1/scrape",
    "-H", f"Authorization: Bearer {api_key}",
    ...
]
```

**Takeaway:** For production scripts, call APIs directly via curl/requests rather than relying on CLI tools that may have interactive auth requirements.

---

### Lesson 4: API Parameter Sensitivity

**Problem:** Initial API calls failed with error:
```
{"success":false,"code":"BAD_REQUEST","error":"Unrecognized key in body..."}
```

**Root Cause:** Added `cache: false` parameter which is not supported in firecrawl API v1.

**Debug Output:**
```json
{"success":false,"code":"BAD_REQUEST","error":"Unrecognized key in body -- please review the v2 API documentation for request body changes","details":[{"code":"unrecognized_keys","keys":["cache"],"path":[],"message":"Unrecognized key: \"cache\""}]}
```

**Solution:** Removed the `cache: false` parameter from request body.

**Working Request:**
```json
{
  "url": "https://amazon.com/dp/...",
  "formats": ["extract"],
  "extract": {
    "schema": {...}
  }
}
```

**Takeaway:** Always test API calls directly with curl before integrating into code. Read error messages carefully - they indicate exactly which parameters are invalid.

---

## Summary: Firecrawl Integration Decision Tree

```
Need to scrape Amazon?
│
├─ Option 1: firecrawl CLI
│  └─ Problem: Interactive auth prompts
│  └─ Verdict: NOT suitable for scripts
│
├─ Option 2: firecrawl-py library
│  └─ Problem: User requested not to install
│  └─ Verdict: Avoid (per user requirement)
│
└─ Option 3: firecrawl API via curl (RECOMMENDED)
   ├─ Use: POST /v1/scrape
   ├─ Format: extract with JSON schema
   ├─ Auth: Bearer token in header
   └─ Verdict: WORKS - use this approach
```

---

## Template for Future Lessons

### Lesson X: [Title]

**Problem:** [Description of the problem]

**Testing:** [What was tried]

**Root Cause:** [Analysis]

**Solution:** [How it was resolved]

**Code Changes:** [Files modified]

**Takeaway:** [What was learned]

---

## Pending Items

None at this time.
