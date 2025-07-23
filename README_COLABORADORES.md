# 🚀 Wiki Veloz - Guia para Colaboradores

## 📋 Visão Geral
O **Wiki Veloz** é a central de conhecimento da Veloz Fibra, onde todos os colaboradores podem acessar documentação, procedimentos e informações importantes da empresa.

## 🎯 Como Usar

### ⚡ Setup Rápido (Recomendado)

#### Para Mac/Linux:
```bash
# Execute o script de setup
./setup_colaborador.sh
```

#### Para Windows:
```cmd
# Execute o script de setup
setup_colaborador.bat
```

### 🔧 Setup Manual

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/mathgallina/wiki-veloz.git
   cd wiki-veloz
   ```

2. **Criar ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Rodar servidor:**
   ```bash
   python3 app.py
   ```

5. **Acessar no navegador:**
   ```
   http://localhost:8000
   ```

## 🔑 Credenciais de Acesso

### Admin (Matheus Gallina)
- **Usuário:** `admin`
- **Senha:** `B@rcelona1998`

### Novos Colaboradores
- Serão criados pelo admin
- Receberão credenciais por email/WhatsApp

## 📚 Funcionalidades Principais

### 📄 Documentos
- **Localização:** `/documents/`
- **Funcionalidades:**
  - Criar, editar, visualizar documentos
  - Upload de anexos (PDFs, imagens)
  - Versionamento de documentos
  - Categorização por setor

### 📊 Analytics
- **Localização:** `/admin/analytics`
- **Funcionalidades:**
  - Estatísticas de uso
  - Relatórios de atividade
  - Métricas de performance

### 👥 Gestão de Usuários
- **Localização:** `/admin/users`
- **Funcionalidades:**
  - Adicionar novos colaboradores
  - Gerenciar permissões
  - Monitorar atividade

### 💾 Backup
- **Localização:** `/admin/backup`
- **Funcionalidades:**
  - Backup automático
  - Integração Google Drive
  - Restauração de dados

## 🛠️ Troubleshooting

### Problema: Porta 8000 ocupada
```bash
# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problema: Erro de dependências
```bash
pip install --upgrade -r requirements.txt
```

### Problema: Erro de permissões
```bash
# Mac/Linux
chmod +x setup_colaborador.sh

# Windows
# Execute como administrador
```

## 📱 Acesso Móvel
- O sistema é totalmente responsivo
- Funciona em smartphones e tablets
- Interface otimizada para touch

## 🔒 Segurança
- Todas as rotas protegidas por login
- Senhas criptografadas
- Logs de atividade completos
- Backup automático dos dados

## 📞 Suporte
- **Problemas técnicos:** Verificar logs em `data/activity_log.json`
- **Backup:** Arquivos em `backups/`
- **Configuração:** Arquivo `app.py`

## 🚀 Próximas Funcionalidades
- [ ] Notificações por email
- [ ] App mobile nativo
- [ ] Integração com sistemas externos
- [ ] Chat interno
- [ ] Calendário de eventos

## 📋 Checklist para Novos Colaboradores
- [ ] Executar script de setup
- [ ] Testar acesso local
- [ ] Receber credenciais do admin
- [ ] Fazer primeiro login
- [ ] Explorar funcionalidades
- [ ] Ler documentação disponível

---
**Última atualização:** 23/07/2025  
**Versão:** 1.0.0  
**Contato:** matheus@velozfibra.com
