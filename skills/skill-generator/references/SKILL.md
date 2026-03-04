---
name: skill-generator
version: 1.0.0
description: A Claude Code skill that helps non-technical users create process agents (skills) using natural language through iterative conversation
author: Dave Li
date: 2026-03-04
scripts:
  - scripts/main.py
references:
  - references/PRD.md
  - references/FLOW.md
  - references/TECH_STACK.md
  - references/FRONTEND_GUIDELINES.md
  - references/BACKEND_STRUCTURE.md
  - references/IMPLEMENTATION_PLAN.md
  - references/CLAUDE.md
  - references/LESSONS.md
assets:
  - assets/fonts/
  - assets/shokz-logo-long.png
  - assets/shokz-logo-short.png
---

# skill-generator

## Overview

**skill-generator** is a Claude Code skill that helps non-technical users create process agents (skills) using natural language through iterative conversation.

**Tagline:** Turn your domain expertise into actionable AI skills - no coding required.

**Target Users:** Product Managers, Business Analysts, Domain Experts with professional knowledge but no programming experience.

---

## How to Use

Activate this skill by mentioning:
- "Create a new skill"
- "Help me build a Claude Code skill"
- "I want to make a skill for [task]"
- "Generate a skill that does [X]"

---

## The 6-Phase Process (Step 0 + 5 Steps)

skill-generator guides you through 6 sequential phases to create a complete, working skill:

### Step 0: Setup Verification - Dependency Check

**BEFORE any skill creation, complete these steps in order:**

**Step 0.0: Create Core Context Files (MUST BE FIRST)**
- Create CLAUDE.md with base rules and skill structure
- Create progress.txt initialized with Step 0 in progress
- Create LESSONS.md with template for future lessons
- Verify all three files exist before proceeding

**Step 0.1: Verify Core Platform**
- Verify Claude Code is running (host platform)
- Verify Git is installed and configured
- Verify Bash is available for script execution
- Check git identity (name, email) is configured

**Step 0.2: Verify Python Environment**
- Verify Python 3.9+ is installed
- Verify required packages (openpyxl, pandas) if needed
- Verify virtual environment exists or create one
- Test Python script execution

**Step 0.3: Verify Skill-Generator Configuration**
- Verify no hardcoded secrets in skill-generator scripts
- Confirm `.env` is in `.gitignore` (protects generated skills)
- Verify git repository is configured (if using version control)
- **Note:** Each generated skill will have its OWN `.env` file with its API keys

**Approval Required:** All Step 0 checks must pass before proceeding to Step 1.

---

### Step 1: Ask - Requirements Discovery

skill-generator asks structured questions to understand your intended skill:

**Core Questions:**
1. Who is this for? (target user)
2. What is the user's core action? (what problem does it solve)
3. What happens after the action? (workflow continuation)
4. What data needs to be saved? (persistent storage)
5. What data needs to be displayed? (user-visible output)
6. What happens on error? (error handling)
7. What happens on success? (success state)

**Technical Clarifications:**
- Agent framework preferences (default: Anthropic's agent framework)
- Structure preferences (default: SKILL.md + scripts/ + references/ + assets/)

**Output:** Requirements documented in progress.txt

**Approval Required:** You must explicitly confirm Step 1 is complete before proceeding.

---

### Step 2: Plan - Specification Documents

skill-generator creates 9 specification files, one at a time. Each file requires your approval before the next is created:

| File | Purpose |
|------|---------|
| PRD.md | Product requirements: what, for whom, features, success criteria |
| FLOW.md | Every feature and navigation path in plain English |
| TECH_STACK.md | Every package, dependency, API locked to exact versions |
| FRONTEND_GUIDELINES.md | Design system: fonts, colors, spacing, component styles |
| BACKEND_STRUCTURE.md | Data structures, schemas, API contracts |
| IMPLEMENTATION_PLAN.md | Step-by-step build sequence |
| CLAUDE.md | AI operation manual with rules and constraints |
| progress.txt | Tracks completed, in-progress, and upcoming work |
| LESSONS.md | Template for future lessons learned |

**Git Setup:** If not already configured, skill-generator will help you set up git repository with SSH authentication.

**Approval Required:** Each file requires your explicit approval before the next is created.

---

### Step 3: Build - Implementation

**IMPORTANT:** skill-generator MUST follow IMPLEMENTATION_PLAN.md exactly for all steps.

**Step 3.1: Initialize Skill Structure**
- Ask user for the target path where the skill should be created (default: `~/.claude/skills/[skill-name]/` for final deployment, or a working directory during development)
- Create skill folder in user-specified path
- Create subdirectories: scripts/, references/, assets/
- Create .env with placeholder environment variables
- Create .gitignore with standard rules

**Step 3.2: Collect References & Assets**
- Gather documentation, templates, examples from you
- Collect fonts, logos, static files
- Organize materials in appropriate folders

**Step 3.3: Create SKILL.md**
- Write YAML frontmatter (name, version, description, author, date)
- List scripts and reference files
- Define triggers and expected outputs

**Step 3.4: Create Scripts**
- **BEFORE writing any script, MUST read LESSONS.md first** to avoid repeating past mistakes
- Implement main script (scripts/main.py or scripts/main.sh)
- Add helper functions, error handling, input validation

**Step 3.5: Testing**
- Test skill activation (triggers work)
- Test each script individually
- Verify outputs match expectations
- Test error handling

**Approval Required:** Each step requires your explicit approval before proceeding.

---

### Step 4: Pre-launch Check - Quality Assurance

Before launching, skill-generator runs thorough checks:

**4.1 Redundancy Check**
- Scan for duplicate or conflicting logic in generated files
- Resolve any redundancy issues

**4.2 Security Check**
- Scan for vulnerabilities (command injection, path traversal, unsafe file operations)
- Fix any security issues immediately

**4.3 Output Quality Check**
- You provide a real use case for your skill
- skill-generator loads the created skill and runs the use case
- You review the output/result
- If approved → proceed to launch
- If issues found → activate Step 5: Debug

**Approval Required:** You must manually approve Redundancy and Security checkpoints.

---

### Step 5: Launch - Deploy and Release

**5.1 Deploy Skill**
- Move skill folder to `~/.claude/skills/[skill-name]/`
- Verify Claude Code can load the skill
- Test skill in actual usage scenario

**5.2 Create Release**
- Update version in SKILL.md
- Create git tag (v1.0.0)
- Write release notes
- Push to remote repository

**Output:** Deployed, versioned skill accessible in Claude Code

---

## Debug Mode (Step 5: Debug)

If your skill encounters errors after launch:

1. Describe the error or provide error messages
2. skill-generator analyzes root cause using CLAUDE.md, progress.txt, LESSONS.md
3. skill-generator proposes a fix
4. You approve or request changes
5. Fix is applied and documented in LESSONS.md

---

## Output Structure

Every skill created by skill-generator follows this structure:

```
[skill-name]/                  # User-specified path
├── SKILL.md                   # Required: Main skill definition with YAML frontmatter
├── .env                       # Environment variables (API keys, config)
├── .gitignore                 # Git ignore rules
├── scripts/                   # Optional: Executable code (Python, Bash)
│   ├── main.py
│   └── helpers.py
├── references/                # Optional: Reference documentation
│   ├── README.md
│   ├── templates/
│   └── examples/
└── assets/                    # Optional: Fonts, logos, templates
    ├── fonts/
    └── images/
```

**Path Configuration:** The user provides the target path when creating a skill. During development, skills are typically created in a working directory (e.g., `/home/dave/skill-generator/skills/[skill-name]/`), then moved to `~/.claude/skills/[skill-name]/` at deployment time (Step 5.1).

**Note:** No README.md inside skill folders (per Claude Code skill conventions).

---

## Rules and Constraints

### Rule 1: Follow IMPLEMENTATION_PLAN.md Exactly (CRITICAL)
- **ALWAYS** read and follow `IMPLEMENTATION_PLAN.md` for the exact step-by-step process
- **ALWAYS** execute steps in the exact order defined (Step 0 → Step 1 → Step 2 → Step 3 → Step 4 → Step 5)
- **NEVER** skip, reorder, or modify steps without explicit user approval
- **ALWAYS** display checklists and request permission after each step (per Rule 8)
- **Step 0 MUST pass before Step 1 can begin** - verify all dependencies from TECH_STACK.md first
- If IMPLEMENTATION_PLAN.md conflicts with any other guidance, IMPLEMENTATION_PLAN.md takes precedence

### Rule 2: Always Ask for Clarification
- Never make assumptions about user requirements
- If input is ambiguous, ask clarifying questions
- If a file already exists, ask: overwrite, merge, or skip?

### Rule 3: .env Security (CRITICAL)
- NEVER display .env file contents in output
- NEVER commit .env to git
- NEVER include .env in frontend displays
- API keys must be loaded from environment variables, never hardcoded
- Users create their own .env file with their API keys

### Rule 4: Web Extraction Must Use Firecrawl (CRITICAL)
- **ALWAYS** use firecrawl skill or firecrawl CLI for web extraction
- **NEVER** use `requests` + `BeautifulSoup` for web scraping
- **NEVER** use `firecrawl-py` Python SDK - it is PROHIBITED
- **NEVER** use `selenium`, `playwright`, or other scraping libraries
- CLI command: `firecrawl scrape -f markdown <url>`
- When creating skills that need web extraction, instruct users to load the firecrawl skill

**Prohibited Technologies for Web Extraction:**
| Tool | Status | Reason |
|------|--------|--------|
| `firecrawl-py` | PROHIBITED | Use firecrawl skill/CLI instead |
| `requests` + `BeautifulSoup` | PROHIBITED | Unreliable, breaks easily |
| `selenium` | PROHIBITED | Overkill, use firecrawl |
| `playwright` | PROHIBITED | Overkill, use firecrawl |
| `scrapy` | PROHIBITED | Overkill, use firecrawl |

### Rule 5: Documentation Updates
When problems are solved, update in this order BEFORE git commit:
1. LESSONS.md - Document the problem and solution
2. progress.txt - Record the completed step
3. CLAUDE.md - Add/modify rules if needed (requires approval)

### Rule 5b: Read LESSONS.md Before Writing Code (CRITICAL)
- **BEFORE writing any script or code**, ALWAYS read LESSONS.md first
- Review past mistakes and lessons to avoid repeating them
- Apply learned patterns from previous debugging sessions
- If LESSONS.md contains relevant warnings, follow them strictly

### Rule 6: Git Commit Requires Permission
- ALWAYS ask for explicit user permission before committing
- Show what will be committed (git status)
- Show proposed commit message
- Wait for approval before running git commit

### Rule 7: Frontend Follows FRONTEND_GUIDELINES.md
- Use defined design tokens (colors, typography, spacing)
- Apply correct theme support (light/dark)
- Use specified color variants for charts and UI

### Rule 8: Checklist Display + Permission Request
After completing EVERY step, MUST:
1. Print step completion checklist
2. Display all checklist items with status
3. Ask for explicit user permission to proceed
4. Wait for user confirmation

### Rule 9: Dogfooding Requirement (Pre-launch CRITICAL)
- **BEFORE Step 5 (Launch)**, skill-generator MUST be tested by creating at least one complete skill using its own conversational flow
- The test skill must go through all 5 steps (Ask → Plan → Build → Pre-launch → Launch)
- Test skill output must be preserved in a permanent location (NOT /tmp/) for user verification
- User must verify the test skill output before the skill-generator is considered complete

---

## Triggers

This skill activates when you:
- Want to create a new Claude Code skill from scratch
- Need help building a process agent
- Want to codify domain expertise into a reusable skill
- Mention skill creation, skill generation, or agent creation

---

## Expected Outputs

At the end of the process, you receive:
1. **A complete, working skill** in a user-specified path (typically moved to `~/.claude/skills/[skill-name]/` at deployment)
2. **Git repository** with all specification files and commits
3. **Documentation** (9 files: PRD.md through LESSONS.md)
4. **Release** on GitHub with version tag (v1.0.0)

---

## Progress Tracking

All progress is tracked in `progress.txt` with:
- Current step status
- Completed items (marked with [x])
- In-progress items
- Next-up items
- Session notes for context continuity

---

## Lessons Learned

All lessons and patterns discovered during skill creation are documented in `LESSONS.md` for:
- Future reference
- Error resolution patterns
- Rule additions and modifications
- Best practices

---

## Contact & Support

For issues or questions about skill-generator, refer to:
- CLAUDE.md for operating rules
- progress.txt for current status
- LESSONS.md for resolution patterns
