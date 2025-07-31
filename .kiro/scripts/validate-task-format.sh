#!/bin/bash

feature_name=$1
if [ -z "$feature_name" ]; then
    echo "Usage: ./validate-task-format.sh <feature-name>"
    echo "Example: ./validate-task-format.sh user-authentication"
    exit 1
fi

task_file="../specs/$feature_name/tasks.md"

if [ ! -f "$task_file" ]; then
    echo "❌ File not found: $task_file"
    exit 1
fi

echo "🔍 Validating task format for: $feature_name"

# Verificar padrão básico - apenas tasks principais (X.Y)
main_tasks=$(grep "^-\s\[" "$task_file" | grep -E "^\s*-\s\[[x ]\]\s+[0-9]+\.[0-9]+\s")
invalid_main_tasks=$(echo "$main_tasks" | grep -v "^\s*-\s\[[x ]\]\s\+[0-9]\+\.[0-9]\+\s")
if [ ! -z "$invalid_main_tasks" ]; then
    echo "❌ Invalid main task format found:"
    echo "$invalid_main_tasks"
    echo ""
    echo "Expected format: - [ ] X.Y Task description"
    exit 1
fi

# Verificar sequência
phases=$(grep -o "^-\s\[[x ]\]\s\+[0-9]\+\." "$task_file" | grep -o "[0-9]\+" | sort -u)
for phase in $phases; do
    tasks_in_phase=$(grep "^-\s\[[x ]\]\s\+$phase\." "$task_file" | grep -o "$phase\.[0-9]\+" | sort -V)
    expected=1
    for task in $tasks_in_phase; do
        task_num=$(echo $task | cut -d. -f2)
        if [ "$task_num" != "$expected" ]; then
            echo "❌ Gap in Phase $phase: expected $phase.$expected, found $task"
            exit 1
        fi
        ((expected++))
    done
done

echo "✅ All task formats are valid for $feature_name" 