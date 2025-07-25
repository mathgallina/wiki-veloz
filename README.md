# Wiki Veloz Fibra

Sistema de Wiki Interna da Veloz Fibra - Plataforma de documentação colaborativa que resolve o problema de documentação fragmentada em organizações.

## 🚀 Stack Tecnológica

- **Backend**: Flask 2.3+ (Python 3.11+)
- **Frontend**: Vanilla JavaScript + Tailwind CSS + Alpine.js
- **Database**: JSON files + Google Drive API
- **Deployment**: Heroku/Railway
- **Arquitetura**: Monolítica → Microservices (evolução)

## 📋 Pré-requisitos

- Python 3.11+
- Node.js 16+
- npm 8+

## 🛠️ Como Rodar Localmente

### 1. Clone o repositório

```bash
git clone <repository-url>
cd wiki-veloz
```

### 2. Configure o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
npm install
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Execute a aplicação

```bash
# Desenvolvimento
python app.py

# Ou usando npm
npm run dev
```

A aplicação estará disponível em `http://localhost:8000`

## 📁 Estrutura do Projeto

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

## 🎯 Como Organizar Novas Páginas ou Seções

### 1. Criando um Novo Módulo

1. **Crie a estrutura do módulo**:

```bash
mkdir -p app/modules/novo_modulo/{models,repositories,routes,services,validators}
```

2. **Implemente os arquivos básicos**:

   - `models/`: Classes de dados
   - `repositories/`: Acesso a dados
   - `routes/`: Endpoints da API
   - `services/`: Lógica de negócio
   - `validators/`: Validação de dados

3. **Registre o blueprint** em `app/__init__.py`:

```python
from app.modules.novo_modulo.routes import novo_modulo_bp
app.register_blueprint(novo_modulo_bp, url_prefix="/api/novo-modulo")
```

### 2. Criando Novas Páginas

1. **Adicione a rota** no módulo apropriado
2. **Crie o template** em `app/templates/`
3. **Adicione JavaScript** se necessário em `components/`

### 3. Funcionalidades de Documentos

#### Edição de Documentos (Admin)

A Wiki Veloz agora inclui funcionalidade completa de edição de documentos para usuários com perfil Admin:

- **Acesso**: Apenas usuários Admin podem editar documentos
- **Campos editáveis**: Título, descrição, categoria
- **Campos não editáveis**: Autor (mantido para histórico)
- **Upload opcional**: Substituição de arquivo PDF/PNG/JPG
- **Versionamento**: Controle automático de versões
- **Histórico**: Rastreamento de alterações e quem editou

**Como usar**:

1. Faça login como usuário Admin
2. Acesse a lista de documentos
3. Clique no botão "Editar" (ícone de lápis) ao lado do documento
4. Modifique os campos desejados
5. Opcionalmente, substitua o arquivo
6. Clique em "Salvar Alterações"

**Recursos técnicos**:

- Formulário responsivo com validação
- Preview do arquivo atual
- Controle de versão automático
- Log de atividades de edição
- Interface dark mode compatível

### 4. Padrões de Código

#### Python (Flask)

```python
@app.route('/api/endpoint', methods=['GET'])
@login_required
def endpoint_name():
    try:
        result = service.method()
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
```

#### JavaScript (Frontend)

```javascript
class ApiClient {
  static async request(endpoint, options = {}) {
    try {
      const response = await fetch(`/api/${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }
}
```

## 🚀 Como Fazer Deploy

### Heroku

```bash
# Configure o Heroku CLI
heroku create wiki-veloz-fibra
heroku config:set FLASK_ENV=production
git push heroku main
```

### Railway

```bash
# Conecte seu repositório ao Railway
# Configure as variáveis de ambiente no dashboard
# O deploy será automático
```

### Docker

```bash
# Build da imagem
docker build -t wiki-veloz .

# Executar container
docker run -p 8000:8000 wiki-veloz
```

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar testes específicos
python -m pytest tests/test_auth.py

# Com cobertura
python -m pytest --cov=app tests/
```

## 📊 Comandos Úteis

```bash
# Desenvolvimento
npm run dev              # Rodar aplicação
npm run test             # Executar testes
npm run format           # Formatar código
npm run lint             # Linting
npm run build:css        # Compilar CSS

# Produção
npm run build:css:prod   # CSS otimizado
python app.py            # Rodar aplicação
```

## 🔧 Configurações Importantes

### Variáveis de Ambiente

```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key
GOOGLE_DRIVE_CREDENTIALS=path/to/credentials.json
UPLOAD_FOLDER=app/static/uploads
```

### Google Drive API

1. Crie um projeto no Google Cloud Console
2. Ative a Google Drive API
3. Crie uma service account
4. Baixe as credenciais JSON
5. Configure o arquivo de credenciais

## 📚 Documentação

- [Guia de Analytics](ANALYTICS_GUIDE.md)
- [Sistema de Backup](SISTEMA_BACKUP.md)
- [Sistema de Notificações](SISTEMA_NOTIFICACOES.md)
- [Sistema de PDFs](SISTEMA_PDFS.md)
- [Credenciais Google Drive](CREDENCIAIS_GOOGLE_DRIVE.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Matheus Gallina**

- Email: matheus@velozfibra.com
- GitHub: [@mathuesgallina](https://github.com/mathuesgallina)

## 🙏 Agradecimentos

- Equipe Veloz Fibra
- Comunidade Flask
- Contribuidores do projeto

---

**Wiki Veloz Fibra** - Transformando a documentação corporativa em uma experiência colaborativa e eficiente.
