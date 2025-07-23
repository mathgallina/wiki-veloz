#!/bin/bash

echo "🧹 WEEKLY CLEANUP - CDD v2.0"
echo "=============================="
echo "Started: $(date)"
echo ""

# Clean old backups (keep last 10)
backup_count=$(find ../backups -maxdepth 1 -type d | wc -l)
if [ $backup_count -gt 11 ]; then
    echo "🗑️  Cleaning old backups..."
    find ../backups -maxdepth 1 -type d | sort | head -n $((backup_count - 10)) | xargs rm -rf
    echo "✅ Old backups cleaned"
else
    echo "📁 Backup count OK ($backup_count directories)"
fi

# Clean old status files (keep last 5)
status_files=$(find . -name "tasks-status-*.json" | wc -l)
if [ $status_files -gt 5 ]; then
    echo "🗑️  Cleaning old status files..."
    find . -name "tasks-status-*.json" | sort | head -n $((status_files - 5)) | xargs rm -f
    echo "✅ Old status files cleaned"
else
    echo "📄 Status files count OK ($status_files files)"
fi

# Validate all task formats
echo "🔍 Validating all task formats..."
for feature in $(find ../specs -mindepth 1 -maxdepth 1 -type d | grep -v "_template"); do
    feature_name=$(basename "$feature")
    if [ -f "$feature/tasks.md" ]; then
        echo "  Checking $feature_name..."
        ./validate-task-format.sh "$feature_name" 2>/dev/null || echo "    ⚠️  Issues found in $feature_name"
    fi
done

# Check for orphaned files
echo "🔍 Checking for orphaned files..."
orphaned_files=$(find ../specs -name "*.md" -not -path "*/_template/*" | while read file; do
    dir=$(dirname "$file")
    if [ ! -f "$dir/requirements.md" ] || [ ! -f "$dir/design.md" ] || [ ! -f "$dir/tasks.md" ]; then
        echo "$file"
    fi
done | wc -l)

if [ $orphaned_files -gt 0 ]; then
    echo "⚠️  Found $orphaned_files potentially orphaned files"
else
    echo "✅ No orphaned files found"
fi

# Generate health report
echo "📊 Generating health report..."
./health-dashboard.sh > "../health-report-$(date +%Y-%m-%d).txt"

echo ""
echo "✅ Weekly cleanup completed!"
echo "📋 Summary:"
echo "  - Backups: Cleaned"
echo "  - Status files: Cleaned"
echo "  - Task validation: Completed"
echo "  - Health report: Generated" 