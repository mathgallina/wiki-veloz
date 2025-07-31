#!/bin/bash

echo "🚀 Configurando Base de Conhecimento Veloz..."

# Verificar se estamos no diretório correto
if [ ! -f "app.py" ]; then
    echo "❌ Erro: Execute este script na pasta raiz do projeto (onde está o app.py)"
    exit 1
fi

# 1. Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
else
    echo "✅ Ambiente virtual já existe"
fi

# 2. Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# 3. Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# 4. Verificar se a porta 8000 está ocupada
echo "🔍 Verificando porta 8000..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "⚠️  Porta 8000 está ocupada. Matando processos..."
    lsof -ti :8000 | xargs kill -9
    sleep 2
fi

# 5. Iniciar o servidor
echo "🌐 Iniciando servidor Flask..."
echo "📍 Acesse: http://localhost:8000"
echo "🛑 Para parar: Ctrl+C"
echo ""

python3 app.py 