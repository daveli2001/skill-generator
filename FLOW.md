# FLOW.md - User Flow and Navigation Documentation

## Overview

This document describes every feature's flow, triggers, decision points, and outcomes for skill-generator.

---

## Global Flow

```
[Start] → Step 1: Ask → Step 2: Plan → Step 3: Build → Step 4: Pre-launch Check → [Launch]
                                                       ↓
                                              (if issues found)
                                                       ↓
                                              Step 5: Debug → [Back to Step 4]
```

---

## Step 1: Ask Flow

### Trigger
- User initiates skill creation with a natural language description

### Sequence
1. skill-generator acknowledges the request
2. **Create core context files first:**
   - CLAUDE.md (with base rules and skill structure)
   - progress.txt (initialized with Step 1 in progress)
   - LESSONS.md (empty template for future lessons)
3. skill-generator asks the 7 core discovery questions:
   - Who is this for?
   - What is the user's core action?
   - What happens after the action?
   - What data needs to be saved?
   - What data needs to be displayed?
   - What happens on error?
   - What happens on success?
4. skill-generator asks technical clarification questions:
   - Agent framework preferences (default: as defined in CLAUDE.md Skill Structure section)
   - Structure preferences (default: as defined in CLAUDE.md Skill Structure section)
5. User provides answers
6. skill-generator summarizes the requirements
7. **Decision Point:** Does the user confirm Step 1 is complete?
   - **Yes** → Proceed to Step 2
   - **No** → Continue clarifying questions

### Success Outcome
- All discovery questions answered
- User explicitly confirms Step 1 complete

### Error Outcome
- User provides ambiguous answers → skill-generator asks clarifying questions (never assumes)

---

## Step 2: Plan Flow

### Trigger
- User confirms Step 1: Ask is complete

### Sequence

#### 2.1 Git Setup (First Sub-step)
1. skill-generator checks if git repository is already linked:
   ```bash
   git remote -v
   ```
2. **Decision Point:** Is remote already configured?
   - **Yes** → Skip to 2.2
   - **No** → Proceed with git setup:
     1. Ask user for git name and email
     2. Configure git identity
     3. Initialize git (if needed)
     4. Add GitHub remote
     5. Generate SSH key (if not exists)
     6. Display public key for user to add to GitHub
     7. Test SSH connection
     8. Make initial commit and push

#### 2.2 File Creation Loop
For each file in order:
1. PRD.md → 2. FLOW.md → 3. TECH_STACK.md → 4. FRONTEND_GUIDELINES.md → 5. BACKEND_STRUCTURE.md → 6. IMPLEMENTATION_PLAN.md

**Per-file sequence:**
1. skill-generator drafts the file
2. **Decision Point:** User review
   - **Approved** → Commit file, proceed to next
   - **Modification requested** → skill-generator updates file, repeat review
3. Update progress.txt
4. Git commit

### Success Outcome
- All 6 specification files created and approved
- Git repository has all commits

### Error Outcome
- User requests changes → Iterate on file content until approved

---

## Step 3: Build Flow

### Trigger
- All Step 2 files approved and committed

### Sequence
1. skill-generator reads IMPLEMENTATION_PLAN.md
2. For each step in IMPLEMENTATION_PLAN.md:
   1. skill-generator executes the step
   2. **Decision Point:** User review
      - **Approved** → Update progress.txt, proceed to next step
      - **Issue found** → Fix the issue, repeat review
   3. Git commit (after each function module completed)
3. Update LESSONS.md for any errors encountered and resolved
4. Update CLAUDE.md if errors reveal rule gaps (requires user approval)

### Success Outcome
- All implementation steps completed
- Skill is fully built in `~/.claude/skills/[skill-name]/`

### Error Outcome
- Implementation error → Fix and document in LESSONS.md

---

## Step 4: Pre-launch Check Flow

### Trigger
- Step 3: Build is complete

### Sequence

#### 4.1 Redundancy Check
1. skill-generator scans all generated files for duplicate or conflicting logic
2. **Decision Point:** Any redundancy found?
   - **Yes** → skill-generator identifies and proposes resolution
   - **No** → Proceed to 4.2
3. User manually approves Redundancy Check

#### 4.2 Security Check
1. skill-generator scans for vulnerabilities:
   - Command injection risks
   - Path traversal risks
   - Unsafe file operations
   - Credential handling issues
2. **Decision Point:** Any security issues found?
   - **Yes** → skill-generator fixes immediately
   - **No** → Proceed to 4.3
3. User manually approves Security Check

#### 4.3 Output Quality Check
1. skill-generator asks user: "Please provide a real use case for your skill"
2. User provides use case
3. **Hard Rule:** skill-generator MUST load the created skill via command line or skill loading mechanism
   - Example: `claude /path/to/skill` or equivalent skill loading command
   - **Prohibited:** Direct task execution or using other skills to simulate the skill
4. skill-generator runs the use case through the loaded skill
5. User reviews the output/result
6. **Decision Point:** Does user approve the result?
   - **Yes** → Quality check passed, proceed to launch
   - **No** → Activate Step 5: Debug

### Success Outcome
- All three checks passed
- User approves launch

### Error Outcome
- Quality check fails → Step 5: Debug activated

---

## Step 5: Debug Flow

### Trigger
- User reports issues with the skill (during Pre-launch Check or after launch)

### Sequence
1. skill-generator reads context files:
   - CLAUDE.md for rules
   - progress.txt for current status
   - LESSONS.md for relevant patterns
2. skill-generator asks user: "Please describe the error or provide any error messages"
3. User provides error information
4. skill-generator analyzes root cause
5. skill-generator proposes a fix
6. **Decision Point:** User approves fix?
   - **Yes** → Apply fix, update LESSONS.md, return to Step 4
   - **No** → Continue debugging
7. Update LESSONS.md with resolution pattern
8. Update CLAUDE.md if rule changes needed (requires user approval)

### Success Outcome
- Issue resolved
- Skill returns to Step 4 or launches successfully

### Error Outcome
- Issue persists → Continue debugging cycle

---

## Feature Checklist

| Feature | File |
|---------|------|
| PRD.md | Product Requirements |
| FLOW.md | This file - User flows |
| TECH_STACK.md | Technology specifications |
| FRONTEND_GUIDELINES.md | Design system |
| BACKEND_STRUCTURE.md | Data/API structure |
| IMPLEMENTATION_PLAN.md | Build steps |
| CLAUDE.md | AI operation manual |
| progress.txt | Progress tracking |
| LESSONS.md | Learned patterns |

---

## Navigation Summary

| From | To | Condition |
|------|-----|-----------|
| Step 1: Ask | Step 2: Plan | User confirms Step 1 complete |
| Step 2: Plan | Step 3: Build | All files approved |
| Step 3: Build | Step 4: Pre-launch Check | All implementation complete |
| Step 4: Pre-launch Check | Launch | All checks pass |
| Step 4: Pre-launch Check | Step 5: Debug | Quality check fails |
| Step 5: Debug | Step 4: Pre-launch Check | Issue resolved |
