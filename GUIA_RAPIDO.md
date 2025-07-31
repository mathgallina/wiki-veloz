# 🚀 Guia Rápido - Base de Conhecimento Veloz

## ⚡ Comandos Essenciais

### Opção 1: Setup Automático (Recomendado)
```bash
cd ~/projetos/base-conhecimento-veloz
bash scripts/setup.sh
```

### Opção 2: Manual
```bash
cd ~/projetos/base-conhecimento-veloz
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

### Opção 3: Script de Inicialização
```bash
cd ~/projetos/base-conhecimento-veloz
bash scripts/start.sh
```

## 🌐 Acesso
- **URL:** http://localhost:8000
- **URL Alternativa:** http://127.0.0.1:8000

## 🔧 Solução de Problemas

### Porta 8000 ocupada:
```bash
lsof -i :8000
kill -9 PID_DO_PROCESSO
```

### Parar servidor:
- Pressione `Ctrl+C` no terminal

### Verificar se está rodando:
```bash
curl -I http://127.0.0.1:8000
```

## 📁 Estrutura
```
base-conhecimento-veloz/
├── app.py              # Servidor Flask
├── scripts/setup.sh    # Setup automático
├── scripts/start.sh    # Inicialização
├── templates/          # HTML
├── static/             # CSS/JS
└── requirements.txt    # Dependências
```

---
**Status:** ✅ Funcionando na porta 8000 