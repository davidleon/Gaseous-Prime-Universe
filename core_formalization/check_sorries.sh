#!/bin/bash
# Lean Sorry Marker Checker
# Run this to detect all unproven parts of your proof

echo "=== LEAN SORRY MARKER CHECKER ==="
echo ""
echo "Scanning for sorry markers in Lean files..."
echo ""

# Count total
TOTAL_FILES=$(find . -name "*.lean" -exec grep -l "sorry" {} \; 2>/dev/null | wc -l)
TOTAL_SORRIES=$(find . -name "*.lean" -exec grep -c "sorry" {} \; 2>/dev/null | awk '{s+=$1} END {print s}')

echo "📊 SUMMARY:"
echo "  Files with sorry markers: $TOTAL_FILES"
echo "  Total sorry markers: $TOTAL_SORRIES"
echo ""

echo "🔴 TOP 20 FILES WITH MOST SORRY MARKERS:"
find . -name "*.lean" -exec sh -c 'echo "$(grep -c "sorry" "$1") $1"' _ {} \; 2>/dev/null | sort -rn | head -20 | nl
echo ""

echo "🔍 KEY COLLATZ PROOF FILES:"
for file in Gpu/Conjectures/Collatz/OmegaManifoldAttackCorrected.lean \
            Gpu/Core/Universal/OmegaMetricProper.lean \
            Gpu/Core/Universal/OmegaILDACorrected.lean; do
    if [ -f "$file" ]; then
        count=$(grep -c "sorry" "$file" 2>/dev/null)
        echo "  $file: $count sorry markers"
    fi
done
echo ""

echo "⚠️  REMEMBER: Each 'sorry' is an unproven assumption!"
echo "   Use 'set_option linter.sorry true' to enable sorry warnings."