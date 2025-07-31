#!/bin/bash

echo "🏥 PROJECT HEALTH DASHBOARD"
echo "=========================="
echo "Generated: $(date)"
echo ""

# Task completion rate
total_tasks=$(find ../specs -name "tasks.md" -exec grep -c "^-\s\[" {} \; | awk '{s+=$1} END {print s}')
completed_tasks=$(find ../specs -name "tasks.md" -exec grep -c "^-\s\[x\]" {} \; | awk '{s+=$1} END {print s}')

if [ $total_tasks -gt 0 ]; then
    progress=$((completed_tasks * 100 / total_tasks))
    echo "📊 Task Progress: $completed_tasks/$total_tasks ($progress%)"
else
    echo "📊 No tasks defined yet"
fi

# Documentation completeness
incomplete_features=0
total_features=$(find ../specs -mindepth 1 -maxdepth 1 -type d | grep -v "_template" | wc -l)

for feature in $(find ../specs -mindepth 1 -maxdepth 1 -type d | grep -v "_template"); do
    if [ ! -f "$feature/requirements.md" ] || [ ! -f "$feature/design.md" ] || [ ! -f "$feature/tasks.md" ]; then
        ((incomplete_features++))
    fi
done

completion_rate=$(((total_features - incomplete_features) * 100 / total_features))
echo "📚 Documentation Completeness: $completion_rate%"

# Patterns compliance (basic check)
if [ -d "../patterns" ]; then
    pattern_files=$(find ../patterns -name "*.md" | wc -l)
    echo "📐 Pattern Files: $pattern_files"
else
    echo "⚠️  Patterns directory not found"
fi

# Recent activity
recent_commits=$(git log --since="1 week ago" --oneline | wc -l)
echo "🔄 Commits (7 days): $recent_commits"

doc_updates=$(git log --since="1 week ago" --oneline -- ../ | grep -i "doc\|task\|spec" | wc -l)
echo "📝 Doc updates (7 days): $doc_updates"

echo ""
echo "🎯 HEALTH SCORE"
echo "============="

# Calculate overall health
health_score=$(((progress + completion_rate) / 2))

if [ $health_score -ge 80 ]; then
    echo "🟢 EXCELLENT ($health_score%) - Project is healthy!"
elif [ $health_score -ge 60 ]; then
    echo "🟡 GOOD ($health_score%) - Some areas need attention"
else
    echo "🔴 NEEDS IMPROVEMENT ($health_score%) - Focus on CDD adoption"
fi

echo ""
echo "📋 Recommendations:"
echo "- Review incomplete features"
echo "- Update outdated documentation"
echo "- Validate task ID formats"
echo "- Check patterns compliance" 