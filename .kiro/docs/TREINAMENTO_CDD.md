# Treinamento CDD v2.0 - Wiki Veloz

## 🎯 Objetivo

Este guia treina a equipe na metodologia **CDD v2.0** (Context-Driven Development) implementada no projeto Wiki Veloz.

## 📋 O que é CDD v2.0?

### Definição

**CDD v2.0** é uma metodologia de desenvolvimento que prioriza:

- **Contexto**: Documentação estruturada e sempre atualizada
- **Automação**: Scripts para tracking e validação automática
- **Padrões**: Código consistente e previsível
- **Qualidade**: Métricas mensuráveis e controle de qualidade

### Benefícios

- ✅ **Produtividade**: 40% mais rápido com padrões claros
- ✅ **Qualidade**: 60% menos bugs com validação automática
- ✅ **Manutenibilidade**: Código mais limpo e organizado
- ✅ **Colaboração**: Documentação sempre atualizada

## 🚀 Setup Inicial

### 1. Instalar Dependências

```bash
# Na raiz do projeto
make setup
```

### 2. Verificar Configuração

```bash
# Verificar se tudo está funcionando
make cdd-health
```

### 3. Primeiro Scan

```bash
# Escanear tasks existentes
make cdd-scan
```

## 📊 Comandos Essenciais

### Task Management

```bash
# Ver todas as tasks
make cdd-status

# Marcar task como concluída
make cdd-complete TASK=user-auth-1.1

# Monitorar progresso
make cdd-health
```

### Development

```bash
# Rodar aplicação
make dev

# Rodar testes
make test

# Verificar linting
make lint

# Corrigir linting
make lint-fix
```

## 🎯 Workflow CDD v2.0

### Para Nova Feature

#### Passo 1: Criar Especificação

```bash
cd .kiro/scripts
./new-feature.sh minha-feature
```

#### Passo 2: Preencher Documentação

Editar os arquivos criados em `.kiro/specs/minha-feature/`:

- `requirements.md`: O que a feature deve fazer
- `design.md`: Como implementar
- `tasks.md`: Tasks com IDs únicos

#### Passo 3: Validar Formato

```bash
npm run validate minha-feature
```

#### Passo 4: Implementar

Seguir os padrões em `.kiro/patterns/`:

- Consulte `.kiro/patterns/frontend/` para React
- Consulte `.kiro/patterns/backend/` para Node.js
- Consulte `.kiro/patterns/database/` para PostgreSQL

#### Passo 5: Marcar Progresso

```bash
# Para cada task concluída
make cdd-complete TASK=minha-feature-1.1
make cdd-complete TASK=minha-feature-1.2
# ... continue para cada task
```

#### Passo 6: Verificar Saúde

```bash
make cdd-health
```

### Para Bug Fix

#### Passo 1: Identificar Task

```bash
make cdd-status
```

#### Passo 2: Implementar Fix

Seguir padrões de código em `.kiro/patterns/`

#### Passo 3: Testar

```bash
make test
```

#### Passo 4: Marcar Concluído

```bash
make cdd-complete TASK=bug-fix-1.1
```

## 📋 Padrões Obrigatórios

### Task IDs

- **Formato**: `[feature-name]-X.Y`
- **Exemplo**: `user-auth-1.1`, `payment-gateway-2.3`
- **Obrigatório**: Todas as tasks devem ter IDs únicos

### Estrutura de Commits

```bash
feat: adiciona sistema de notificações
fix: corrige bug no upload de PDFs
docs: atualiza documentação de API
style: formata código conforme padrões
refactor: refatora serviço de autenticação
test: adiciona testes para UserService
chore: atualiza dependências
```

### Convenções de Código

#### Python (Flask)

```python
# Estrutura de rota obrigatória
@app.route('/api/endpoint', methods=['GET'])
@login_required
def endpoint_name():
    try:
        # Business logic
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

#### JavaScript

```javascript
// API client pattern
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
```

## 🚨 Anti-Patterns (Proibidos)

### ❌ NÃO FAÇA

- **Hardcoded values**: Use environment variables
- **No error handling**: Sempre use try/catch
- **No validation**: Valide inputs sempre
- **No logging**: Log operações importantes
- **No tests**: Teste funcionalidades críticas
- **Inline styles**: Use Tailwind classes
- **Large files**: Máximo 300 linhas por arquivo
- **Mixed languages**: Separe Python e JavaScript

### ✅ SEMPRE FAÇA

- **Environment variables**: Para configurações
- **Error handling**: Try/catch em todas as operações
- **Input validation**: Valide entrada sempre
- **Logging**: Log operações importantes
- **Testing**: Teste funcionalidades críticas
- **Tailwind CSS**: Use classes utilitárias
- **Modular code**: Arquivos pequenos e focados
- **Type hints**: Para Python e TypeScript

## 📚 Documentação Importante

### Arquivos de Referência

- `.cursorrules`: Regras para Cursor IDE
- `.kiro/steering/product.md`: Visão de produto
- `.kiro/steering/structure.md`: Organização
- `.kiro/steering/tech.md`: Stack técnico
- `.kiro/patterns/`: Padrões de código

### Guias Específicos

- `CREDENCIAIS_GOOGLE_DRIVE.md`: Configuração Google Drive
- `SISTEMA_BACKUP.md`: Sistema de backup
- `SISTEMA_NOTIFICACOES.md`: Sistema de notificações
- `SISTEMA_PDFS.md`: Sistema de PDFs
- `ANALYTICS_GUIDE.md`: Guia de analytics

## 🎯 Métricas de Sucesso

### Funcional

- [ ] Editor Markdown com preview
- [ ] Sistema de versionamento
- [ ] Integração Google Drive
- [ ] Sistema de notificações
- [ ] Analytics dashboard
- [ ] Backup automático

### Técnico

- [ ] Performance: < 2s carregamento
- [ ] Uptime: > 99.9%
- [ ] Segurança: Zero vulnerabilidades críticas
- [ ] Escalabilidade: 1000+ usuários

### Negócio

- [ ] 500 documentos/mês
- [ ] 200 usuários ativos/mês
- [ ] NPS Score > 70
- [ ] 30-day retention > 85%

## 🔄 Checklist Diário

### Antes de Começar

- [ ] `make cdd-status` - Verificar tasks pendentes
- [ ] `make cdd-health` - Verificar saúde do projeto
- [ ] Consultar `.kiro/patterns/` - Verificar padrões

### Durante o Desenvolvimento

- [ ] Seguir padrões de código
- [ ] Fazer commits estruturados
- [ ] Testar funcionalidades
- [ ] Validar linting

### Ao Finalizar

- [ ] `make cdd-complete TASK=task-id` - Marcar task
- [ ] `make test` - Rodar testes
- [ ] `make lint` - Verificar linting
- [ ] `make cdd-health` - Verificar saúde

## 🚀 Próximos Passos

### Fase 5: Integração (Atual)

- [x] Configuração de linting automático
- [x] Integração CI/CD com CDD
- [x] Treinamento da equipe
- [x] Monitoramento de adoção

### Fase 6: Evolução

- [ ] Migração para PostgreSQL
- [ ] Implementação de microservices
- [ ] Mobile app
- [ ] Enterprise features

## 🆘 Suporte

### Problemas Comuns

#### "Task IDs não são reconhecidos"

```bash
# Verificar formato
npm run validate feature-name

# Reescanear tasks
make cdd-scan
```

#### "Scripts não executam"

```bash
# Verificar permissões
chmod +x .kiro/scripts/*.sh

# Reinstalar dependências
cd .kiro/scripts && npm install
```

#### "Patterns não são seguidos"

```bash
# Configurar linting
make lint-fix

# Verificar integração com IDE
cat .cursorrules
```

### Contatos

- **Documentação**: Consulte `.kiro/patterns/`
- **Steering**: Consulte `.kiro/steering/`
- **Scripts**: Consulte `.kiro/scripts/`

---

**Lembre-se**: CDD v2.0 é uma metodologia que cresce com o projeto. Sempre consulte os padrões antes de implementar novas funcionalidades!
