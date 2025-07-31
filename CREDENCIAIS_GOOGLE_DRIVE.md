# 🔐 Configuração do Google Drive - Wiki Veloz Fibra

## 📋 Como Configurar o Google Drive

### 1. Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto ou selecione um existente
3. Ative a **Google Drive API**

### 2. Criar Credenciais OAuth 2.0

1. Vá em **APIs & Services** → **Credentials**
2. Clique em **Create Credentials** → **OAuth 2.0 Client IDs**
3. Configure:
   - **Application type**: Desktop application
   - **Name**: Wiki Veloz Backup
4. Baixe o arquivo JSON das credenciais

### 3. Renomear Arquivo

Renomeie o arquivo baixado para `credentials.json` e coloque na raiz do projeto.

### 4. Estrutura do Arquivo credentials.json

```json
{
  "installed": {
    "client_id": "seu-client-id.apps.googleusercontent.com",
    "project_id": "seu-projeto",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "seu-client-secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

### 5. Configurar no Sistema

1. Coloque o arquivo `credentials.json` na raiz do projeto
2. Acesse o sistema de backup
3. Clique em **Configurar Google Drive**
4. Siga as instruções de autorização

### 🔒 Permissões Necessárias

O sistema solicita apenas permissão para:

- ✅ Ler e escrever arquivos no Google Drive
- ✅ Acessar apenas arquivos criados pelo sistema
- ✅ Não acessa outros arquivos do usuário

### 📁 Pasta de Backup

O sistema criará automaticamente uma pasta chamada **"Wiki-Veloz-Backups"** no Google Drive.

### ⚠️ Importante

- Mantenha o arquivo `credentials.json` seguro
- Não compartilhe as credenciais
- O arquivo `token.json` será criado automaticamente após a primeira autorização

---

**💡 Dica**: Após configurar, os backups serão enviados automaticamente para o Google Drive!
