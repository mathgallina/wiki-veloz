#!/bin/bash

feature_name=$1
if [ -z "$feature_name" ]; then
    echo "Usage: ./new-feature.sh <feature-name>"
    echo "Example: ./new-feature.sh user-profile"
    exit 1
fi

# Validar nome da feature (kebab-case)
if [[ ! "$feature_name" =~ ^[a-z0-9-]+$ ]]; then
    echo "❌ Feature name must be kebab-case (lowercase, hyphens only)"
    echo "Example: user-profile, auth-system, data-export"
    exit 1
fi

feature_dir="../specs/$feature_name"

if [ -d "$feature_dir" ]; then
    echo "❌ Feature already exists: $feature_name"
    exit 1
fi

echo "🚀 Creating new feature: $feature_name"

# Criar diretório da feature
mkdir -p "$feature_dir"

# Copiar templates
cp ../specs/_template/requirements.md "$feature_dir/"
cp ../specs/_template/design.md "$feature_dir/"
cp ../specs/_template/tasks.md "$feature_dir/"

# Substituir placeholders nos arquivos
sed -i '' "s/\[Nome da Funcionalidade\]/$feature_name/g" "$feature_dir/requirements.md"
sed -i '' "s/\[Nome da Funcionalidade\]/$feature_name/g" "$feature_dir/design.md"
sed -i '' "s/\[Feature Name\]/$feature_name/g" "$feature_dir/tasks.md"
sed -i '' "s/\[feature-name\]/$feature_name/g" "$feature_dir/tasks.md"

echo "✅ Feature created successfully!"
echo ""
echo "📁 Files created:"
echo "  - $feature_dir/requirements.md"
echo "  - $feature_dir/design.md"
echo "  - $feature_dir/tasks.md"
echo ""
echo "🎯 Next steps:"
echo "  1. Edit requirements.md with user stories"
echo "  2. Edit design.md with technical decisions"
echo "  3. Edit tasks.md with implementation plan"
echo "  4. Run: npm run scan"
echo "  5. Start implementing with: npm run complete $feature_name-1.1" 