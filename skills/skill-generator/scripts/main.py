#!/usr/bin/env python3
"""
skill-generator - Main Script

A Claude Code skill that helps non-technical users create process agents (skills)
using natural language through iterative conversation.

Usage:
    python3 scripts/main.py [command] [options]

Commands:
    init            Initialize a new skill structure
    progress        Display current progress
    checklist       Display step completion checklist
    git-status      Show git status before commit
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def get_working_directory():
    """Get the skill-generator working directory."""
    return Path("/home/dave/skill-generator")


def get_skills_directory():
    """Get the skills directory."""
    return get_working_directory() / "skills"


def verify_working_directory():
    """Verify we're in the correct working directory."""
    expected = get_working_directory()
    current = Path.cwd()

    if not expected.exists():
        print(f"Error: Expected working directory not found: {expected}")
        return False

    return True


def initialize_skill_structure(skill_name, target_path=None):
    """
    Initialize the base folder structure for a new skill.

    Args:
        skill_name: Name of the skill (kebab-case)
        target_path: Optional custom path. If None, uses skills/[skill-name]/

    Returns:
        Path to the created skill folder
    """
    if target_path:
        skill_dir = Path(target_path) / skill_name
    else:
        skill_dir = get_skills_directory() / skill_name

    # Create directories
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)

    # Create .env with placeholder
    env_content = """# Skill Environment Variables
# Copy this file to .env and fill in your actual values

# Add your API keys below
# Example:
# FIRECRAWL_API_KEY=your-api-key-here
"""
    (skill_dir / ".env").write_text(env_content)

    # Create .gitignore
    gitignore_content = """# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
.venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"""
    (skill_dir / ".gitignore").write_text(gitignore_content)

    return skill_dir


def display_progress(progress_file):
    """
    Display current progress from progress.txt.

    Args:
        progress_file: Path to progress.txt
    """
    if not progress_file.exists():
        print("No progress.txt found. Starting fresh.")
        return

    content = progress_file.read_text()
    print("\n" + "=" * 60)
    print("CURRENT PROGRESS")
    print("=" * 60)
    print(content)
    print("=" * 60)


def display_checklist(step_name, tasks):
    """
    Display step completion checklist.

    Args:
        step_name: Name of the current step
        tasks: List of tuples (task_description, is_completed)
    """
    print("\n" + "=" * 60)
    print(f"  {step_name} - COMPLETION CHECKLIST")
    print("=" * 60)

    completed = sum(1 for _, done in tasks if done)
    total = len(tasks)

    for task, is_done in tasks:
        status = "[x]" if is_done else "[ ]"
        print(f"{status} {task}")

    print("\n" + "=" * 60)
    print(f"  Status: {completed}/{total} tasks completed")
    print("=" * 60)


def get_git_status(repo_path):
    """
    Get git status for the repository.

    Args:
        repo_path: Path to git repository

    Returns:
        String containing git status output
    """
    try:
        result = subprocess.run(
            ["git", "status"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error getting git status: {e}"


def check_git_remote(repo_path):
    """
    Check if git remote is configured.

    Args:
        repo_path: Path to git repository

    Returns:
        Tuple (is_configured, remote_url)
    """
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            # Extract the first remote URL
            lines = result.stdout.strip().split("\n")
            if lines:
                parts = lines[0].split()
                if len(parts) >= 2:
                    return True, parts[1]
        return False, None
    except Exception as e:
        return False, None


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]

    if command == "init":
        skill_name = sys.argv[2] if len(sys.argv) > 2 else "new-skill"
        target_path = sys.argv[3] if len(sys.argv) > 3 else None
        skill_dir = initialize_skill_structure(skill_name, target_path)
        print(f"Initialized skill structure at: {skill_dir}")

    elif command == "progress":
        progress_file = get_working_directory() / "progress.txt"
        display_progress(progress_file)

    elif command == "verify":
        if verify_working_directory():
            print("Working directory verified: OK")
            sys.exit(0)
        else:
            print("Working directory verification: FAILED")
            sys.exit(1)

    elif command == "git-status":
        repo_path = get_working_directory()
        print(get_git_status(repo_path))

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
