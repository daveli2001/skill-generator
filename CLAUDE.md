# CLAUDE.md - skill-generator Operating Manual

This file contains rules and context that must be followed in every session.

---

## CRITICAL WORKFLOW RULES

### Rule 0: Create Core Files First (Step 1 Start)
**At the beginning of Step 1: Ask, always create these core context files first:**
- `CLAUDE.md` - Base rules and skill structure
- `progress.txt` - Progress tracking initialized to Step 1
- `LESSONS.md` - Template for future lessons

These files provide the foundation for the entire skill creation process.

### Rule 1: Never Skip Steps
**DO NOT jump to Step 2 (Plan) before the user confirms Step 1 (Ask) is complete.**

The workflow MUST be followed in exact order:
1. **Step 1: Ask** → Ask all clarifying questions → **WAIT for user confirmation**
2. **Step 2: Plan** → Create files one by one → **WAIT for user approval before each file**
3. **Step 3: Build** → Code step by step → **WAIT for user approval before each step**
4. **Step 4: Pre-launch Check** → Run thorough checks → **WAIT for user confirmation**
5. **Step 5: Debug** → Only activated when errors occur

### Rule 2: Always Ask for Clarification
- Never make assumptions about user requirements
- If input is ambiguous, ask clarifying questions
- If a file already exists, ask whether to overwrite, merge, or skip

### Rule 3: .env Security (CRITICAL)
- **NEVER** display `.env` file contents to the user or in any output
- **NEVER** commit `.env` to git under any circumstances
- **NEVER** include `.env` in any frontend display or artifact
- **ALWAYS** verify `.env` is in `.gitignore` before any git operations
- API keys must always be loaded from environment variables, never hardcoded
- Instruct users to create their own `.env` file with their API keys

### Rule 4: Web Extraction Must Use Firecrawl Skill/CLI
- **ALWAYS** use the firecrawl skill or firecrawl CLI for web extraction
- **NEVER** attempt to install or use `firecrawl-py` Python SDK
- **NEVER** use `requests` or `BeautifulSoup` for web scraping
- CLI command: `firecrawl scrape -f markdown <url>`
- Ensure FIRECRAWL_API_KEY is set in `.env` before using firecrawl

### Rule 5: Documentation Updates (When Problems Are Solved)

**When you solve a problem, follow this order BEFORE git commit:**

1. **Update LESSONS.md** - Document the problem and solution:
   - Document the trigger, problem, solution, and any rules added
   - Use the lesson template at the end of LESSONS.md
   - Date: YYYY-MM-DD format
   - **NEVER delete or overwrite existing lessons** - always append new lessons after existing ones

2. **Update progress.txt** - Record the completed step:
   - Update current status and date
   - Mark completed items with [x]
   - Update "In Progress" and "Next Up" sections
   - Add session notes for important context

3. **Update CLAUDE.md** - When a problem reveals a need for new/modified rules:
   - Add new rules under "CRITICAL WORKFLOW RULES"
   - Modify existing rules if they caused the issue
   - Requires user approval before committing rule changes

**Order of Operations:**

```
[If problem solved:] Problem Solved → LESSONS.md → progress.txt → CLAUDE.md (if needed) → Git Commit
[If no problem:] Git Commit
```

**Summary:**
- Problem solved → Update files, then git commit
- No problem solved → Git commit directly
- **NEVER delete existing LESSONS.md content without user permission**

---

### Rule 6: Never Delete Existing Content Without Permission

**CRITICAL: When updating documentation files:**

- **LESSONS.md:** NEVER delete or replace existing lessons. Always append new lessons after existing ones.
- **progress.txt:** Update status and add notes, don't remove historical context.
- **CLAUDE.md:** Modify rules only when necessary, preserve existing rules unless they're being replaced.

**If you accidentally delete content:**
1. Acknowledge the mistake immediately
2. Restore the deleted content
3. Document the incident in LESSONS.md

---

## Project Context

**Project Name:** skill-generator
**Purpose:** A Claude Code skill that helps non-technical users create process agents (skills) using natural language through iterative conversation.

**Target Users:** Non-technical users with domain expertise (product managers, business analysts)

**Output Location:** Generated skills are created in `~/.claude/skills/[skill-name]/`

---

## Skill Structure (from new-output-folder-structure.png)

Every skill folder contains:
- `SKILL.md` (required) - Instructions in Markdown with YAML frontmatter
- `scripts/` (optional) - Executable code (Python, Bash, etc.)
- `references/` (optional) - Documentation loaded as needed
- `assets/` (optional) - Templates, fonts, icons used in output

---

## Files to Generate (from instruction.xlsx)

| File | Purpose |
|------|---------|
| PRD.md | Complete spec: what, for whom, features, in/out of scope, user stories, success criteria |
| FLOW.md | Every feature and navigation path in plain English, triggers, sequences, decision points |
| TECH_STACK.md | Every package, dependency, API locked to exact versions |
| FRONTEND_GUIDELINES.md | Design system: fonts, colors, spacing, layout rules, component styles |
| BACKEND_STRUCTURE.md | Database schema, tables, columns, types, relationships, API contracts |
| IMPLEMENTATION_PLAN.md | Step-by-step build sequence |
| CLAUDE.md | AI operation manual with rules, constraints, patterns |
| progress.txt | Tracks completed, in-progress, and upcoming work |
| LESSONS.md | Patterns and rules learned from corrections and debugging |

---

## Session Startup Checklist

At the start of each session:
1. Read `CLAUDE.md` for rules and context
2. Read `progress.txt` for current status
3. Read `LESSONS.md` for relevant lessons
4. Determine which step to continue from

---

## Git Workflow

### Git Repository Check (Always First)
**Before any git operations, always check if the repository is already linked:**
```bash
git remote -v
```
- If origin is already set to the correct GitHub repository, skip linking
- If no remote exists, proceed with setup

### Step 2 Starts with Git Setup
**Always ask user for git identity (name + email) as the first sub-step of Step 2**

### Standard Git Repository Linking Operation (SSH)
When setting up a new repository, follow these steps in order:

1. **Initialize git (if not already done):**
   ```bash
   git init
   ```

2. **Configure git identity:**
   ```bash
   git config user.name "[user's name]"
   git config user.email "[user's email]"
   ```

3. **Add GitHub remote (SSH):**
   ```bash
   git remote add origin git@github.com:[username]/[repository].git
   ```

4. **Generate SSH key (if not exists):**
   ```bash
   ssh-keygen -t ed25519 -C "[user's email]" -f ~/.ssh/id_ed25519 -N ""
   ```

5. **Display public key for user to add to GitHub:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   - Instruct user to add this key to: https://github.com/settings/keys

6. **Test SSH connection:**
   ```bash
   ssh -T git@github.com -o StrictHostKeyChecking=no
   ```
   - Expected: "You've successfully authenticated"

7. **Initial commit and push:**
   ```bash
   git add -A
   git commit -m "Initial commit: [description]"
   git push -u origin master
   ```

### Ongoing Git Operations
- Commit after each function module is created
- Commit after each specification file is approved
- Ask user before pushing to remote (unless already authorized)

