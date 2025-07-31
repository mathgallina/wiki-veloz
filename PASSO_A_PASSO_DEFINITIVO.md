# 🚀 Passo a Passo Definitivo - Base de Conhecimento Veloz

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

## 🔧 Se a porta 8000 estiver ocupada

### Verifique os processos:
```bash
lsof -i :8000
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
**http://127.0.0.1:8000**

ou

**http://localhost:8000**

## ✅ Status Atual
- ✅ Repositório clonado
- ✅ Ambiente virtual ativo
- ✅ Dependências instaladas
- ✅ Servidor rodando na porta 8000

## 🛑 Para parar o servidor
- Pressione `Ctrl+C` no terminal

---

**Pronto! Seu projeto está 100% funcional com toda a estrutura e páginas montadas.** 🎉 