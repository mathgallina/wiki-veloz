# 🔐 BACKUP COMPLETO - Wiki Veloz Fibra

## 📍 **Informações do Projeto**

### **Repositório GitHub:**
- **URL:** https://github.com/mathgallina/wiki-veloz.git
- **Username:** mathgallina
- **Nome do repositório:** wiki-veloz

### **Local do Projeto:**
- **Caminho:** `/Users/mathuesgallina/projetos/base-conhecimento-veloz`
- **Ambiente virtual:** `.venv`

## 🚀 **Como Rodar o Projeto (PASSO A PASSO)**

### **1. Clone o repositório**
```bash
git clone https://github.com/mathgallina/wiki-veloz.git
cd wiki-veloz
```

### **2. Configure o ambiente virtual**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Instale as dependências**
```bash
pip install -r requirements.txt
```

### **4. Execute o servidor**
```bash
python3 app.py
```

### **5. Acesse no navegador**
- **http://localhost:8000**
- **http://127.0.0.1:8000**

## 🔧 **Comandos Úteis**

### **Para parar o servidor:**
- Pressione `Ctrl+C` no terminal

### **Para verificar se está rodando:**
```bash
curl -I http://127.0.0.1:8000
```

### **Para matar processos na porta 8000:**
```bash
lsof -i :8000
kill -9 PID_DO_PROCESSO
```

### **Para fazer commit e push:**
```bash
git add .
git commit -m "Sua mensagem"
git push origin main
```

## 📋 **Status Atual (31/07/2025)**

### ✅ **Funcionando:**
- ✅ Repositório conectado ao GitHub
- ✅ Ambiente virtual configurado
- ✅ Todas as dependências instaladas
- ✅ Servidor rodando na porta 8000
- ✅ Sistema de login funcionando
- ✅ Interface web acessível
- ✅ Todas as funcionalidades ativas

### 📊 **Logs do Sistema:**
```
INFO:app:Main blueprint registered
INFO:app:Auth blueprint registered
INFO:app:Users blueprint registered
INFO:app:Pages blueprint registered
INFO:app:Documents blueprint registered
INFO:app:PDFs blueprint registered
INFO:app:Notifications blueprint registered
INFO:app:Analytics blueprint registered
INFO:app:Activity blueprint registered
INFO:app:Backup blueprint registered
INFO:app:All blueprints registered
INFO:app:Error handlers registered
INFO:app:Context processors registered
INFO:app:Default admin user created
INFO:app:Flask application created successfully
```

## 🛠️ **Stack Tecnológica**

- **Backend:** Flask 2.3+ (Python 3.11+)
- **Frontend:** Vanilla JavaScript + Tailwind CSS + Alpine.js
- **Database:** JSON files + Google Drive API
- **Deployment:** Heroku/Railway
- **Arquitetura:** Monolítica → Microservices (evolução)

## 📁 **Estrutura do Projeto**

```
wiki-veloz/
├── app/                    # Aplicação Flask principal
│   ├── core/              # Configurações e banco de dados
│   ├── modules/           # Módulos da aplicação
│   ├── shared/            # Utilitários compartilhados
│   ├── static/            # Arquivos estáticos
│   └── templates/         # Templates HTML
├── components/            # Componentes JavaScript reutilizáveis
├── pages/                # Rotas principais do sistema
├── services/             # Integrações com APIs e serviços
├── utils/                # Funções auxiliares
├── constants/            # Constantes e configurações
├── tests/                # Testes automatizados
└── data/                 # Arquivos JSON (banco de dados)
```

## 🔐 **Credenciais e Acesso**

### **Usuário Admin Padrão:**
- **Username:** admin
- **Password:** admin123
- **Role:** admin

### **URLs de Acesso:**
- **Login:** http://localhost:8000/auth/login
- **Dashboard:** http://localhost:8000/
- **Documentos:** http://localhost:8000/documents/
- **Admin:** http://localhost:8000/admin/users

## 📝 **Dependências Principais**

```
Flask==2.3.3
Flask-CORS==4.0.0
markdown==3.5.1
python-slugify==8.0.1
Werkzeug==2.3.7
gunicorn==21.2.0
Flask-Login==0.6.3
Flask-WTF==1.1.1
WTForms==3.0.1
bcrypt==4.0.1
python-dotenv==1.0.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
cryptography==41.0.7
schedule==1.2.0
zipfile36==0.1.3
```

## 🚨 **Solução de Problemas**

### **Erro: "No module named 'flask_cors'"**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### **Erro: "ImportError: cannot import name 'Flask'"**
```bash
source .venv/bin/activate
pip install Flask==2.3.3
```

### **Porta 8000 ocupada:**
```bash
lsof -i :8000
kill -9 PID_DO_PROCESSO
```

## 📞 **Contatos e Suporte**

- **Desenvolvedor:** Matheus Gallina
- **Email:** matheus@velozfibra.com
- **GitHub:** @mathuesgallina

## 🎯 **Funcionalidades Implementadas**

- ✅ Sistema de autenticação
- ✅ Gerenciamento de usuários
- ✅ Sistema de documentos
- ✅ Upload de PDFs
- ✅ Sistema de notificações
- ✅ Analytics dashboard
- ✅ Sistema de backup
- ✅ Interface responsiva
- ✅ Dark mode
- ✅ Integração Google Drive

## 🔄 **Workflow de Desenvolvimento**

1. **Fazer alterações no código**
2. **Testar localmente:** `python3 app.py`
3. **Fazer commit:** `git add . && git commit -m "mensagem"`
4. **Fazer push:** `git push origin main`
5. **Deploy automático** (se configurado)

---

**📅 Última atualização:** 31/07/2025  
**✅ Status:** FUNCIONANDO PERFEITAMENTE  
**🎉 Sistema:** 100% OPERACIONAL  

**NÃO PERCA MAIS ESTE PROJETO!** 🔐 