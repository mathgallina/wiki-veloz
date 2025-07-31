# 🖥️ Guia da Interface do Wiki Veloz

## 🚀 **ACESSO RÁPIDO**

### **1. Abra seu navegador e acesse:**
```
http://localhost:8000
```

### **2. Faça login com:**
- **Usuário**: `admin`
- **Senha**: `B@rcelona1998`

---

## 📱 **INTERFACES DISPONÍVEIS**

### **🏠 Página Principal**
- **URL**: http://localhost:8000
- **Funcionalidade**: Dashboard principal com visão geral do sistema

### **📄 Sistema de Páginas**
- **URL**: http://localhost:8000/pages
- **Funcionalidades**:
  - Listar todas as páginas
  - Criar nova página
  - Editar páginas existentes
  - Buscar páginas
  - Visualizar analytics

### **📁 Sistema de Documentos**
- **URL**: http://localhost:8000/documents
- **Funcionalidades**:
  - Listar documentos
  - Upload de arquivos
  - Download de documentos
  - Categorização
  - Analytics de storage

### **👥 Gerenciamento de Usuários**
- **URL**: http://localhost:8000/admin/users
- **Funcionalidades**:
  - Listar usuários
  - Criar novos usuários
  - Editar perfis
  - Gerenciar permissões

---

## 🔧 **APIs RESTful (Para Desenvolvedores)**

### **📄 Páginas**
```bash
# Listar páginas
GET http://localhost:8000/api/pages/

# Páginas recentes
GET http://localhost:8000/api/pages/recent

# Páginas populares
GET http://localhost:8000/api/pages/popular
```

### **📁 Documentos**
```bash
# Listar documentos
GET http://localhost:8000/documents/

# Documentos recentes
GET http://localhost:8000/documents/recent

# Analytics de storage
GET http://localhost:8000/documents/analytics/storage
```

### **👥 Usuários**
```bash
# Listar usuários
GET http://localhost:8000/api/users/
```

---

## 🎨 **CARACTERÍSTICAS DA INTERFACE**

### **✅ Design Responsivo**
- Funciona em desktop, tablet e mobile
- Interface moderna com Tailwind CSS
- Navegação intuitiva

### **✅ Funcionalidades Avançadas**
- Editor Markdown com preview
- Upload de arquivos
- Sistema de busca
- Analytics em tempo real
- Versionamento de conteúdo

### **✅ Segurança**
- Login seguro
- Controle de sessões
- Permissões por usuário
- Logs de atividades

---

## 🚨 **SOLUÇÃO DE PROBLEMAS**

### **Se o servidor não iniciar:**
```bash
# Parar processos na porta 8000
lsof -ti:8000 | xargs kill -9

# Iniciar novamente
python3 app.py
```

### **Se o login não funcionar:**
- Verifique se está usando: `admin` / `B@rcelona1998`
- Limpe o cache do navegador
- Tente em modo incógnito

### **Se as páginas não carregarem:**
- Verifique se o servidor está rodando
- Acesse: http://localhost:8000/auth/login
- Faça login novamente

---

## 📊 **DADOS DO SISTEMA**

### **📈 Estatísticas Atuais:**
- **8 páginas** criadas
- **3 documentos** no sistema
- **2 usuários** cadastrados
- **Sistema 100% funcional**

### **🔧 Tecnologias:**
- **Backend**: Flask 2.3+
- **Frontend**: Tailwind CSS
- **Database**: JSON Files
- **Arquitetura**: CDD v2.0

---

## 🎯 **PRÓXIMOS PASSOS**

1. **🌐 Acesse**: http://localhost:8000
2. **🔐 Faça login** com admin/B@rcelona1998
3. **📄 Explore** o sistema de páginas
4. **📁 Teste** o sistema de documentos
5. **👥 Gerencie** usuários
6. **🔌 Use** as APIs para integração

---

**🎉 Sistema Wiki Veloz CDD v2.0 funcionando perfeitamente!** 