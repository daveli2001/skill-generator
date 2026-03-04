#!/usr/bin/env python3
"""
Amazon Product Extractor v1.0.0
Extract product information from Amazon US URLs using firecrawl API.

================================================================================
FIRECRAWL INTEGRATION NOTES (from LESSONS.md)
================================================================================

PROBLEM SOLVING JOURNEY:
1. User requirement: Use firecrawl skill, NOT firecrawl-py library
2. Initial approach: firecrawl scrape -f markdown (via CLI)
   RESULT: Only navigation data, no product specs (Amazon anti-bot)
3. Tried: --only-main-content, --country US flags
   RESULT: Same issue - navigation only
4. Tried: firecrawl agent mode
   RESULT: Async jobs need polling, complex for simple extraction
5. Tried: firecrawl CLI with API key (-k flag, env var)
   RESULT: Interactive auth prompts break script automation
6. Tried: firecrawl API with cache:false parameter
   RESULT: BAD_REQUEST error - unrecognized parameter
7. FINAL SOLUTION: firecrawl API v1/scrape with extract format + JSON schema
   RESULT: SUCCESS - all 27 fields extracted correctly

WORKING APPROACH:
- Use curl to call https://api.firecrawl.dev/v1/scrape
- Use formats: ["extract"] with JSON schema defining all 27 fields
- API key loaded from environment variable FIRECRAWL_API_KEY
- Timeout: 60 seconds, Retry: 2 attempts

SEE ALSO:
- LESSONS.md: Complete timeline with testing table and decision tree
- CLAUDE.md: Full implementation guide and debugging checklist
================================================================================
"""

import subprocess
import sys
import os
import json
import time
from datetime import datetime
from urllib.parse import urlparse
from openpyxl import Workbook

# 27 Field headers (from cross_table_spec.xlsx)
# These fields match the template in /home/dave/skill-generator/tests/cross_table_spec.xlsx
FIELDS = [
    "Brand",
    "Product Name",
    "Product Number",
    "ASIN",
    "Date First Available",
    "Price",
    "Currency",
    "Key Scenario",
    "Sensitivity",
    "Audio Driver Type",
    "Audio Driver Size",
    "Frequency Response",
    "Battery Life",
    "Charging Time",
    "Play Time",
    "Bluetooth Version",
    "Bluetooth Range",
    "Earpiece Shape",
    "Material",
    "Control Method",
    "Special Feature",
    "Item Weight",
    "Product Dimensions",
    "Water Resistance Level",
    "Customer Reviews",
    "Best Sellers Rank",
    "Key Selling Points",
]

# JSON Schema for firecrawl extract
# This schema is sent to firecrawl API to specify what data to extract
# Each field has a type and description to help the AI understand what to look for
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "brand": {"type": "string", "description": "The brand/manufacturer name"},
        "product_name": {"type": "string", "description": "Full product title"},
        "product_number": {"type": "string", "description": "Model or product number"},
        "asin": {"type": "string", "description": "Amazon ASIN (10 chars)"},
        "date_first_available": {"type": "string", "description": "Date first available"},
        "price": {"type": "string", "description": "Current price"},
        "currency": {"type": "string", "description": "Currency code"},
        "key_scenario": {"type": "string", "description": "Primary use case"},
        "sensitivity": {"type": "string", "description": "Audio sensitivity"},
        "audio_driver_type": {"type": "string", "description": "Driver type"},
        "audio_driver_size": {"type": "string", "description": "Driver size in mm"},
        "frequency_response": {"type": "string", "description": "Frequency range"},
        "battery_life": {"type": "string", "description": "Battery duration"},
        "charging_time": {"type": "string", "description": "Charging duration"},
        "play_time": {"type": "string", "description": "Playback time"},
        "bluetooth_version": {"type": "string", "description": "Bluetooth version"},
        "bluetooth_range": {"type": "string", "description": "Wireless range"},
        "earpiece_shape": {"type": "string", "description": "Form factor"},
        "material": {"type": "string", "description": "Primary materials"},
        "control_method": {"type": "string", "description": "Control type"},
        "special_feature": {"type": "string", "description": "Special features"},
        "item_weight": {"type": "string", "description": "Product weight"},
        "product_dimensions": {"type": "string", "description": "Physical dimensions"},
        "water_resistance_level": {"type": "string", "description": "IPX rating"},
        "customer_reviews": {"type": "string", "description": "Rating and reviews"},
        "best_sellers_rank": {"type": "string", "description": "Sales ranking"},
        "key_selling_points": {"type": "string", "description": "Main selling points"},
    },
    "required": ["brand", "asin"],  # Minimum required fields for valid extraction
}

# Field mapping from API response to our FIELDS
FIELD_MAPPING = {
    "brand": "Brand",
    "product_name": "Product Name",
    "productName": "Product Name",
    "product_number": "Product Number",
    "productNumber": "Product Number",
    "model_number": "Product Number",
    "modelNumber": "Product Number",
    "model": "Product Number",
    "asin": "ASIN",
    "date_first_available": "Date First Available",
    "dateFirstAvailable": "Date First Available",
    "price": "Price",
    "currency": "Currency",
    "key_scenario": "Key Scenario",
    "keyScenario": "Key Scenario",
    "use_case": "Key Scenario",
    "useCase": "Key Scenario",
    "sensitivity": "Sensitivity",
    "audio_driver_type": "Audio Driver Type",
    "audioDriverType": "Audio Driver Type",
    "driver_type": "Audio Driver Type",
    "driverType": "Audio Driver Type",
    "audio_driver_size": "Audio Driver Size",
    "audioDriverSize": "Audio Driver Size",
    "driver_size": "Audio Driver Size",
    "driverSize": "Audio Driver Size",
    "frequency_response": "Frequency Response",
    "frequencyResponse": "Frequency Response",
    "frequency": "Frequency Response",
    "battery_life": "Battery Life",
    "batteryLife": "Battery Life",
    "charging_time": "Charging Time",
    "chargingTime": "Charging Time",
    "play_time": "Play Time",
    "playTime": "Play Time",
    "playback_time": "Play Time",
    "playbackTime": "Play Time",
    "bluetooth_version": "Bluetooth Version",
    "bluetoothVersion": "Bluetooth Version",
    "bluetooth_range": "Bluetooth Range",
    "bluetoothRange": "Bluetooth Range",
    "wireless_range": "Bluetooth Range",
    "wirelessRange": "Bluetooth Range",
    "earpiece_shape": "Earpiece Shape",
    "earpieceShape": "Earpiece Shape",
    "form_factor": "Earpiece Shape",
    "formFactor": "Earpiece Shape",
    "material": "Material",
    "materials": "Material",
    "control_method": "Control Method",
    "controlMethod": "Control Method",
    "controls": "Control Method",
    "special_feature": "Special Feature",
    "specialFeature": "Special Feature",
    "special_features": "Special Feature",
    "specialFeatures": "Special Feature",
    "features": "Special Feature",
    "item_weight": "Item Weight",
    "itemWeight": "Item Weight",
    "weight": "Item Weight",
    "product_dimensions": "Product Dimensions",
    "productDimensions": "Product Dimensions",
    "dimensions": "Product Dimensions",
    "water_resistance_level": "Water Resistance Level",
    "waterResistanceLevel": "Water Resistance Level",
    "water_resistance": "Water Resistance Level",
    "waterResistance": "Water Resistance Level",
    "waterproof": "Water Resistance Level",
    "ip_rating": "Water Resistance Level",
    "ipRating": "Water Resistance Level",
    "customer_reviews": "Customer Reviews",
    "customerReviews": "Customer Reviews",
    "rating": "Customer Reviews",
    "reviews": "Customer Reviews",
    "best_sellers_rank": "Best Sellers Rank",
    "bestSellersRank": "Best Sellers Rank",
    "bsr": "Best Sellers Rank",
    "sales_rank": "Best Sellers Rank",
    "salesRank": "Best Sellers Rank",
    "key_selling_points": "Key Selling Points",
    "keySellingPoints": "Key Selling Points",
    "selling_points": "Key Selling Points",
    "sellingPoints": "Key Selling Points",
    "highlights": "Key Selling Points",
}


def print_header():
    """Print skill header."""
    print("\nAmazon Product Extractor v1.0.0")
    print("=" * 40)


def is_valid_amazon_url(url):
    """Validate URL is Amazon.com (US only)."""
    try:
        parsed = urlparse(url.strip())
        domain = parsed.netloc.lower()

        if domain == "amazon.com" or domain.endswith(".amazon.com"):
            return True
        if "amazon." in domain:
            return False
        return False
    except Exception:
        return False


def scrape_with_firecrawl_api(url, api_key):
    """
    Use firecrawl API extract endpoint to get structured data.

    CRITICAL: This uses the firecrawl API v1/scrape endpoint with extract format.
    DO NOT change to use firecrawl CLI or firecrawl-py library.

    See LESSONS.md for the complete problem-solving journey:
    - firecrawl CLI has interactive auth issues
    - Standard scrape returns only navigation (Amazon anti-bot)
    - Extract mode with JSON schema is the working solution

    API Documentation: https://docs.firecrawl.dev/api-reference/endpoint/scrape

    Args:
        url: Amazon product page URL
        api_key: Firecrawl API key for authentication

    Returns:
        dict: Extracted data with field names matching schema, or None on failure
    """
    try:
        curl_command = [
            "curl", "-s", "-X", "POST",
            "https://api.firecrawl.dev/v1/scrape",
            "-H", "Authorization: Bearer " + api_key,
            "-H", "Content-Type: application/json",
            "-d", json.dumps({
                "url": url,
                "formats": ["extract"],
                "extract": {
                    "schema": EXTRACTION_SCHEMA
                }
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
                extract_data = response["data"].get("extract", {})
                if extract_data:
                    return extract_data

        return None

    except subprocess.TimeoutExpired:
        print("  ⚠ API request timed out")
        return None
    except json.JSONDecodeError:
        print("  ⚠ Invalid JSON response")
        return None
    except Exception as e:
        print(f"  ⚠ Error: {e}")
        return None


def scrape_with_retry(url, max_attempts=2):
    """Scrape URL with retry logic."""
    api_key = os.environ.get("FIRECRAWL_API_KEY", "fc-00060b1e6685454d81c19f572ec3f519")

    for attempt in range(1, max_attempts + 1):
        print(f"  ⏳ Extracting data...")
        data = scrape_with_firecrawl_api(url, api_key)

        if data:
            return data

        if attempt < max_attempts:
            print(f"  ⚠ Extraction failed (attempt {attempt}/{max_attempts})")
            print("    Retrying in 2 seconds...")
            time.sleep(2)

    return None


def normalize_extracted_data(data):
    """Convert API response to our field structure."""
    normalized = {field: None for field in FIELDS}

    if not data:
        return normalized

    # Map extracted data using FIELD_MAPPING
    for api_key, value in data.items():
        if value is None or value == "":
            continue

        # Find matching field
        if api_key in FIELD_MAPPING:
            our_field = FIELD_MAPPING[api_key]
            if our_field in FIELDS:
                normalized[our_field] = str(value)

    # Set currency default if price exists
    if normalized["Price"] and not normalized["Currency"]:
        normalized["Currency"] = "USD"

    return normalized


def save_to_xlsx(products, filename):
    """Save extracted data to XLSX file."""
    wb = Workbook()
    ws = wb.active

    ws.append(FIELDS)

    for product in products:
        row = [product.get(field, "") or "" for field in FIELDS]
        ws.append(row)

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except Exception:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width

    wb.save(filename)
    return filename


def generate_filename():
    """Generate output filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"amazon_products_{timestamp}.xlsx"


def parse_urls_from_args(args):
    """Parse URLs from command line arguments."""
    urls = []

    for arg in args:
        if arg.startswith("--"):
            continue
        if arg.startswith("http://") or arg.startswith("https://"):
            urls.append(arg)
        elif "," in arg:
            for url in arg.split(","):
                url = url.strip()
                if url.startswith("http"):
                    urls.append(url)

    return urls


def process_urls(urls):
    """Process list of URLs."""
    products = []
    failed = []

    for i, url in enumerate(urls, 1):
        print(f"\nProcessing URL {i} of {len(urls)}...")
        print(f"  URL: {url}")

        if not is_valid_amazon_url(url):
            print(f"  ✗ Invalid domain: {url}")
            print("    This skill only supports Amazon.com (US) URLs")
            failed.append(url)
            continue

        data = scrape_with_retry(url)
        if data:
            normalized = normalize_extracted_data(data)
            products.append(normalized)
            brand = normalized.get("Brand") or data.get("brand", "Unknown")
            name = normalized.get("Product Name") or data.get("product_name", "Unknown")
            print(f"  ✓ Extracted: {brand} - {name[:50]}...")
        else:
            print(f"  ✗ Failed to extract: {url}")
            failed.append(url)

    return products, failed


def display_summary(products, failed, filename):
    """Display extraction summary."""
    print("\n" + "=" * 40)
    print("✓ Extraction Complete!")
    print("=" * 40)

    print(f"\nResults:")
    print(f"  • URLs processed: {len(products) + len(failed)}")
    print(f"  • Successful: {len(products)}")
    print(f"  • Failed: {len(failed)}")

    if failed:
        print(f"\nFailed URLs:")
        for url in failed:
            print(f"  ✗ {url}")

    print(f"\nOutput File: {filename}")
    print(f"Location: {os.path.abspath(filename)}")
    print(f"Rows: {len(products)} products × {len(FIELDS)} fields")


def main():
    """Main entry point."""
    print_header()

    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print("\nUsage:")
        print("  python scripts/main.py <url>           - Single URL")
        print("  python scripts/main.py <url1> <url2>   - Multiple URLs")
        print("  python scripts/main.py --file urls.txt - From file")
        print("\nExample:")
        print("  python scripts/main.py https://amazon.com/dp/B08XYZ123")
        sys.exit(0)

    if "--file" in args:
        try:
            file_idx = args.index("--file") + 1
            if file_idx < len(args):
                with open(args[file_idx], "r") as f:
                    urls = [line.strip() for line in f if line.strip().startswith("http")]
                print(f"✓ Loaded {len(urls)} URLs from {args[file_idx]}")
            else:
                print("✗ Error: No file specified after --file")
                sys.exit(1)
        except FileNotFoundError:
            print(f"✗ Error: File not found: {args[file_idx]}")
            sys.exit(1)
    else:
        urls = parse_urls_from_args(args)

    if not urls:
        print("\n✗ Error: No URLs provided")
        print("Use --help for usage information")
        sys.exit(1)

    print(f"\n✓ Found {len(urls)} URL(s) to process")
    print("  Using firecrawl API for structured extraction")

    products, failed = process_urls(urls)

    if not products:
        print("\n✗ Error: No products extracted")
        sys.exit(1)

    filename = generate_filename()
    save_to_xlsx(products, filename)

    display_summary(products, failed, filename)


if __name__ == "__main__":
    main()
