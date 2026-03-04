# Product Requirements Document (PRD)

## Product Overview

**Product Name:** Amazon Product Extractor

**Version:** 1.0.0

**Created:** 2026-03-04

---

## 1. Problem Statement

Co-workers need to extract structured product information from Amazon US product pages efficiently. Manual extraction is time-consuming and error-prone when dealing with multiple products.

---

## 2. Target Users

- **Primary:** All co-workers who need to extract Amazon product data
- **Technical Level:** Non-technical users who can provide Amazon URLs
- **Usage Context:** Market research, competitive analysis, product cataloging

---

## 3. Goals & Objectives

### Primary Goals
1. Extract product information from Amazon US URLs (single or batch)
2. Save all extracted data to a structured XLSX file
3. Handle errors gracefully with retry logic

### Success Metrics
- Successfully extracts all 27 defined fields from Amazon product pages
- Handles both single URL and batch URL inputs
- Produces valid, well-formatted XLSX output
- Provides clear error messages when extraction fails

---

## 4. Functional Requirements

### FR-1: URL Input
- **FR-1.1:** Accept single Amazon US URL as input
- **FR-1.2:** Accept multiple Amazon US URLs (batch mode)
- **FR-1.3:** Validate that URLs are Amazon.com (US) domain

### FR-2: Data Extraction
- **FR-2.1:** Extract all 27 product fields from each URL
- **FR-2.2:** Handle missing fields gracefully (leave blank or mark as "N/A")
- **FR-2.3:** Use Firecrawl for web extraction (per skill-generator rules)

### FR-3: Data Output
- **FR-3.1:** Save extracted data to XLSX format
- **FR-3.2:** Use template structure from cross_table_spec.xlsx
- **FR-3.3:** Save file to current working directory
- **FR-3.4:** Include all 27 columns with proper headers

### FR-4: Error Handling
- **FR-4.1:** Retry failed extractions once
- **FR-4.2:** Stop and notify user if retry fails
- **FR-4.3:** Continue processing remaining URLs in batch mode

### FR-5: User Feedback
- **FR-5.1:** Display progress during extraction
- **FR-5.2:** Show summary of results (successful/failed)
- **FR-5.3:** Indicate output file location

---

## 5. Data Fields (27 Total)

| # | Field Name |
|---|------------|
| 1 | Brand |
| 2 | Product Name |
| 3 | Product Number |
| 4 | ASIN |
| 5 | Date First Available |
| 6 | Price |
| 7 | Currency |
| 8 | Key Scenario |
| 9 | Sensitivity |
| 10 | Audio Driver Type |
| 11 | Audio Driver Size |
| 12 | Frequency Response |
| 13 | Battery Life |
| 14 | Charging Time |
| 15 | Play Time |
| 16 | Bluetooth Version |
| 17 | Bluetooth Range |
| 18 | Earpiece Shape |
| 19 | Material |
| 20 | Control Method |
| 21 | Special Feature |
| 22 | Item Weight |
| 23 | Product Dimensions |
| 24 | Water Resistance Level |
| 25 | Customer Reviews |
| 26 | Best Sellers Rank |
| 27 | Key Selling Points |

---

## 6. Non-Functional Requirements

### NFR-1: Performance
- Process single URL within 30 seconds
- Batch mode: process URLs sequentially with progress indication

### NFR-2: Reliability
- Retry mechanism for transient failures
- Graceful handling of missing data fields

### NFR-3: Security
- No sensitive data storage
- API keys loaded from environment variables only
- No hardcoded credentials

### NFR-4: Compatibility
- Amazon.com (US) marketplace only
- Python 3.x compatible
- Works in Claude Code skill environment

---

## 7. Dependencies

| Dependency | Purpose |
|------------|---------|
| Firecrawl | Web extraction/scraping |
| openpyxl | XLSX file creation |
| Python | Runtime environment |

---

## 8. Out of Scope

- Amazon marketplaces other than US (amazon.co.uk, amazon.de, etc.)
- Real-time price tracking
- Product image extraction
- User authentication or session handling
- Web interface (CLI/Claude Code skill only)

---

## 9. Acceptance Criteria

1. **AC-1:** Skill activates via natural language trigger
2. **AC-2:** Accepts single or multiple Amazon US URLs
3. **AC-3:** Extracts all 27 fields from product pages
4. **AC-4:** Creates valid XLSX file with correct structure
5. **AC-5:** Handles errors with retry logic
6. **AC-6:** Provides clear user feedback on success/failure

---

## 10. Open Questions

None at this time.
