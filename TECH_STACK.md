# TECH_STACK.md - Technology Stack Specification

## Overview

This document defines the complete technology stack for skill-generator and all skills it creates. All versions are locked to ensure consistency and eliminate dependency ambiguity.

---

## Core Platform

| Technology | Version | Purpose |
|------------|---------|---------|
| **Claude Code** | Latest | Host platform for skill execution |
| **Git** | System default (2.x+) | Version control |
| **Bash** | System default (5.x+) | Script execution |

---

## skill-generator Dependencies

### Required Tools

| Tool | Minimum Version | Purpose |
|------|-----------------|---------|
| Node.js | 18.x | Optional helper scripts |
| Python | 3.9+ | Optional data processing scripts |
| openpyxl | 3.1+ | Excel file reading (if needed) |
| pandas | 2.0+ | Data manipulation (if needed) |

### Optional Packages (for generated skills)

| Package | Version | Use Case |
|---------|---------|----------|
| `requests` | 2.31+ | HTTP API calls in Python scripts |
| `pyyaml` | 6.0+ | YAML parsing for SKILL.md frontmatter |
| `python-dotenv` | 1.0+ | Environment variable management |

---

## Standard Skill Library

These are common dependencies available for skills created by skill-generator. Include only what each skill needs.

### Office Document Manipulation

| Package | Version | Purpose | File Formats |
|---------|---------|---------|--------------|
| `python-docx` | 1.1+ | Create, modify Word documents | .docx |
| `pypdf` | 3.0+ | Read, write, merge PDFs | .pdf |
| `python-pptx` | 0.6+ | Create, modify PowerPoint presentations | .pptx |
| `openpyxl` | 3.1+ | Read, write Excel files | .xlsx, .xlsm |
| `pandas` | 2.0+ | Data manipulation, CSV/Excel processing | .csv, .xlsx |
| `xlrd` | 2.0+ | Read legacy Excel files | .xls |

### Chart Creation

| Package | Version | Purpose | Chart Types |
|---------|---------|---------|-------------|
| `matplotlib` | 3.7+ | Static charts | Bar, line, pie, scatter, area, histogram |
| `plotly` | 5.15+ | Interactive charts | All types + dashboards |
| `seaborn` | 0.12+ | Statistical charts | Heatmaps, distribution plots |

**Supported Chart Types:**
- Combination bar and line charts
- 100% stacked bar charts
- Line charts
- Pie charts
- Radar charts
- Mekko charts
- Area charts
- Scatter plots
- Heatmaps

### Web Extraction

| Package | Version | Purpose | Requirement |
|---------|---------|---------|-------------|
| `firecrawl-py` | Latest | **MANDATORY** - Web scraping via Firecrawl API | Required for all web extraction |

#### Firecrawl Setup (Required Web Extraction Tool)

**Rule:** All skills created by skill-generator MUST use Firecrawl for web extraction. Other methods (requests, BeautifulSoup, etc.) are NOT permitted for web scraping.

**Installation:**
```bash
pip install firecrawl-py
```

**Environment Setup:**
```bash
# Get API key from https://www.firecrawl.dev/app
export FIRECRAWL_API_KEY="your-api-key-here"
```

**Basic Usage:**
```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))

# Scrape a single URL
scrape_result = app.scrape_url(
    url='https://example.com',
    params={'formats': ['markdown', 'html']}
)

# Crawl multiple pages from a domain
crawl_result = app.crawl_url(
    url='https://example.com',
    params={'limit': 10, 'scrapeOptions': {'formats': ['markdown']}}
)
```

**SKILL.md Integration:**
```yaml
---
name: web-extraction-skill
version: 1.0.0
description: Extract content from URLs using Firecrawl
scripts:
  - scripts/extract.py
---
```

---

## Skill Structure Requirements

Every skill created by skill-generator MUST follow this structure:

```
[skill-name]/
├── SKILL.md          # Required: Instructions with YAML frontmatter
├── scripts/          # Optional: Executable code
│   ├── *.py          # Python scripts (3.9+)
│   └── *.sh          # Bash scripts (5.x+)
├── references/       # Optional: Documentation loaded as needed
│   └── *.md          # Markdown documentation
└── assets/           # Optional: Templates, fonts, icons
    └── *             # Any asset files
```

---

## SKILL.md YAML Frontmatter Specification

Every SKILL.md file MUST start with this YAML frontmatter:

```yaml
---
name: [skill-name]
version: 1.0.0
description: [Brief description]
author: [Author name]
date: YYYY-MM-DD
scripts:
  - scripts/[script-name].py
---
```

### Field Requirements

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill identifier (kebab-case) |
| `version` | semver | Yes | Version following semantic versioning |
| `description` | string | Yes | One-line description |
| `author` | string | Yes | Skill creator name |
| `date` | date | Yes | Creation date (YYYY-MM-DD) |
| `scripts` | array | No | List of script files to load |

---

## Script Execution Rules

### Python Scripts
- **Shebang:** `#!/usr/bin/env python3`
- **Encoding:** UTF-8
- **Minimum Version:** Python 3.9
- **Dependencies:** Must be listed in `requirements.txt` if used

### Bash Scripts
- **Shebang:** `#!/bin/bash`
- **Error Handling:** `set -euo pipefail` recommended
- **Minimum Version:** Bash 5.x

---

## Security Requirements

### Mandatory Security Rules

1. **No Hardcoded Secrets**
   - Credentials must use environment variables
   - Use `.env` files (gitignored) for local development

2. **Input Validation**
   - All user inputs must be sanitized
   - Use parameterized commands (no string concatenation for shell commands)

3. **Path Safety**
   - Use absolute paths with `os.path.abspath()` or `realpath`
   - Validate paths are within expected directories

4. **Command Injection Prevention**
   - Never use `eval()` on user input
   - Use `subprocess.run()` with list arguments (Python)
   - Quote all variables in Bash (`"$var"` not `$var`)

---

## Git Configuration

### Required Settings

```bash
# User identity (set per-project)
git config user.name "[name]"
git config user.email "[email]"

# Line endings (cross-platform)
git config core.autocrlf input  # macOS/Linux
git config core.autocrlf true   # Windows

# SSH key type
ssh-keygen -t ed25519
```

### Branch Naming Convention

| Branch Type | Prefix | Example |
|-------------|--------|---------|
| Main branch | `master` or `main` | `master` |
| Feature | `feature/` | `feature/user-auth` |
| Bug fix | `fix/` | `fix/login-error` |
| Documentation | `docs/` | `docs/readme-update` |

---

## File Encoding and Formatting

| File Type | Encoding | Line Endings |
|-----------|----------|--------------|
| Markdown (.md) | UTF-8 | LF (\n) |
| Python (.py) | UTF-8 | LF (\n) |
| Bash (.sh) | UTF-8 | LF (\n) |
| YAML (.yml) | UTF-8 | LF (\n) |

---

## Version Update Policy

- **skill-generator core:** Versions are locked; updates require explicit user approval
- **Generated skills:** Each skill manages its own versioning via SKILL.md frontmatter
- **Security patches:** Apply immediately with user notification

---

## Dependency Management

### For Python Scripts

Create `scripts/requirements.txt` with only the dependencies your skill needs:

**Minimal Template (web extraction only):**
```
firecrawl-py>=1.0.0
python-dotenv==1.0.0
pyyaml==6.0.1
```

**Office Documents Template:**
```
python-docx==1.1.0
pypdf==3.17.0
python-pptx==0.6.23
openpyxl==3.1.2
pandas==2.1.4
```

**Charting Template:**
```
matplotlib==3.8.2
plotly==5.18.0
pandas==2.1.4
```

**Full Template (all features):**
```
# Web extraction (MANDATORY - no fallback)
firecrawl-py>=1.0.0

# Office documents
python-docx==1.1.0
pypdf==3.17.0
python-pptx==0.6.23
openpyxl==3.1.2
pandas==2.1.4

# Charting
matplotlib==3.8.2
plotly==5.18.0

# Utilities
pyyaml==6.0.1
python-dotenv==1.0.0
```
python-dotenv==1.0.0
requests==2.31.0
```

Install with:
```bash
pip install -r scripts/requirements.txt
```

### For Node.js Scripts (if used)

Create `package.json`:
```json
{
  "name": "skill-scripts",
  "version": "1.0.0",
  "dependencies": {
    "yaml": "^2.3.0"
  }
}
```

Install with:
```bash
npm install
```

---

## Prohibited Technologies

The following are NOT allowed in skill-generator or generated skills:

| Technology | Reason |
|------------|--------|
| `eval()` on user input | Security vulnerability |
| Unquoted shell variables | Word splitting risks |
| Hardcoded credentials | Security risk |
| External APIs without user consent | Privacy violation |
| Non-open-source dependencies | Licensing issues |
| `requests`/`BeautifulSoup` for web scraping | Must use Firecrawl skill instead |

---

## Tool Compatibility Matrix

| Tool | macOS | Linux | Windows (WSL) | Windows (Native) |
|------|-------|-------|---------------|------------------|
| Bash | ✅ | ✅ | ✅ (WSL) | ⚠️ (Git Bash only) |
| Python 3.9+ | ✅ | ✅ | ✅ (WSL) | ⚠️ (Path issues) |
| Git | ✅ | ✅ | ✅ (WSL) | ✅ |
| Claude Code | ✅ | ✅ | ✅ (WSL) | ⚠️ (Limited) |

**Recommendation:** Use WSL or macOS/Linux for best compatibility.
