# 🚀 Deploy no GitHub - Wiki Veloz Fibra

## 📋 Passos para colocar no GitHub:

### 1. Criar repositório no GitHub
1. Acesse [github.com](https://github.com)
2. Clique em "New repository"
3. Nome: `wiki-veloz-fibra`
4. Descrição: "Sistema de wiki interna da Veloz Fibra"
5. Deixe público (para facilitar o deploy)
6. **NÃO** inicialize com README (já temos um)

### 2. Conectar repositório local
```bash
git remote add origin https://github.com/SEU_USUARIO/wiki-veloz-fibra.git
git branch -M main
git push -u origin main
```

### 3. Opções de Deploy

#### Opção A: Deploy Local (Recomendado)
```bash
# Clone o repositório em qualquer máquina
git clone https://github.com/SEU_USUARIO/wiki-veloz-fibra.git
cd wiki-veloz-fibra
python3 -m pip install -r requirements.txt
python3 app.py
# Acesse: http://localhost:8000
```

#### Opção B: Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte sua conta GitHub
3. Selecione o repositório `wiki-veloz-fibra`
4. Deploy automático

#### Opção C: Render.com
1. Acesse [render.com](https://render.com)
2. Conecte GitHub
3. Crie novo Web Service
4. Selecione o repositório
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

#### Opção D: Railway
1. Acesse [railway.app](https://railway.app)
2. Conecte GitHub
3. Selecione o repositório
4. Deploy automático

### 4. Configuração para Produção

Crie um arquivo `Procfile` para deploy:
```
web: gunicorn app:app
```

Adicione gunicorn ao requirements.txt:
```
gunicorn==21.2.0
```

### 5. Variáveis de Ambiente (se necessário)
```bash
FLASK_ENV=production
FLASK_DEBUG=0
```

## 🎯 URLs de Acesso

Após o deploy, você terá URLs como:
- **Streamlit**: `https://wiki-veloz-fibra.streamlit.app`
- **Render**: `https://wiki-veloz-fibra.onrender.com`
- **Railway**: `https://wiki-veloz-fibra.railway.app`

## 📱 Compartilhamento com a Equipe

1. **Envie o link** do deploy para a equipe
2. **Configure autenticação** se necessário
3. **Adicione colaboradores** no GitHub
4. **Documente o uso** na wiki

## 🔧 Manutenção

### Atualizações
```bash
# Faça alterações localmente
git add .
git commit -m "Atualização da wiki"
git push origin main
# O deploy será atualizado automaticamente
```

### Backup
- O arquivo `data/pages.json` contém todo o conteúdo
- Faça backup regular
- Considere usar GitHub para versionamento

---

**Pronto para deploy! 🚀** 