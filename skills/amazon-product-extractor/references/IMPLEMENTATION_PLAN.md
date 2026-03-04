# Implementation Plan (IMPLEMENTATION_PLAN.md)

## Overview

This document defines the step-by-step build sequence for the Amazon Product Extractor skill.

---

## Phase 1: Initialize Structure

### Step 1.1: Create Directory Structure

```bash
cd /home/dave/skill-generator/skills/amazon-product-extractor/
mkdir -p scripts
mkdir -p references
mkdir -p assets
```

**Status:** Already created ✓

---

### Step 1.2: Create .env File

**File:** `.env`

```env
# No environment variables needed
# firecrawl skill manages its own authentication
```

---

### Step 1.3: Create .gitignore

**File:** `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Environment
.env
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Output files
*.xlsx
```

---

### Step 1.4: Create requirements.txt

**File:** `requirements.txt`

```txt
# Amazon Product Extractor Dependencies
openpyxl==3.1.2
python-dateutil>=2.8.2
```

---

## Phase 2: Create Main Script

### Step 2.1: Write scripts/main.py

**NOTE:** The implementation below reflects the FINAL working approach using firecrawl API with extract mode. The original plan used `firecrawl scrape -f markdown` which didn't work with Amazon's anti-bot protection.

**Structure (FINAL IMPLEMENTATION):**

```python
#!/usr/bin/env python3
"""
Amazon Product Extractor v1.0.0
Extract product information from Amazon US URLs using firecrawl API.

HISTORICAL NOTE: Original plan used firecrawl CLI scrape command,
but it failed with Amazon's anti-bot. Solution: Use firecrawl API
v1/scrape with extract format and JSON schema.
"""

import subprocess
import sys
import os
import json
import time
from datetime import datetime
from openpyxl import Workbook

# 27 Field headers
FIELDS = [...]

# JSON Schema for firecrawl extract
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "brand": {"type": "string", "description": "Brand name"},
        "product_name": {"type": "string", "description": "Product title"},
        "asin": {"type": "string", "description": "Amazon ASIN"},
        # ... all 27 fields
    },
    "required": ["brand", "asin"]
}

def scrape_with_firecrawl_api(url, api_key):
    """Use firecrawl API extract endpoint (WORKING SOLUTION)."""
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
    result = subprocess.run(curl_command, capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        response = json.loads(result.stdout)
        if response.get("success"):
            return response["data"]["extract"]
    return None
```

**SEE ALSO:**
- LESSONS.md for complete problem-solving journey
- CLAUDE.md for detailed implementation guide
- scripts/main.py for actual working code

def extract_fields(content):
    """Parse markdown content and extract 27 fields."""
    data = {field: None for field in FIELDS}
    # TODO: Implement field extraction logic
    return data

def save_to_xlsx(products, filename):
    """Save extracted data to XLSX file."""
    wb = Workbook()
    ws = wb.active

    # Headers
    ws.append(FIELDS)

    # Data rows
    for product in products:
        row = [product.get(field, '') for field in FIELDS]
        ws.append(row)

    wb.save(filename)
    return filename

def main():
    """Main entry point."""
    print("Amazon Product Extractor v1.0.0")
    print("=" * 40)

    # Parse URLs from arguments
    # Extract each URL
    # Save to XLSX
    # Display summary

if __name__ == "__main__":
    main()
```

---

### Step 2.2: Implement Field Extraction Logic

**Parsing rules for each field:**

```python
def extract_field(content, field_name, patterns):
    """Extract a specific field using regex patterns."""
    import re
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "N/A"

# Example patterns
BRAND_PATTERNS = [
    r'Brand:\s*([^\n]+)',
    r'brand["\s:]+([A-Za-z0-9\s]+)',
]

ASIN_PATTERNS = [
    r'ASIN:\s*([A-Z0-9]{10})',
    r'/dp/([A-Z0-9]{10})',
]

PRICE_PATTERNS = [
    r'\$([0-9,]+\.?[0-9]*)',
    r'Price:\s*\$?([0-9,]+\.?[0-9]*)',
]
```

---

### Step 2.3: Implement Retry Logic

```python
def scrape_with_retry(url, max_attempts=2):
    """Scrape URL with retry logic."""
    for attempt in range(1, max_attempts + 1):
        content = scrape_with_firecrawl(url)
        if content:
            return content

        if attempt < max_attempts:
            print(f"⚠ Extraction failed (attempt {attempt}/{max_attempts})")
            print("  Retrying in 2 seconds...")
            time.sleep(2)

    return None
```

---

### Step 2.4: Implement URL Validation

```python
from urllib.parse import urlparse

def is_valid_amazon_url(url):
    """Validate URL is Amazon.com (US)."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Check for Amazon.com domain
        if 'amazon.com' in domain:
            return True

        return False
    except:
        return False
```

---

### Step 2.5: Implement Main Flow

```python
def process_urls(urls):
    """Process list of URLs."""
    products = []
    failed = []

    for i, url in enumerate(urls, 1):
        print(f"\nProcessing URL {i} of {len(urls)}...")

        if not is_valid_amazon_url(url):
            print(f"✗ Invalid domain: {url}")
            failed.append(url)
            continue

        content = scrape_with_retry(url)
        if content:
            data = extract_fields(content)
            data['_url'] = url
            products.append(data)
            print(f"✓ Extracted: {data.get('Brand', 'Unknown')} - {data.get('Product Name', 'Unknown')[:50]}")
        else:
            print(f"✗ Failed to extract: {url}")
            failed.append(url)

    return products, failed
```

---

## Phase 3: Testing

### Step 3.1: Test Single URL

```bash
cd /home/dave/skill-generator/skills/amazon-product-extractor/
python scripts/main.py https://amazon.com/dp/B08XYZ123
```

**Expected:** XLSX file created with 1 product row

---

### Step 3.2: Test Batch URLs

```bash
python scripts/main.py --urls "https://amazon.com/dp/B08XYZ123,https://amazon.com/dp/B09ABC456"
```

**Expected:** XLSX file created with 2 product rows

---

### Step 3.3: Test Error Handling

```bash
python scripts/main.py https://amazon.co.uk/dp/B08XYZ123
```

**Expected:** Error message about non-US domain

---

### Step 3.4: Test XLSX Output

```bash
python -c "from openpyxl import load_workbook; wb = load_workbook('amazon_products_*.xlsx'); print(wb.active.max_row)"
```

**Expected:** Row count matches number of products

---

## Phase 4: Pre-launch Check

### Step 4.1: Redundancy Check

- Scan all files for duplicate logic
- Verify no conflicting implementations

### Step 4.2: Security Check

- Verify no hardcoded credentials
- Check for path traversal vulnerabilities
- Validate all user inputs

### Step 4.3: Dogfooding Test

- Create a test skill using this skill
- Extract real Amazon products
- Verify output quality

---

## Phase 5: Launch

### Step 5.1: Deploy Skill

```bash
# Move to skills directory
cp -r /home/dave/skill-generator/skills/amazon-product-extractor/ \
      ~/.claude/skills/amazon-product-extractor/
```

### Step 5.2: Create Git Release

```bash
cd /home/dave/skill-generator/skills/amazon-product-extractor/
git init
git add .
git commit -m "Initial release: Amazon Product Extractor v1.0.0"
git tag v1.0.0
```

---

## Implementation Order Summary

| Phase | Step | Description | Status |
|-------|------|-------------|--------|
| 1 | 1.1-1.4 | Directory structure, .env, .gitignore, requirements.txt | Pending |
| 2 | 2.1 | Write main.py skeleton | Pending |
| 2 | 2.2 | Implement field extraction | Pending |
| 2 | 2.3 | Implement retry logic | Pending |
| 2 | 2.4 | Implement URL validation | Pending |
| 2 | 2.5 | Implement main flow | Pending |
| 3 | 3.1-3.4 | Testing | Pending |
| 4 | 4.1-4.3 | Pre-launch checks | Pending |
| 5 | 5.1-5.2 | Deploy and release | Pending |

---

## Next Action

Begin Phase 1: Initialize Structure (Step 1.1-1.4)
