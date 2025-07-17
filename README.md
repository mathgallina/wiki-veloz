# 🚀 Wiki Veloz Fibra

Sistema de Wiki Interna da Veloz Fibra - Plataforma completa para documentação, gerenciamento de usuários, upload de PDFs e backup automático.

## ✨ Funcionalidades

### 📚 **Wiki e Documentação**

- ✅ Criação e edição de páginas
- ✅ Categorização de conteúdo
- ✅ Sistema de busca avançada
- ✅ Histórico de mudanças
- ✅ Markdown support

### 👥 **Gerenciamento de Usuários**

- ✅ Sistema de login seguro
- ✅ Controle de acesso por roles
- ✅ Perfis de usuário
- ✅ Logs de atividade
- ✅ Notificações em tempo real

### 📄 **Sistema de PDFs**

- ✅ Upload de documentos
- ✅ Visualização inline
- ✅ Download seguro
- ✅ Categorização
- ✅ Busca por conteúdo

### 💾 **Sistema de Backup**

- ✅ Backup automático
- ✅ Criptografia de dados
- ✅ Compressão inteligente
- ✅ Integração Google Drive (opcional)
- ✅ Restauração de dados

### 📊 **Analytics e Relatórios**

- ✅ Dashboard administrativo
- ✅ Métricas de uso
- ✅ Relatórios exportáveis
- ✅ Gráficos interativos

## 🛠️ Tecnologias

### Backend

- **Python 3.9+**
- **Flask** - Framework web
- **Flask-Login** - Autenticação
- **Werkzeug** - Utilitários web
- **bcrypt** - Criptografia de senhas
- **Pillow** - Processamento de imagens
- **cryptography** - Criptografia avançada

### Frontend

- **HTML5** - Estrutura
- **Tailwind CSS** - Estilização
- **Alpine.js** - Interatividade
- **JavaScript** - Funcionalidades

### DevOps

- **Docker** - Containerização
- **Git** - Versionamento
- **Pre-commit** - Qualidade de código
- **Black** - Formatação Python
- **Flake8** - Linting Python
- **ESLint** - Linting JavaScript

## 🚀 Instalação

### Pré-requisitos

- Python 3.9+
- Node.js 16+
- Git

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/wiki-veloz-fibra.git
cd wiki-veloz-fibra
```

### 2. Configure o ambiente Python

```bash
# Crie o ambiente virtual
python3 -m venv .venv

# Ative o ambiente
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configure o ambiente Node.js

```bash
# Instale as dependências do frontend
npm install

# Compile o CSS
npm run build:css
```

### 4. Configure as variáveis de ambiente

```bash
# Crie o arquivo .env
cp .env.example .env

# Edite as variáveis conforme necessário
nano .env
```

### 5. Inicialize o banco de dados

```bash
# Execute o script de inicialização
python3 app.py
```

### 6. Execute o servidor

```bash
# Desenvolvimento
python3 app.py

# Ou usando Docker
docker-compose up -d
```

## 📖 Uso

### Acesso ao Sistema

1. Abra o navegador em `http://localhost:8000`
2. Faça login com as credenciais:
   - **Usuário**: `matheus.gallina`
   - **Senha**: `B@rcelona1998`

### Funcionalidades Principais

#### 📚 Criar Páginas

1. Acesse a página inicial
2. Clique em "Nova Página"
3. Preencha título, categoria e conteúdo
4. Use Markdown para formatação
5. Salve a página

#### 📄 Upload de PDFs

1. Acesse "Gerenciar PDFs" no menu
2. Arraste arquivos ou clique para selecionar
3. Adicione descrição e tags
4. Visualize ou baixe os documentos

#### 👥 Gerenciar Usuários

1. Acesse "Gerenciar Usuários" (apenas admin)
2. Crie novos usuários
3. Defina roles e permissões
4. Monitore atividades

#### 💾 Sistema de Backup

1. Acesse "Sistema de Backup"
2. Configure backup automático
3. Monitore status dos backups
4. Restaure dados quando necessário

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_users.py
```

### Qualidade de Código

```bash
# Formatação
black . --line-length=88

# Linting
flake8 . --max-line-length=88

# Organizar imports
isort . --profile=black

# Verificar tudo
npm run check
```

## 🐳 Docker

### Desenvolvimento

```bash
# Construir imagem
docker build -t wiki-veloz .

# Executar container
docker run -p 8000:8000 wiki-veloz

# Ou usar docker-compose
docker-compose up -d
```

### Produção

```bash
# Construir para produção
docker build -t wiki-veloz:prod .

# Executar com variáveis de produção
docker run -d \
  -p 8000:8000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=sua-chave-secreta \
  wiki-veloz:prod
```

## 📁 Estrutura do Projeto

```
wiki-veloz-fibra/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── package.json          # Dependências Node.js
├── pyproject.toml        # Configuração Python
├── tailwind.config.js    # Configuração Tailwind
├── .pre-commit-config.yaml # Hooks de qualidade
├── Dockerfile            # Containerização
├── docker-compose.yml    # Orquestração
├── .vscode/             # Configurações VS Code
│   └── settings.json
├── data/                # Dados da aplicação
│   ├── users.json
│   ├── pages.json
│   ├── notifications.json
│   └── activity_log.json
├── static/              # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── uploads/
├── templates/           # Templates HTML
│   ├── index.html
│   ├── login.html
│   └── admin_*.html
├── tests/              # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
└── backups/            # Backups do sistema
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# .env
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=52428800
```

### Configurações do VS Code

O projeto inclui configurações otimizadas para:

- ✅ Formatação automática
- ✅ Linting em tempo real
- ✅ IntelliSense para Python
- ✅ Suporte a Tailwind CSS
- ✅ Git integration
- ✅ Debugging

## 📊 Monitoramento

### Logs

- Logs de aplicação em `logs/`
- Logs de atividade em `data/activity_log.json`
- Logs de erro em console

### Métricas

- Dashboard de analytics em `/admin/analytics`
- Relatórios exportáveis
- Métricas de performance

## 🔒 Segurança

### Implementado

- ✅ Autenticação segura
- ✅ Criptografia de senhas
- ✅ Controle de acesso por roles
- ✅ Validação de entrada
- ✅ Sanitização de dados
- ✅ Proteção CSRF
- ✅ Headers de segurança

### Recomendações

- Use HTTPS em produção
- Configure firewall adequado
- Mantenha dependências atualizadas
- Monitore logs de segurança
- Faça backups regulares

## 🤝 Contribuição

### Como Contribuir

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -am 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### Padrões de Código

- Use Black para formatação Python
- Use Prettier para formatação JavaScript
- Siga as convenções PEP 8
- Escreva testes para novas funcionalidades
- Documente APIs e funções

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Desenvolvido por

**Matheus Gallina** - [matheus@velozfibra.com](mailto:matheus@velozfibra.com)

## 🆘 Suporte

### Problemas Comuns

#### Erro de Porta Ocupada

```bash
# Encontre o processo
lsof -ti:8000

# Mate o processo
kill -9 $(lsof -ti:8000)
```

#### Erro de Dependências

```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

#### Problemas de CSS

```bash
# Recompile o CSS
npm run build:css:prod
```

### Contato

- **Email**: matheus@velozfibra.com
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/wiki-veloz-fibra/issues)

---

**⭐ Se este projeto te ajudou, considere dar uma estrela!**
