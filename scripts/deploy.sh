#!/bin/bash
# Quick deploy script for skill-generator
# Usage: ./deploy.sh

set -e

SKILL_SRC="/home/dave/skill-generator/skills/skill-generator"
SKILL_DST="$HOME/.claude/skills/skill-generator"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  skill-generator Deployment Menu"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Use arrow keys or type a number:"
echo ""
echo "  1) Deploy skill to ~/.claude/skills/skill-generator/"
echo "  2) Test deployed skill"
echo "  3) Create release (git tag, push)"
echo "  4) Show status"
echo "  5) Exit"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

while true; do
    read -p "Select option: " choice
    
    case $choice in
        1)
            echo ""
            echo "→ Deploying skill..."
            mkdir -p "$SKILL_DST"
            cp -r "$SKILL_SRC/." "$SKILL_DST/"
            echo "✓ Deployed to $SKILL_DST"
            echo ""
            ;;
        2)
            echo ""
            echo "→ To test: Start a new Claude Code session and type:"
            echo "   '/skill-generator' or 'Create a new skill'"
            echo ""
            ;;
        3)
            echo ""
            echo "→ Creating release v1.0.0..."
            git tag -a v1.0.0 -m "skill-generator v1.0.0 - Initial release"
            git push origin v1.0.0
            echo "✓ Release created and pushed!"
            echo ""
            ;;
        4)
            echo ""
            echo "📦 Deployment Status:"
            if [ -f "$SKILL_DST/SKILL.md" ]; then
                echo "   Deployed: YES ($SKILL_DST)"
            else
                echo "   Deployed: NO"
            fi
            echo ""
            echo "📝 Recent commits:"
            git log --oneline -5 | sed 's/^/   /'
            echo ""
            ;;
        5)
            echo ""
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option. Try again."
            ;;
    esac
done
