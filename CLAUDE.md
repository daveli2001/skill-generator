# CLAUDE.md - skill-generator Operating Manual

This file contains rules and context that must be followed in every session.

---

## CRITICAL WORKFLOW RULES

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

### Rule 3: Update Progress After Each Step
- Update `progress.txt` after completing each step
- Update `LESSONS.md` when encountering and resolving errors
- Update `CLAUDE.md` when errors are caused by rules in this file (requires user approval)

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

