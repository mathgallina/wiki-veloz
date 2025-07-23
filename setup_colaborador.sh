#!/bin/bash

echo "🚀 Setup Wiki Veloz para Colaboradores"
echo "======================================"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.9+ primeiro."
    exit 1
fi

# Verificar se Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Instale Git primeiro."
    exit 1
fi

echo "✅ Python e Git encontrados"

# Clonar repositório se não existir
if [ ! -d "wiki-veloz" ]; then
    echo "📥 Clonando repositório..."
    git clone https://github.com/mathgallina/wiki-veloz.git
    cd wiki-veloz
else
    echo "📁 Repositório já existe"
    cd wiki-veloz
fi

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
python3 -m venv .venv

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p data static/uploads backups

echo ""
echo "✅ Setup concluído!"
echo ""
echo "🎯 Para iniciar o servidor:"
echo "   source .venv/bin/activate"
echo "   python3 app.py"
echo ""
echo "🌐 Acesse: http://localhost:8000"
echo "🔑 Login: admin / B@rcelona1998"
echo ""
echo "📚 Para mais informações, consulte: deploy_guide.md"
