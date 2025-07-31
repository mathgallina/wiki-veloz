#!/bin/bash

backup_dir="../backups/$(date +%Y-%m-%d_%H-%M-%S)"
mkdir -p "$backup_dir"

echo "💾 Creating backup: $backup_dir"

# Backup tasks files
find ../specs -name "tasks.md" -exec cp {} "$backup_dir/" \;

# Backup status
cp tasks-status.json "$backup_dir/" 2>/dev/null || true

# Create backup info
cat > "$backup_dir/backup-info.json" << JSON
{
  "timestamp": "$(date -Iseconds)",
  "user": "$(git config user.name)",
  "files_backed_up": $(find "$backup_dir" -name "*.md" | wc -l),
  "git_commit": "$(git rev-parse HEAD)"
}
JSON

echo "✅ Backup created successfully: $backup_dir" 