# Frontend Guidelines (FRONTEND_GUIDELINES.md)

## Overview

This document defines the CLI output format, text styles, and user interface conventions for the Amazon Product Extractor skill.

---

## 1. Design Tokens

### 1.1 Status Indicators

| Symbol | Meaning |
|--------|---------|
| ✓ | Success |
| ✗ | Failure |
| ⏳ | In progress |
| ⚠ | Warning |
| → | Navigation/Next step |

### 1.2 Text Formatting

| Element | Format | Example |
|---------|--------|---------|
| File paths | `[path]` | `[amazon_products_20260304.xlsx]` |
| URLs | `<url>` | `<https://amazon.com/dp/B08XYZ>` |
| Numbers | Bold | **27** fields |
| Status | Emoji + text | ✓ Success |

---

## 2. Output Templates

### 2.1 Skill Activation

```
Amazon Product Extractor v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2.2 URL Validation

**Valid URL:**
```
✓ URL validated: amazon.com/dp/B08XYZ123
```

**Invalid Domain:**
```
✗ Invalid domain: <https://amazon.co.uk/dp/B08XYZ>
  This skill only supports Amazon.com (US) URLs
```

### 2.3 Progress Display

**Single URL:**
```
Extracting product data...
─────────────────────────
⏳ Fetching page content...
✓ Page loaded (1.2s)
⏳ Parsing 27 fields...
✓ Extraction complete
```

**Batch Mode:**
```
Batch Extraction: URL 3 of 5
───────────────────────────
⏳ Processing: <https://amazon.com/dp/B09ABC456>
  ✓ Extracted: Brand, Product Name, ASIN, Price...
  ⏳ Fetching: Reviews, Best Sellers Rank...
```

### 2.4 Retry Display

```
⚠ Extraction failed (attempt 1/2)
  Retrying in 2 seconds...
```

### 2.5 Error Display

```
✗ Extraction failed after 2 attempts
  URL: <https://amazon.com/dp/B08XYZ123>
  Error: Timeout - page content could not be loaded

  Skipping to next URL...
```

### 2.6 Success Summary (Single URL)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Extraction Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Product: Sony WH-1000XM5 Wireless Headphones
ASIN: B08XYZ123
Fields extracted: 27/27

Output File: amazon_products_20260304_113045.xlsx
Location: /home/dave/project/

To open: excel amazon_products_20260304_113045.xlsx
```

### 2.7 Success Summary (Batch Mode)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Batch Extraction Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
  • URLs processed: 5
  • Successful: 4
  • Failed: 1

Output File: amazon_products_20260304_141522.xlsx
Location: /home/dave/project/
Rows: 4 products × 27 fields

Failed URLs:
  ✗ <https://amazon.com/dp/B07INVALID>
```

---

## 3. Input Format Display

### 3.1 Help Message

```
Amazon Product Extractor - Usage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Single URL:
  Extract from https://amazon.com/dp/B08XYZ123

Batch URLs:
  Extract from these URLs:
  https://amazon.com/dp/B08XYZ123
  https://amazon.com/dp/B09ABC456
  https://amazon.com/dp/B07DEF789

From file:
  Extract from file urls.txt

Options:
  --help     Show this message
  --version  Show version number
```

### 3.2 File Input Confirmation

```
Reading URLs from file: urls.txt
✓ Found 10 URLs
✓ Validated 10 Amazon.com URLs
```

---

## 4. Field Display Format

### 4.1 Field Categories

Fields are grouped by category during display:

```
Basic Info:
  • Brand: Sony
  • Product Name: WH-1000XM5
  • ASIN: B08XYZ123
  • Price: $349.99

Technical Specs:
  • Audio Driver Size: 30mm
  • Frequency Response: 4Hz-40kHz
  • Bluetooth Version: 5.2

Customer Data:
  • Customer Reviews: 4.5 out of 5 stars
  • Best Sellers Rank: #12 in Electronics
```

### 4.2 Missing Fields

```
  • Battery Life: N/A
  • Water Resistance: N/A
```

---

## 5. Table Output (Optional Preview)

### 5.1 Console Table Preview

```
┌─────────────┬──────────────────────┬─────────────┬──────────┐
│ Brand       │ Product Name         │ ASIN        │ Price    │
├─────────────┼──────────────────────┼─────────────┼──────────┤
│ Sony        │ WH-1000XM5           │ B08XYZ123   │ $349.99  │
│ Apple       │ AirPods Pro 2        │ B09ABC456   │ $249.00  │
│ Bose        │ QuietComfort Ultra   │ B07DEF789   │ $429.00  │
└─────────────┴──────────────────────┴─────────────┴──────────┘

Full data saved to: amazon_products_20260304_113045.xlsx
```

---

## 6. Color Scheme (Terminal)

| Element | Color |
|---------|-------|
| Success (✓) | Green |
| Error (✗) | Red |
| Warning (⚠) | Yellow |
| Progress (⏳) | Blue |
| Headers | Cyan |
| URLs | Blue (underlined) |
| File paths | Magenta |

---

## 7. Responsive Formatting

### 7.1 Line Width

| Terminal Width | Format |
|----------------|--------|
| < 80 chars | Condensed output |
| ≥ 80 chars | Full table display |

### 7.2 Truncation

Long product names are truncated:
```
Product: Sony WH-1000XM5 Wireless Noise Cancelling...
```

---

## 8. Accessibility

- All status indicated by text + symbol (not symbol only)
- Clear error messages with actionable guidance
- Consistent formatting for screen readers

---

## 9. Output File Format

### 9.1 XLSX Structure

| Row | Content |
|-----|---------|
| 1 | Headers (27 columns) |
| 2-n | Product data rows |

### 9.2 Column Formatting

| Column | Format |
|--------|--------|
| Price | Currency ($X.XX) |
| Date First Available | Date (YYYY-MM-DD) |
| Customer Reviews | Text (X.X out of 5 stars) |
| All text | Left-aligned |
| Numbers | Right-aligned |

---

## 10. Version Display

```
Amazon Product Extractor v1.0.0
Built: 2026-03-04
```
