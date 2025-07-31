# 🚀 Guia de Deploy - Wiki Veloz

## 📋 Status Atual
- ✅ **Local**: Funcionando perfeitamente
- ❌ **Render**: Problemas de configuração
- 🔄 **Railway**: Configuração em andamento

## 🎯 Solução Imediata para Colaboradores

### Opção 1: Uso Local (Recomendado)
```bash
# 1. Clonar o repositório
git clone https://github.com/mathgallina/wiki-veloz.git
cd wiki-veloz

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar servidor
python3 app.py

# 5. Acessar no navegador
# http://localhost:8000
# Login: admin / B@rcelona1998
```

### Opção 2: Deploy no Railway (Alternativa)
```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Fazer login
railway login

# 3. Deploy
railway up

# 4. Obter URL
railway domain
```

## 🔧 Configuração para Colaboradores

### Adicionar Novo Usuário
1. Acessar como admin
2. Ir para `/admin/users`
3. Adicionar novo colaborador

### Credenciais Padrão
- **Admin**: admin / B@rcelona1998
- **Novos usuários**: Serão criados pelo admin

## 📱 Acesso Móvel
- O sistema é responsivo
- Funciona em tablets e smartphones
- Interface otimizada para mobile

## 🔒 Segurança
- Todas as rotas protegidas por login
- Senhas criptografadas
- Logs de atividade
- Backup automático

## 🆘 Suporte
- Problemas técnicos: Verificar logs em `data/activity_log.json`
- Backup: Arquivos em `backups/`
- Configuração: Arquivo `app.py`

## 🚀 Próximos Passos
1. Testar Railway como alternativa ao Render
2. Configurar domínio personalizado
3. Implementar notificações por email
4. Adicionar mais funcionalidades

---
**Última atualização**: 23/07/2025
**Versão**: 1.0.0
