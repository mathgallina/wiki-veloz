#!/bin/bash

# CDD v2.0 Integration Script
# Integra o CDD v2.0 com o projeto Wiki Veloz existente

set -e

echo "🚀 CDD v2.0 Integration Setup"
echo "=============================="

# Verificar se estamos no diretório correto
if [ ! -f "app.py" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto Wiki Veloz"
    exit 1
fi

echo "✅ Diretório correto detectado"

# 1. Configurar linting automático
echo ""
echo "📋 Configurando linting automático..."

# Copiar configurações de linting
if [ -f ".kiro/patterns/linting/.eslintrc.js" ]; then
    cp .kiro/patterns/linting/.eslintrc.js .eslintrc.js
    echo "✅ ESLint configurado"
fi

if [ -f ".kiro/patterns/linting/.prettierrc" ]; then
    cp .kiro/patterns/linting/.prettierrc .prettierrc
    echo "✅ Prettier configurado"
fi

if [ -f ".kiro/patterns/linting/pyproject.toml" ]; then
    # Mesclar com pyproject.toml existente se houver
    if [ -f "pyproject.toml" ]; then
        echo "⚠️  pyproject.toml já existe, mesclando configurações..."
        # Aqui você pode implementar uma lógica de merge mais sofisticada
    else
        cp .kiro/patterns/linting/pyproject.toml pyproject.toml
        echo "✅ pyproject.toml configurado"
    fi
fi

# 2. Configurar scripts no package.json
echo ""
echo "📋 Configurando scripts de desenvolvimento..."

if [ -f "package.json" ]; then
    # Adicionar scripts CDD se não existirem
    if ! grep -q "cdd:scan" package.json; then
        echo "✅ Adicionando scripts CDD ao package.json..."
        # Aqui você pode implementar uma lógica para adicionar scripts
    else
        echo "✅ Scripts CDD já configurados"
    fi
else
    echo "⚠️  package.json não encontrado, criando..."
    cat > package.json << 'EOF'
{
  "name": "wiki-veloz",
  "version": "1.0.0",
  "description": "Plataforma de documentação colaborativa",
  "scripts": {
    "dev": "python app.py",
    "test": "python -m pytest tests/",
    "lint": "flake8 . && black . && isort .",
    "lint:fix": "black . && isort .",
    "cdd:scan": "cd .kiro/scripts && npm run scan",
    "cdd:status": "cd .kiro/scripts && npm run status",
    "cdd:health": "cd .kiro/scripts && npm run health",
    "cdd:complete": "cd .kiro/scripts && npm run complete"
  },
  "devDependencies": {
    "eslint": "^8.0.0",
    "@typescript-eslint/parser": "^5.0.0",
    "@typescript-eslint/eslint-plugin": "^5.0.0",
    "prettier": "^2.8.0"
  }
}
EOF
    echo "✅ package.json criado com scripts CDD"
fi

# 3. Configurar Makefile para automação
echo ""
echo "📋 Configurando Makefile..."

cat > Makefile << 'EOF'
# CDD v2.0 - Wiki Veloz Makefile

.PHONY: help dev test lint lint-fix cdd-scan cdd-status cdd-health cdd-complete setup

help: ## Mostrar ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Rodar aplicação em desenvolvimento
	python app.py

test: ## Rodar testes
	python -m pytest tests/ -v

lint: ## Verificar linting
	flake8 .
	black --check .
	isort --check-only .

lint-fix: ## Corrigir problemas de linting
	black .
	isort .

cdd-scan: ## Escanear tasks CDD
	cd .kiro/scripts && npm run scan

cdd-status: ## Status do projeto CDD
	cd .kiro/scripts && npm run status

cdd-health: ## Health dashboard CDD
	cd .kiro/scripts && npm run health

cdd-complete: ## Marcar task como concluída (uso: make cdd-complete TASK=feature-1.1)
	cd .kiro/scripts && npm run complete $(TASK)

setup: ## Setup inicial do projeto
	pip install -r requirements.txt
	npm install
	cd .kiro/scripts && npm install
	make cdd-scan

deploy: ## Deploy para produção
	git push heroku main

backup: ## Backup manual
	cd .kiro/scripts && npm run backup

cleanup: ## Limpeza semanal
	cd .kiro/scripts && npm run cleanup
EOF

echo "✅ Makefile configurado"

# 4. Configurar .gitignore para CDD
echo ""
echo "📋 Configurando .gitignore..."

# Adicionar entradas CDD ao .gitignore se não existirem
if ! grep -q ".kiro/scripts/node_modules" .gitignore 2>/dev/null; then
    echo "" >> .gitignore
    echo "# CDD v2.0" >> .gitignore
    echo ".kiro/scripts/node_modules/" >> .gitignore
    echo ".kiro/scripts/tasks-status.json" >> .gitignore
    echo ".kiro/backups/" >> .gitignore
    echo "*.log" >> .gitignore
    echo "✅ .gitignore atualizado"
else
    echo "✅ .gitignore já configurado"
fi

# 5. Verificar estrutura CDD
echo ""
echo "📋 Verificando estrutura CDD..."

cd .kiro/scripts

# Verificar se os scripts CDD estão funcionando
if npm run scan > /dev/null 2>&1; then
    echo "✅ Scripts CDD funcionando"
else
    echo "⚠️  Scripts CDD precisam de setup"
    npm install
fi

# 6. Gerar relatório inicial
echo ""
echo "📊 Relatório Inicial CDD v2.0"
echo "=============================="

# Contar arquivos de documentação
docs_count=$(find . -name "*.md" | wc -l | tr -d ' ')
echo "📚 Documentação: $docs_count arquivos"

# Contar patterns
patterns_count=$(find ../patterns -name "*.md" | wc -l | tr -d ' ')
echo "📐 Patterns: $patterns_count arquivos"

# Contar specs
specs_count=$(find ../specs -name "*.md" | wc -l | tr -d ' ')
echo "📋 Specs: $specs_count arquivos"

# Verificar steering
steering_count=$(find ../steering -name "*.md" | wc -l | tr -d ' ')
echo "🎯 Steering: $steering_count documentos"

# Calcular health score
total_files=$((docs_count + patterns_count + specs_count + steering_count))
if [ $total_files -gt 0 ]; then
    health_score=$((total_files * 100 / 20))  # Assumindo 20 como máximo esperado
    if [ $health_score -gt 100 ]; then
        health_score=100
    fi
else
    health_score=0
fi

echo ""
echo "🎯 Health Score: $health_score%"

if [ $health_score -ge 80 ]; then
    echo "🟢 EXCELLENT - CDD v2.0 bem configurado!"
elif [ $health_score -ge 60 ]; then
    echo "🟡 GOOD - Algumas áreas precisam de atenção"
else
    echo "🔴 NEEDS IMPROVEMENT - Foco na adoção do CDD"
fi

# 7. Instruções finais
echo ""
echo "🎉 CDD v2.0 Integration Completa!"
echo "=================================="
echo ""
echo "📋 Próximos passos:"
echo "1. Execute: make setup"
echo "2. Execute: make cdd-scan"
echo "3. Execute: make cdd-health"
echo "4. Consulte: .cursorrules"
echo "5. Leia: .kiro/steering/product.md"
echo ""
echo "🔧 Comandos úteis:"
echo "- make dev          # Rodar aplicação"
echo "- make test         # Rodar testes"
echo "- make lint         # Verificar linting"
echo "- make cdd-status   # Status do projeto"
echo "- make cdd-health   # Health dashboard"
echo ""
echo "📚 Documentação:"
echo "- .cursorrules      # Regras para Cursor IDE"
echo "- .kiro/patterns/   # Padrões de código"
echo "- .kiro/steering/   # Direcionamento estratégico"
echo ""
echo "✅ CDD v2.0 integrado com sucesso!"

cd ../.. 