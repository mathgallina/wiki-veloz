#!/bin/bash
echo "🧹 Limpando processors..."
pkill -f python
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 2
echo "🚀 Iniciando Wiki Veloz..."
echo "🌐 Acesse: http://localhost:8000"
echo "👤 Login: admin / B@rcelona1998"
python3 app.py
