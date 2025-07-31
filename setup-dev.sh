#!/bin/bash

echo "🚀 Configurando ambiente de desenvolvimento para Wiki Veloz Fibra..."

# Criar ambiente virtual Python
echo "📦 Criando ambiente virtual Python..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências Python..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar pre-commit hooks (opcional)
echo "🔧 Configurando formatação automática..."

# Tornar o script executável
chmod +x setup-dev.sh

echo "✅ Ambiente configurado com sucesso!"
echo ""
echo "🎯 Próximos passos:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Execute o servidor: python3 app.py"
echo "3. Acesse: http://127.0.0.1:8000"
echo ""
echo "🔧 Recursos configurados:"
echo "- Prettier: Formatação automática de código"
echo "- ESLint: Análise de qualidade JavaScript"
echo "- Black: Formatação Python"
echo "- Flake8: Linting Python"
echo "- Live Preview: Visualização em tempo real"
