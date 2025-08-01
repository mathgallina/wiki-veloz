# 🚀 Passo a Passo Definitivo - Wiki Veloz Fibra

## 📥 Clonar o repositório do GitHub

### 1. Clone o repositório
```bash
git clone https://github.com/mathgallina/wiki-veloz.git
cd wiki-veloz
```

## ⚡ Comandos Essenciais (Copie e Cole)

### 2. Crie o ambiente virtual
```bash
python3 -m venv .venv
```

### 3. Ative o ambiente virtual
```bash
source .venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Execute o servidor
```bash
python3 app.py
```

## 🔧 Se a porta 8002 estiver ocupada

### Verifique os processos:
```bash
lsof -i :8002
```

### Mate os processos (substitua pelos PIDs que aparecerem):
```bash
kill -9 PID_DO_PROCESSO
```

**Exemplo:**
```bash
kill -9 5098 5100
```

### Depois rode novamente:
```bash
python3 app.py
```

## 🌐 Acesse no navegador
**http://127.0.0.1:8002**

ou

**http://localhost:8002**

## ✅ Status Atual
- ✅ Repositório conectado ao GitHub
- ✅ Ambiente virtual ativo
- ✅ Dependências instaladas
- ✅ Servidor rodando na porta 8000

## 🛑 Para parar o servidor
- Pressione `Ctrl+C` no terminal

## 📚 Sobre o Projeto

**Wiki Veloz Fibra** é um sistema de Wiki Interna da Veloz Fibra - Plataforma de documentação colaborativa que resolve o problema de documentação fragmentada em organizações.

### 🚀 Stack Tecnológica
- **Backend**: Flask 2.3+ (Python 3.11+)
- **Frontend**: Vanilla JavaScript + Tailwind CSS + Alpine.js
- **Database**: JSON files + Google Drive API
- **Deployment**: Heroku/Railway
- **Arquitetura**: Monolítica → Microservices (evolução)

---

**Pronto! Seu projeto está 100% funcional e conectado ao GitHub.** 🎉 