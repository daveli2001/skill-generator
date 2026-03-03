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

   **CRITICAL TECHNICAL REQUIREMENT:**
   - **MUST use `Edit()` tool** to append new lessons after existing content
   - **NEVER use `Write()` tool** - it replaces the entire file and deletes all existing lessons
   - **ALWAYS read LESSONS.md first** to verify all previous lessons are intact
   - **Verify** the file ends with "## Lessons Learned (Future entries...)" before editing

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

**LESSONS.md Editing Checklist (MUST verify before committing):**
- [ ] Read LESSONS.md first to see existing lessons
- [ ] Used `Edit()` NOT `Write()` to add new lesson
- [ ] All previous lessons (1, 2, 3...) are still present
- [ ] New lesson is appended after existing lessons
- [ ] File ends with "## Lessons Learned (Future entries will be added here)"

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

**LESSONS.md Specific Rule:**
- Before editing LESSONS.md, always ask user for permission if the edit would overwrite or replace existing content
- Never use Write() to replace the entire file - always use Edit() to append

---

### Rule 7: Dependency Installation Must Reference TECH_STACK.md

**Before installing any Python package, npm package, or system tool:**

1. **First**, check TECH_STACK.md for the approved dependency and version
2. **If the dependency is listed in TECH_STACK.md**, proceed with installation using the specified version
3. **If the dependency is NOT listed**, ask the user for confirmation before installing:
   - Explain why the dependency is needed
   - Propose the installation command
   - Wait for explicit user approval

**Example:**
```
User needs chart generation → Check TECH_STACK.md → matplotlib==3.8.2 is approved → Install with pip
User needs xyz-package → Not in TECH_STACK.md → Ask user for confirmation first
```

**Never:**
- Install packages without checking TECH_STACK.md first
- Use default pip/npm install without version pinning
- Install system tools without user confirmation

---

### Rule 8: Git Commit Requires User Permission

**Before running any git commit:**

1. **Always ask for explicit user permission** before committing
2. Show the user what will be committed (git status summary)
3. Wait for user confirmation
4. Only proceed with git commit after approval

**Exception:** None - this rule applies to ALL commits

**What to show user before committing:**
- List of files to be committed (git status)
- Proposed commit message
- Any unstaged changes that will NOT be included

**Example flow:**
```
Assistant: "Ready to commit. Here's what will be committed:
  - scripts/create_demo_charts.py (new file)
  - LESSONS.md (modified)
  - progress.txt (modified)

  Proposed commit message: 'Add demo chart generation script'

  Shall I proceed with git commit?"

User: "Yes" or "Proceed"

Assistant: [runs git commit]
```

**Never:**
- Commit without asking
- Assume user approval
- Batch multiple commits without individual approval

---

### Rule 9: Frontend Development Must Follow FRONTEND_GUIDELINES.md

**When creating any frontend content (HTML, CSS, JavaScript, charts, visualizations):**

1. **Always** read and follow FRONTEND_GUIDELINES.md first
2. **Must use** the defined design tokens:
   - Colors (primary, secondary, semantic colors)
   - Typography (fonts, sizes, weights)
   - Spacing (8px grid system)
   - Border radius (0px for sharp corners)
   - Shadows and borders
3. **Must apply** the correct theme support:
   - Light theme (default)
   - Dark theme (`[data-theme="dark"]`)
   - Glassmorphism styles (if applicable)
4. **Must use** the specified color variants:
   - Light colors for large-area fills (bars, areas, pie segments)
   - Normal/darker colors for small-area fills (lines, markers, points)
5. **Must ensure** all badges, cards, and panels use consistent styling:
   - `border-radius: 0px` (sharp corners)
   - Consistent border definitions
   - Proper dark mode color variations

**Example:**
```
Creating HTML page → Read FRONTEND_GUIDELINES.md → Apply design tokens → Use correct colors → Ensure dark mode support
```

**Checklist before finalizing frontend content:**
- [ ] Colors match FRONTEND_GUIDELINES.md palette
- [ ] Typography uses specified fonts and sizes
- [ ] Border radius is 0px (unless specified otherwise)
- [ ] Dark mode styles are included
- [ ] Semantic colors use the defined values
- [ ] Chart colors follow large-area vs small-area guidelines

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

