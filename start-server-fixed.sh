#!/bin/bash
echo "🚀 Iniciando Wiki Veloz em porta diferente..."
echo "🌐 Acesse: http://localhost:8001"
echo "👤 Login: admin / B@rcelona1998"
python3 -c "import app; app.app.run(host=\"0.0.0.0\", port=8001, debug=False)"
