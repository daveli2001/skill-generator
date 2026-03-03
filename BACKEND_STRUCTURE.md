# BACKEND_STRUCTURE.md - Backend Architecture Specification

## Overview

This document defines the backend architecture, data structures, and API contracts for skills created by skill-generator. Since skill-generator creates Claude Code skills (not full-stack applications), this document focuses on:

- Data structures and schemas for skill configurations
- Environment variable management
- File-based data storage patterns
- API integration patterns

---

## Architecture Principles

### Stateless Design

Skills created by skill-generator are **stateless agents** that:
- Read configuration from SKILL.md frontmatter
- Load reference files as needed
- Execute scripts on-demand
- Do not maintain persistent state between invocations

### File-Based Storage

Skills use the local filesystem for:
- Configuration: `SKILL.md` YAML frontmatter
- Reference data: `references/` folder
- Assets: `assets/` folder
- Temporary output: User-specified locations

### API-First Integration

Skills integrate with external services via:
- **Firecrawl API**: Web scraping and content extraction
- **User-provided APIs**: Any REST/GraphQL API
- **CLI tools**: System commands for specialized tasks

---

## Data Structures

### Skill Configuration Schema

Every skill must have a `SKILL.md` file with this YAML frontmatter:

```yaml
---
name: skill-name
version: 1.0.0
description: Brief description of what the skill does
author: Author Name
date: YYYY-MM-DD
scripts:
  - scripts/main.py
  - scripts/helper.sh
references:
  - references/guide.md
  - references/template.docx
assets:
  - assets/logo.png
---
```

**Field Requirements:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill identifier (kebab-case) |
| `version` | semver | Yes | Version following semantic versioning |
| `description` | string | Yes | One-line description |
| `author` | string | Yes | Skill creator name |
| `date` | date | Yes | Creation date (YYYY-MM-DD) |
| `scripts` | array | No | List of script files to load |
| `references` | array | No | Reference files to load |
| `assets` | array | No | Asset files to include |

### Environment Variables Schema

Skills requiring API keys or configuration must use environment variables:

```yaml
# .env file structure (never commit to git)
FIRECRAWL_API_KEY=your-api-key-here
CUSTOM_API_KEY=another-key-if-needed
CONFIG_VALUE=some-configuration
```

**Python Loading Pattern:**
```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
api_key = os.getenv('FIRECRAWL_API_KEY')
custom_key = os.getenv('CUSTOM_API_KEY')
```

**Bash Loading Pattern:**
```bash
#!/bin/bash

# Load .env file
set -a
source .env
set +a

# Access environment variables
echo "$FIRECRAWL_API_KEY"
```

---

## File Structure Standards

### Standard Skill Folder

```
[skill-name]/
├── SKILL.md              # Required: Skill configuration
├── scripts/              # Optional: Executable code
│   ├── main.py           # Main entry point
│   ├── helpers.py        # Helper functions
│   └── utils.sh          # Bash utilities
├── references/           # Optional: Reference documentation
│   ├── guide.md          # Markdown documentation
│   ├── template.docx     # Word templates
│   └── data.csv          # Data files
├── assets/               # Optional: Fonts, logos, templates
│   ├── logo.png
│   └── fonts/
├── .env.example          # Required: Example environment variables
└── .gitignore            # Required: Git ignore rules
```

### .env.example Template

```bash
# API Keys
FIRECRAWL_API_KEY=get-key-from-https://www.firecrawl.dev/app

# Optional: Custom API Keys
# CUSTOM_API_KEY=your-key-here

# Configuration
# OUTPUT_FORMAT=pdf
# OUTPUT_FOLDER=~/output
```

### .gitignore Template

```gitignore
# Environment variables (NEVER commit these)
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Output files (user-specific)
output/
*.pdf
*.docx
*.xlsx
```

---

## API Integration Patterns

### Firecrawl API (Web Scraping)

**Pattern 1: Using Firecrawl Skill (Recommended)**
```python
# The firecrawl skill is loaded via Claude Code's Skill tool
# No Python SDK needed - use CLI directly

import subprocess

def scrape_url(url):
    result = subprocess.run(
        ['firecrawl', 'scrape', '-f', 'markdown', url],
        capture_output=True,
        text=True
    )
    return result.stdout
```

**Pattern 2: Using Firecrawl CLI**
```bash
# Basic scrape
firecrawl scrape -f markdown "https://example.com" -o output.md

# Scrape with multiple formats
firecrawl scrape -f markdown,html,links "https://example.com" -o output.json

# Search the web
firecrawl search "your query" -o search-results.json
```

### REST API Integration

**Python Pattern:**
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    def __init__(self):
        self.api_key = os.getenv('CUSTOM_API_KEY')
        self.base_url = 'https://api.example.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get(self, endpoint, params=None):
        response = requests.get(
            f'{self.base_url}/{endpoint}',
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        response = requests.post(
            f'{self.base_url}/{endpoint}',
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
```

### Error Handling Pattern

```python
import os
from dotenv import load_dotenv

load_dotenv()

def validate_config():
    """Validate required environment variables."""
    required = ['FIRECRAWL_API_KEY']
    missing = [key for key in required if not os.getenv(key)]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Please create a .env file with these variables."
        )

def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls with error handling."""
    try:
        return func(*args, **kwargs)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {'error': 'Authentication failed. Check API key.'}
        elif e.response.status_code == 429:
            return {'error': 'Rate limit exceeded. Try again later.'}
        else:
            return {'error': f'API error: {e.response.status_code}'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Network error: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}
```

---

## Data Validation

### Input Validation Schema

```python
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class SkillConfig:
    """Configuration schema for skills."""
    name: str
    version: str
    description: str
    author: str
    date: str
    scripts: Optional[List[str]] = None
    references: Optional[List[str]] = None
    assets: Optional[List[str]] = None

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.name or not isinstance(self.name, str):
            return False
        if not self.version or not isinstance(self.version, str):
            return False
        # Add more validation as needed
        return True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
```

### YAML Frontmatter Parsing

```python
import yaml

def parse_skill_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from SKILL.md."""
    if not content.startswith('---'):
        raise ValueError("SKILL.md must start with YAML frontmatter")

    # Split frontmatter from content
    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError("Invalid YAML frontmatter format")

    frontmatter = parts[1]
    return yaml.safe_load(frontmatter)
```

---

## Output Generation Patterns

### Document Generation Pattern

```python
from docx import Document
from docx.shared import Inches, Pt

def create_document(title: str, content: list) -> str:
    """Create a Word document with standardized formatting."""
    doc = Document()

    # Title
    doc.add_heading(title, 0)

    # Content sections
    for section in content:
        doc.add_heading(section['heading'], level=1)
        doc.add_paragraph(section['text'])

    # Save
    output_path = f'output/{title.replace(" ", "_")}.docx'
    doc.save(output_path)
    return output_path
```

### PDF Generation Pattern

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(title: str, content: str, output_path: str) -> str:
    """Create a PDF document with standardized formatting."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 24))

    # Content
    for line in content.split('\n'):
        story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)
    return output_path
```

### JSON Output Pattern

```python
import json
from datetime import datetime

def create_json_output(data: dict, filename: str) -> str:
    """Create a JSON output file with metadata."""
    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0.0'
        },
        'data': data
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return filename
```

---

## Security Guidelines

### API Key Management

1. **Never hardcode API keys** in source code
2. **Always use environment variables** via `.env` files
3. **Include `.env.example`** with placeholder values
4. **Add `.env` to `.gitignore`** to prevent accidental commits

### Input Sanitization

```python
import re
import os

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal."""
    # Remove any path components
    filename = os.path.basename(filename)
    # Remove special characters
    filename = re.sub(r'[^\w\-. ]', '', filename)
    return filename

def validate_path(path: str, base_dir: str) -> bool:
    """Validate that path is within base directory."""
    abs_path = os.path.abspath(path)
    abs_base = os.path.abspath(base_dir)
    return abs_path.startswith(abs_base)
```

### Output Validation

```python
def validate_output(data: dict, schema: dict) -> bool:
    """Validate output data against expected schema."""
    for key, value_type in schema.items():
        if key not in data:
            return False
        if not isinstance(data[key], value_type):
            return False
    return True
```

---

## Testing Guidelines

### Unit Test Pattern

```python
import unittest

class TestSkillFunctions(unittest.TestCase):

    def test_parse_frontmatter(self):
        content = """---
name: test-skill
version: 1.0.0
---
Content here"""
        result = parse_skill_frontmatter(content)
        self.assertEqual(result['name'], 'test-skill')
        self.assertEqual(result['version'], '1.0.0')

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename('test.txt'), 'test.txt')
        self.assertEqual(sanitize_filename('../test.txt'), 'test.txt')
        self.assertEqual(sanitize_filename('test?.txt'), 'test.txt')

if __name__ == '__main__':
    unittest.main()
```

---

## Deployment Checklist

Before deploying a skill:

- [ ] SKILL.md frontmatter is complete and valid
- [ ] All scripts have proper shebang (`#!/usr/bin/env python3`)
- [ ] Environment variables are documented in `.env.example`
- [ ] `.env` is in `.gitignore`
- [ ] All API keys are loaded from environment variables
- [ ] Error handling is implemented for all external calls
- [ ] Input validation is in place
- [ ] Output files are sanitized and validated
- [ ] Documentation is complete in `references/`

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| API key not found | Check `.env` file exists and is loaded |
| Permission denied on script | Add execute permission: `chmod +x scripts/*.py` |
| Module not found | Install dependencies: `pip install -r requirements.txt` |
| Firecrawl not working | Verify FIRECRAWL_API_KEY is set correctly |

### Debug Mode

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use logger in code
logger.debug(f"API key present: {bool(os.getenv('FIRECRAWL_API_KEY'))}")
```
