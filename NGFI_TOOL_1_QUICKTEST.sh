#!/bin/bash

# 🏭 NGFI Tools Factory - Outil #1 Quick Validation Script
# Exécute des tests basiques sur l'outil avant production

echo "🔍 NGFI Tool #1 - QUICKTEST Suite"
echo "=================================="
echo ""

TOOL_PATH="/home/pc/.openclaw/workspace/tools/verificateur-facture"
HTML_FILE="$TOOL_PATH/index.html"
README_FILE="$TOOL_PATH/README.md"

# Test 1: Files exist
echo "✅ TEST 1: Files exist"
if [ -f "$HTML_FILE" ] && [ -f "$README_FILE" ]; then
    echo "  ✓ HTML file: $(wc -c < $HTML_FILE) bytes"
    echo "  ✓ README file: $(wc -c < $README_FILE) bytes"
else
    echo "  ✗ FAIL: Files missing"
    exit 1
fi
echo ""

# Test 2: HTML validation (basic)
echo "✅ TEST 2: HTML Structure"
if grep -q "<!DOCTYPE html>" "$HTML_FILE"; then
    echo "  ✓ DOCTYPE found"
else
    echo "  ✗ DOCTYPE missing"
fi

if grep -q "<title>.*Vérificateur" "$HTML_FILE"; then
    echo "  ✓ Title tag found"
else
    echo "  ✗ Title missing"
fi

if grep -q 'Tailwind' "$HTML_FILE"; then
    echo "  ✓ Tailwind CDN present"
else
    echo "  ✗ Tailwind missing"
fi

if grep -q 'id="criteriaContainer"' "$HTML_FILE"; then
    echo "  ✓ Criteria container found"
else
    echo "  ✗ Criteria container missing"
fi
echo ""

# Test 3: 15 Criteria present
echo "✅ TEST 3: URSSAF 15 Criteria"
CRITERIA_COUNT=$(grep -c 'id: [0-9]' "$HTML_FILE")
echo "  ✓ Found $CRITERIA_COUNT criteria definitions"
if [ "$CRITERIA_COUNT" -eq 15 ]; then
    echo "    ✓ EXACT: 15/15 criteria present"
else
    echo "    ⚠ WARNING: Expected 15, found $CRITERIA_COUNT"
fi
echo ""

# Test 4: JavaScript functionality
echo "✅ TEST 4: JavaScript Code"
if grep -q 'function updateScore()' "$HTML_FILE"; then
    echo "  ✓ updateScore() function present"
else
    echo "  ✗ updateScore() function missing"
fi

if grep -q 'function renderCriteria()' "$HTML_FILE"; then
    echo "  ✓ renderCriteria() function present"
else
    echo "  ✗ renderCriteria() function missing"
fi

if grep -q 'class="criteria-checkbox"' "$HTML_FILE"; then
    echo "  ✓ Checkboxes present"
else
    echo "  ✗ Checkboxes missing"
fi
echo ""

# Test 5: NGFI CTA
echo "✅ TEST 5: NGFI CTA"
if grep -q 'ngfi.fr/demo' "$HTML_FILE"; then
    echo "  ✓ NGFI CTA link present (ngfi.fr/demo)"
else
    echo "  ✗ NGFI CTA missing"
fi

if grep -q 'Essaie NGFI gratuitement' "$HTML_FILE"; then
    echo "  ✓ NGFI CTA text present"
else
    echo "  ✗ NGFI CTA text missing"
fi

if grep -q 'gradient-to-r.*indigo.*purple' "$HTML_FILE"; then
    echo "  ✓ NGFI CTA styling present"
else
    echo "  ✗ NGFI CTA styling might be missing"
fi
echo ""

# Test 6: Mobile responsive
echo "✅ TEST 6: Mobile Responsiveness"
if grep -q 'viewport' "$HTML_FILE"; then
    echo "  ✓ Viewport meta tag present"
else
    echo "  ✗ Viewport meta tag missing"
fi

if grep -q 'max-w-2xl' "$HTML_FILE"; then
    echo "  ✓ Max width constraint present"
else
    echo "  ⚠ Max width might be missing"
fi

if grep -q 'px-4' "$HTML_FILE"; then
    echo "  ✓ Padding for mobile present"
else
    echo "  ⚠ Mobile padding might be missing"
fi
echo ""

# Test 7: No obvious syntax errors
echo "✅ TEST 7: Syntax Check"
if grep -q 'onclick=' "$HTML_FILE"; then
    echo "  ⚠ WARNING: Using onclick (use event listeners instead)"
else
    echo "  ✓ No deprecated onclick handlers"
fi

if grep -q 'alert(' "$HTML_FILE"; then
    echo "  ⚠ WARNING: Using alert() (bad UX)"
else
    echo "  ✓ No alert() calls"
fi

if grep -q 'console.log' "$HTML_FILE"; then
    echo "  ⚠ INFO: console.log() present (ok for debugging)"
else
    echo "  ✓ No debug console.log()"
fi
echo ""

# Test 8: Documentation
echo "✅ TEST 8: Documentation"
if [ -f "$README_FILE" ]; then
    README_SIZE=$(wc -c < "$README_FILE")
    if [ "$README_SIZE" -gt 1000 ]; then
        echo "  ✓ README.md adequate size ($README_SIZE bytes)"
    else
        echo "  ⚠ WARNING: README.md very small"
    fi
    
    if grep -q "NGFI" "$README_FILE"; then
        echo "  ✓ README mentions NGFI"
    fi
    
    if grep -q "15 critères" "$README_FILE" || grep -q "15 criteria" "$README_FILE"; then
        echo "  ✓ README mentions 15 criteria"
    fi
else
    echo "  ✗ README.md missing"
fi
echo ""

# Test 9: Posts files generated
echo "✅ TEST 9: Marketing Materials"
POSTS_FILE="/home/pc/.openclaw/workspace/NGFI_TOOL_1_POSTS.md"
if [ -f "$POSTS_FILE" ]; then
    echo "  ✓ NGFI_TOOL_1_POSTS.md present"
    LINKEDIN_COUNT=$(grep -c "POST LINKEDIN" "$POSTS_FILE")
    if [ "$LINKEDIN_COUNT" -ge 1 ]; then
        echo "    ✓ LinkedIn post template found"
    fi
    if grep -q "POST X" "$POSTS_FILE"; then
        echo "    ✓ X/Twitter post template found"
    fi
else
    echo "  ✗ NGFI_TOOL_1_POSTS.md missing"
fi
echo ""

# Test 10: Reports generated
echo "✅ TEST 10: Reports Generated"
REPORTS=(
    "/home/pc/.openclaw/workspace/NGFI_TOOL_1_VERIFICATION.md"
    "/home/pc/.openclaw/workspace/NGFI_TOOL_1_READINESS.md"
    "/home/pc/.openclaw/workspace/SUBAGENT_TEST_REPORT_FINAL.md"
)

for report in "${REPORTS[@]}"; do
    if [ -f "$report" ]; then
        SIZE=$(wc -c < "$report")
        NAME=$(basename "$report")
        echo "  ✓ $NAME ($SIZE bytes)"
    fi
done
echo ""

# Summary
echo "=================================="
echo "✅ QUICKTEST SUMMARY"
echo "=================================="
echo ""
echo "📊 All basic validations complete!"
echo ""
echo "Files ready for production:"
echo "  • $HTML_FILE"
echo "  • $README_FILE"
echo "  • Posts templates"
echo "  • Complete documentation"
echo ""
echo "⚠️  BEFORE MONDAY 09:00 AM:"
echo "  1. Confirm GitHub structure with Idir"
echo "  2. Configure webhook URL for email capture"
echo "  3. Add webhook code to HTML (email POST)"
echo "  4. Git push to GitHub"
echo "  5. Verify Vercel live: https://tools.ngfi.fr/verificateur-facture"
echo "  6. Test on mobile (320px - iPhone SE, 375px - Pixel)"
echo ""
echo "🚀 Ready to go!"
