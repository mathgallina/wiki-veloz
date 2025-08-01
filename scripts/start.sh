#!/bin/bash
echo "🚀 Iniciando o servidor Flask..."
echo "🌐 Acesse: http://localhost:8002"
cd "$(dirname "$0")/.."
source .venv/bin/activate
python3 app.py
