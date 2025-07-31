#!/bin/bash
echo "🚀 Iniciando o servidor Flask..."
cd "$(dirname "$0")/.."
source .venv/bin/activate
python3 app.py
