#!/bin/bash

echo "🚀 Instalando extensões recomendadas para o projeto Wiki Veloz Fibra..."
echo ""

# Python Development
echo "📦 Instalando extensões Python..."
code --install-extension ms-python.python
code --install-extension ms-python.pylance
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
code --install-extension ms-python.isort

# Frontend Development
echo "🎨 Instalando extensões Frontend..."
code --install-extension bradlc.vscode-tailwindcss
code --install-extension formulahendry.auto-rename-tag
code --install-extension formulahendry.auto-close-tag
code --install-extension ms-vscode.vscode-typescript-next

# Code Quality
echo "🔍 Instalando extensões de Qualidade de Código..."
code --install-extension ms-vscode.vscode-eslint
code --install-extension ms-vscode.vscode-prettier
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension streetsidesoftware.code-spell-checker-portuguese-brazilian
code --install-extension sonarsource.sonarlint-vscode

# Git & Version Control
echo "📚 Instalando extensões Git..."
code --install-extension eamodio.gitlens
code --install-extension mhutchie.git-graph

# API Testing
echo "🌐 Instalando extensões para Teste de API..."
code --install-extension rangav.vscode-thunder-client
code --install-extension humao.rest-client

# Productivity
echo "⚡ Instalando extensões de Produtividade..."
code --install-extension ms-vscode.live-server
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
code --install-extension ms-vscode.vscode-markdownlint

# Database
echo "🗄️ Instalando extensões de Banco de Dados..."
code --install-extension ms-mssql.mssql
code --install-extension cweijan.vscode-mysql-client2

# Docker
echo "🐳 Instalando extensões Docker..."
code --install-extension ms-azuretools.vscode-docker

# Themes & Icons
echo "🎨 Instalando temas e ícones..."
code --install-extension pkief.material-icon-theme
code --install-extension zhuangtongfa.material-theme

# Utilities
echo "🛠️ Instalando utilitários..."
code --install-extension ms-vscode.vscode-js-debug
code --install-extension ms-vscode.vscode-js-debug-companion

echo ""
echo "✅ Todas as extensões foram instaladas!"
echo ""
echo "🎯 Próximos passos:"
echo "1. Reinicie o VS Code/Cursor"
echo "2. Configure o tema Material Icon Theme"
echo "3. Configure o Prettier para formatação automática"
echo "4. Configure o ESLint para análise de código"
echo ""
echo "📚 Documentação das extensões:"
echo "- Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python"
echo "- Tailwind CSS: https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss"
echo "- GitLens: https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens"
echo "- Thunder Client: https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client"
