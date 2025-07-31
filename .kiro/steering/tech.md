# Stack Tecnológico & Decisões - CDD v2.0

## Arquitetura

### Pattern

**Monolithic Architecture** com separação clara de responsabilidades, evoluindo para **Microservices** conforme escala.

### Separation of Concerns

- **Presentation Layer**: Flask templates, HTML/CSS/JS, Tailwind CSS
- **Business Layer**: Python services, business logic, validation
- **Data Layer**: JSON files, Google Drive API, backup systems
- **Integration Layer**: Google Drive API, external services

## Stack Principal (com Versões e Justificativas)

### Backend

- **Framework**: **Flask 2.3+** - Simplicidade, flexibilidade, rápido desenvolvimento
- **Language**: **Python 3.11+** - Legibilidade, vasto ecossistema, excelente para prototipagem
- **Database**: **JSON files** - Simplicidade para MVP, fácil backup e versionamento
- **Authentication**: **Session-based** - Simples e efetivo para aplicação atual
- **File Storage**: **Google Drive API** - Backup automático, confiabilidade, integração nativa

### Frontend

- **Framework**: **Vanilla JavaScript** - Simplicidade, performance, sem overhead
- **Styling**: **Tailwind CSS 3.3+** - Utility-first, rapid development, consistent design
- **Build Tool**: **None (CDN)** - Simplicidade para MVP
- **State Management**: **DOM manipulation** - Simples para aplicação atual
- **Testing**: **Manual testing** - Adequado para MVP

### DevOps & Infrastructure

- **Containerization**: **Docker + Docker Compose** - Portabilidade, consistência
- **Deployment**: **Heroku** - Simplicidade, integração Git, auto-scaling
- **CI/CD**: **GitHub Actions** - Integração nativa, automatização
- **Monitoring**: **Heroku logs** - Built-in monitoring
- **Backup**: **Google Drive API** - Automatizado, confiável

## Comandos Essenciais (Automatizados)

### Development

```bash
# Instalar dependências
pip install -r requirements.txt
npm install

# Desenvolvimento local
python app.py              # Backend (port 5000)
# Frontend: Abrir templates/ no navegador

# Testes
python -m pytest tests/    # Run all tests
python -m pytest tests/ -v # Verbose mode
python -m pytest tests/ -k "test_name" # Specific test

# Linting & Formatting
python -m flake8 .         # PEP8 check
python -m black .          # Code formatting
python -m isort .          # Import sorting

# CDD Automation
npm run scan               # Scan tasks
npm run status             # Check progress
npm run complete           # Mark task complete
npm run watch              # Monitor progress
npm run health             # Project health
```

### Production

```bash
# Build Docker image
docker build -t wiki-veloz .

# Run with Docker Compose
docker-compose up -d

# Deploy to Heroku
git push heroku main

# Check logs
heroku logs --tail
```

## Decisões Técnicas (com Trade-offs)

| Decisão      | Alternativas                 | Motivo da Escolha                  | Trade-offs                  |
| ------------ | ---------------------------- | ---------------------------------- | --------------------------- |
| Flask        | Django, FastAPI              | Simplicidade + flexibilidade       | Menos features built-in     |
| Python       | Node.js, Go                  | Legibilidade + ecossistema         | Performance vs simplicidade |
| JSON files   | PostgreSQL, MongoDB          | Simplicidade para MVP              | Escalabilidade limitada     |
| Google Drive | AWS S3, Local storage        | Backup automático + confiabilidade | Vendor lock-in              |
| Tailwind CSS | Bootstrap, Styled-components | Rapidez + consistência             | Bundle size                 |
| Vanilla JS   | React, Vue                   | Simplicidade + performance         | Menos reutilização          |
| Heroku       | AWS, DigitalOcean            | Simplicidade + integração          | Custo vs conveniência       |

## Performance Targets

### Backend

- **Response Time**: < 500ms (95th percentile)
- **Throughput**: > 100 req/sec
- **Uptime**: > 99.5%
- **Memory Usage**: < 512MB

### Frontend

- **First Contentful Paint**: < 1.5s
- **Bundle Size**: < 100KB (gzipped)
- **Lighthouse Score**: > 85

### Database

- **Query Time**: < 100ms
- **Backup Time**: < 5 minutes
- **Recovery Time**: < 10 minutes

## Security Considerations

### Authentication & Authorization

- **Session management**: Flask sessions com secret key
- **Password policy**: 8+ chars, complexity required
- **Rate limiting**: 100 req/min per IP
- **CSRF protection**: Flask-WTF CSRF tokens

### Data Protection

- **Input validation**: Flask-WTF forms
- **File upload security**: Whitelist de extensões
- **Google Drive integration**: OAuth2 com escopo limitado
- **Backup encryption**: Google Drive encryption

### Infrastructure Security

- **HTTPS**: Heroku SSL automático
- **Environment variables**: Secrets em variáveis de ambiente
- **Dependency scanning**: bandit para análise de segurança
- **Regular updates**: Dependências atualizadas mensalmente

## Arquitetura de Dados

### Estrutura JSON

```json
{
  "users": [
    {
      "id": "uuid",
      "username": "string",
      "email": "string",
      "password_hash": "string",
      "role": "admin|user",
      "created_at": "timestamp",
      "last_login": "timestamp"
    }
  ],
  "pages": [
    {
      "id": "uuid",
      "title": "string",
      "content": "markdown",
      "author_id": "uuid",
      "created_at": "timestamp",
      "updated_at": "timestamp",
      "version": "number"
    }
  ],
  "pdfs": [
    {
      "id": "uuid",
      "filename": "string",
      "google_drive_id": "string",
      "uploaded_by": "uuid",
      "uploaded_at": "timestamp",
      "size": "number"
    }
  ]
}
```

### Backup Strategy

- **Automated**: Google Drive sync a cada 6 horas
- **Manual**: Backup via admin interface
- **Versioning**: Mantém últimas 10 versões
- **Recovery**: Restore via Google Drive API

## Integrações

### Google Drive API

```python
# Configuração
GOOGLE_DRIVE_CREDENTIALS = {
    "type": "service_account",
    "project_id": "wiki-veloz",
    "private_key_id": "...",
    "private_key": "...",
    "client_email": "...",
    "client_id": "...",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "...",
    "client_x509_cert_url": "..."
}

# Escopos necessários
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]
```

### Funcionalidades de Integração

- **Upload automático**: PDFs enviados para Google Drive
- **Sincronização**: Backup automático de dados JSON
- **Versionamento**: Histórico de versões no Drive
- **Recuperação**: Restore de backups via API

## Estratégia de Escalabilidade

### Fase 1: MVP (Atual)

- **Arquitetura**: Monolítica com Flask
- **Database**: JSON files
- **Deployment**: Heroku
- **Usuários**: 50-100 usuários

### Fase 2: Crescimento

- **Database**: PostgreSQL (migração gradual)
- **Caching**: Redis para sessões
- **CDN**: CloudFlare para assets
- **Usuários**: 500-1000 usuários

### Fase 3: Escala

- **Microservices**: Separação por domínio
- **Message Queue**: Celery + Redis
- **Monitoring**: Sentry + Analytics
- **Usuários**: 5000+ usuários

## Padrões de Código

### Python (Flask)

```python
# Estrutura de rota
@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
    try:
        users = user_service.get_all_users()
        return jsonify({
            'success': True,
            'data': users
        }), 200
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

# Service pattern
class UserService:
    def __init__(self):
        self.data_file = 'data/users.json'

    def get_all_users(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        return data.get('users', [])
```

### JavaScript (Frontend)

```javascript
// API client
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

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }
}

// Usage
const users = await ApiClient.request('users');
```

## Testes

### Estratégia de Testes

- **Unit tests**: pytest para lógica de negócio
- **Integration tests**: Testes de API endpoints
- **Manual testing**: Interface de usuário
- **Security tests**: bandit para análise de segurança

### Exemplo de Teste

```python
# tests/test_user_service.py
import pytest
from services.user_service import UserService

class TestUserService:
    def setup_method(self):
        self.user_service = UserService()

    def test_create_user(self):
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }

        user = self.user_service.create_user(user_data)

        assert user['username'] == user_data['username']
        assert user['email'] == user_data['email']
        assert 'password' not in user
```

## Monitoring e Logging

### Logging Strategy

```python
import logging

# Configuração
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Uso
logger.info('User created successfully', extra={'user_id': user_id})
logger.error('Failed to upload file', exc_info=True)
```

### Métricas Importantes

- **Response time**: Tempo médio de resposta
- **Error rate**: Taxa de erros por endpoint
- **User activity**: Usuários ativos por dia
- **File uploads**: Uploads por dia
- **Backup success**: Taxa de sucesso de backup

## Deployment

### Heroku Configuration

```yaml
# Procfile
web: python app.py

# runtime.txt
python-3.11.7

# requirements.txt
Flask==2.3.3
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
```

### Environment Variables

```bash
# .env.example
FLASK_ENV=development
SECRET_KEY=your-secret-key
GOOGLE_DRIVE_CREDENTIALS={"type":"service_account",...}
GOOGLE_DRIVE_FOLDER_ID=your-folder-id
```

## Riscos Técnicos e Mitigações

### Riscos Identificados

- **Google Drive API limits**: Rate limiting implementado
- **JSON file corruption**: Backup automático e validação
- **Memory leaks**: Monitoramento e garbage collection
- **Security vulnerabilities**: Dependências atualizadas regularmente

### Mitigações

- **Rate limiting**: Implementado no Google Drive client
- **Data validation**: Schemas JSON para validação
- **Error handling**: Try/catch em todas as operações críticas
- **Monitoring**: Logs estruturados e alertas
