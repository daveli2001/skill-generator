# Technical Stack Document (TECH_STACK.md)

## Overview

This document specifies every package, dependency, and API with exact versions for the Amazon Product Extractor skill.

---

## 1. Core Runtime

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.9+ | Runtime environment |
| pip | 23.0+ | Package manager |

---

## 2. Python Dependencies

### 2.1 Web Extraction

| Method | Purpose |
|--------|---------|
| **firecrawl API** | Structured data extraction via REST API |

**Configuration:**
```python
# Use firecrawl API v1 /scrape endpoint with extract format
# Called via curl subprocess
# API key required for authentication
```

**Why firecrawl API:**
- Per skill-generator Rule 4: Web extraction MUST use Firecrawl
- Extract mode with JSON schema returns structured data
- Bypasses Amazon's anti-scraping via managed infrastructure
- Supports all 27 field extraction in single call
- Invoked via: `curl -X POST https://api.firecrawl.dev/v1/scrape`

**API Key:** Stored in .env file (FIRECRAWL_API_KEY)

---

### 2.2 XLSX File Creation

| Package | Version | Purpose | Installation |
|---------|---------|---------|--------------|
| openpyxl | 3.1.2 | XLSX file creation and manipulation | `pip install openpyxl` |

**Configuration:**
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append(headers)  # 27 field headers
ws.append(data_row)
wb.save(filename)
```

**Why openpyxl:**
- Native XLSX support (not XLS)
- No external dependencies
- Well-maintained and stable
- Compatible with Excel and LibreOffice

---

### 2.3 Utilities

| Package | Version | Purpose | Installation |
|---------|---------|---------|--------------|
| python-dateutil | 2.8.2 | Date parsing and formatting | `pip install python-dateutil` |

---

## 3. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FIRECRAWL_API_KEY` | Yes | None | Firecrawl API authentication key |

### .env Template

```env
# Firecrawl API Configuration
FIRECRAWL_API_KEY=your_api_key_here
```

---

## 4. External APIs

### 4.1 firecrawl API

| Property | Value |
|----------|-------|
| **Provider** | Firecrawl (firecrawl.dev) |
| **Endpoint** | `https://api.firecrawl.dev/v1/scrape` |
| **Method** | POST |
| **Authentication** | Bearer token (API key) |
| **Format** | extract (with JSON schema) |
| **Timeout** | 60 seconds per request |
| **Retry** | 2 attempts max |

**Request Format:**
```json
{
  "url": "https://amazon.com/dp/B08XYZ123",
  "formats": ["extract"],
  "extract": {
    "schema": {
      "type": "object",
      "properties": {
        "brand": {"type": "string"},
        "product_name": {"type": "string"},
        "price": {"type": "string"},
        "asin": {"type": "string"}
      }
    }
  }
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "metadata": {...},
    "extract": {
      "brand": "Sony",
      "product_name": "WH-1000XM5",
      "price": "$349.99",
      "asin": "B08XYZ123"
    }
  }
}
```

**Python Integration:**
```python
import subprocess
import json

def scrape_with_firecrawl(url, api_key):
    result = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "https://api.firecrawl.dev/v1/scrape",
         "-H", f"Authorization: Bearer {api_key}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({...})],
        capture_output=True, text=True, timeout=60
    )
    data = json.loads(result.stdout)
    return data["data"]["extract"] if data.get("success") else None
```

---

## 5. File System Requirements

| Requirement | Specification |
|-------------|---------------|
| Write permissions | Current working directory |
| File encoding | UTF-8 |
| XLSX format | Excel 2007+ (.xlsx) |
| Max file size | < 10 MB (typical usage) |

---

## 6. System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 512 MB | 1 GB |
| Disk Space | 100 MB | 500 MB |
| Network | Broadband | Broadband |
| OS | Linux/macOS/Windows | Any with Python 3.9+ |

---

## 7. Dependency Tree

```
amazon-product-extractor/
├── Python 3.9+
│   ├── openpyxl == 3.1.2
│   │   └── et-xmlfile (auto-installed)
│   └── python-dateutil >= 2.8.2
│       └── six (auto-installed)
└── External Tools
    └── firecrawl skill (Claude Code skill)
```

---

## 8. requirements.txt

```txt
# Amazon Product Extractor Dependencies
# Generated: 2026-03-04

# Core dependencies
openpyxl==3.1.2
python-dateutil>=2.8.2
```

---

## 9. Version Pinning Strategy

| Dependency | Pinning Strategy | Rationale |
|------------|------------------|-----------|
| openpyxl | `==3.1.2` | Exact pin for stable XLSX output |
| python-dateutil | `>=2.8.2` | Allow updates, API is stable |

---

## 10. API Key Management

### Security Requirements

1. **NEVER** hardcode API keys in source code
2. **firecrawl skill** manages its own API keys internally
3. **NEVER** commit sensitive files to git
4. **ALWAYS** include .env in .gitignore

### Implementation

```python
# No API key management needed
# firecrawl skill handles its own authentication
```

---

## 11. Testing Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.0 | Unit testing framework |

---

## 12. Compatibility Matrix

| Python Version | Supported | Notes |
|----------------|-----------|-------|
| 3.9 | ✓ | Minimum supported |
| 3.10 | ✓ | Recommended |
| 3.11 | ✓ | Full support |
| 3.12 | ✓ | Full support |
| 3.8 | ✗ | End of life |
