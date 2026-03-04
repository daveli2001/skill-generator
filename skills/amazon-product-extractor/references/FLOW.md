# Flow Document (FLOW.md)

## Overview

This document describes every feature and navigation path for the Amazon Product Extractor skill.

---

## 1. Skill Activation Flow

### 1.1 Trigger Phrases

The skill activates when user says:
- "Extract Amazon product info from [URL]"
- "Get product specs from this Amazon link"
- "Extract data from Amazon URLs"
- "Save Amazon product data to Excel"
- "Scrape Amazon product page"

### 1.2 Activation Sequence

```
User Input → Parse URLs → Validate Amazon.com domain → Start Extraction
```

---

## 2. Main Feature Flows

### Flow 1: Single URL Extraction

**Step 1:** User provides single Amazon URL

```
User: "Extract info from https://amazon.com/dp/B08XYZ123"
         ↓
Skill: Parse and validate URL
         ↓
Skill: Check if URL is amazon.com domain
         ↓
(Valid) → Proceed to extraction
(Invalid) → Notify user: "Please provide an Amazon.com (US) URL"
```

**Step 2:** Extract product data

```
Skill: Call Firecrawl to scrape product page
         ↓
Skill: Parse HTML for 27 fields
         ↓
(Retry on failure) → Max 2 attempts
         ↓
Success → Store extracted data
Failure → Notify user and stop
```

**Step 3:** Save output

```
Skill: Create XLSX file with headers
         ↓
Skill: Write extracted data to row
         ↓
Skill: Save to current directory
         ↓
Skill: Display file path to user
```

---

### Flow 2: Batch URL Extraction

**Step 1:** User provides multiple URLs

```
User: "Extract from these URLs: [URL1, URL2, URL3]"
         ↓
Skill: Parse all URLs
         ↓
Skill: Validate each URL is amazon.com
         ↓
Skill: Report invalid URLs (if any)
         ↓
Skill: Proceed with valid URLs
```

**Step 2:** Process each URL sequentially

```
For each URL:
    Display progress: "Processing URL X of N"
         ↓
    Extract data (with retry)
         ↓
    Append to data collection
         ↓
    (Success) → Continue to next URL
    (Failure after retry) → Log and continue
```

**Step 3:** Save consolidated output

```
Skill: Create XLSX with all 27 column headers
         ↓
Skill: Write all extracted rows
         ↓
Skill: Display summary:
       - Total URLs processed
       - Successful extractions
       - Failed extractions
       - Output file path
```

---

## 3. Error Handling Flows

### Error Flow 1: Invalid URL Domain

```
User provides non-Amazon.com URL
         ↓
Skill detects non-US domain
         ↓
Notify: "This skill only supports Amazon.com (US) URLs"
         ↓
Stop processing that URL
```

### Error Flow 2: Extraction Failure (First Attempt)

```
Firecrawl extraction fails
         ↓
Increment retry counter (1/2)
         ↓
Wait 2 seconds
         ↓
Retry extraction
```

### Error Flow 3: Extraction Failure (Second Attempt)

```
Firecrawl extraction fails (retry)
         ↓
Increment retry counter (2/2 - max reached)
         ↓
Log failure with URL
         ↓
Notify user: "Failed to extract from [URL] after 2 attempts"
         ↓
Continue to next URL (batch mode) or stop (single URL)
```

### Error Flow 4: XLSX Write Failure

```
XLSX save operation fails
         ↓
Check file permissions
         ↓
Notify user: "Failed to save output file: [error message]"
         ↓
Provide extracted data in alternative format (CSV/JSON)
```

---

## 4. Success Flow

### Single URL Success

```
Extraction complete
         ↓
XLSX file created successfully
         ↓
Display to user:
  ✓ Successfully extracted product data
  ✓ File saved: [filename.xlsx]
  ✓ Location: [current directory path]
  ✓ Fields extracted: 27
```

### Batch URL Success

```
All URLs processed
         ↓
XLSX file created successfully
         ↓
Display to user:
  ✓ Batch extraction complete
  ✓ Processed: X URLs
  ✓ Successful: Y extractions
  ✓ Failed: Z extractions
  ✓ File saved: [filename.xlsx]
  ✓ Location: [current directory path]
```

---

## 5. Navigation Paths

### Path 1: Standard Flow

```
Activate skill → Provide URL(s) → Extract → Save → Complete
```

### Path 2: With Retry

```
Activate skill → Provide URL(s) → Extract (fail) → Retry → Save → Complete
```

### Path 3: Error Recovery

```
Activate skill → Provide URL(s) → Extract (fail) → Retry (fail) →
Notify user → User provides corrected URL → Extract → Save → Complete
```

---

## 6. State Transitions

| State | Trigger | Next State |
|-------|---------|------------|
| Idle | User provides URL | Validating |
| Validating | URL is valid | Extracting |
| Validating | URL is invalid | Error (notify user) |
| Extracting | Extraction succeeds | Saving |
| Extracting | Extraction fails (attempt 1) | Retrying |
| Extracting | Extraction fails (attempt 2) | Error (notify user) |
| Retrying | Extraction succeeds | Saving |
| Retrying | Extraction fails | Error (notify user) |
| Saving | Save succeeds | Complete |
| Saving | Save fails | Error (notify user) |

---

## 7. Progress Indicators

### During Extraction

```
Processing URL 1 of 5...
  ✓ Extracted: Brand, Product Name, ASIN...
  ⏳ Fetching: Price, Reviews...
```

### On Completion

```
Extraction Complete!

Results:
  • URLs Processed: 5
  • Successful: 4
  • Failed: 1

Output: amazon_products_20260304_113045.xlsx
Location: /home/dave/project/
```

---

## 8. User Input Formats

### Single URL

```
"Extract from https://amazon.com/dp/B08XYZ123"
"https://amazon.com/dp/B08XYZ123"
```

### Multiple URLs (Batch)

```
"Extract from these:
https://amazon.com/dp/B08XYZ123
https://amazon.com/dp/B09ABC456
https://amazon.com/dp/B07DEF789"
```

### Comma-separated

```
"Extract from https://amazon.com/dp/B08XYZ123, https://amazon.com/dp/B09ABC456"
```

---

## 9. Output File Naming

**Format:** `amazon_products_YYYYMMDD_HHMMSS.xlsx`

**Examples:**
- `amazon_products_20260304_113045.xlsx`
- `amazon_products_20260304_141522.xlsx`

---

## 10. Data Validation

### Field Validation Rules

| Field | Validation |
|-------|------------|
| ASIN | Must be 10 characters (alphanumeric) |
| Price | Must be numeric (may include decimals) |
| Currency | Must be valid currency code (USD) |
| Customer Reviews | Must be in format "X.X out of 5 stars" |
| Best Sellers Rank | Must include category and rank number |
| All text fields | Strip whitespace, handle null gracefully |
