# Prompt: Gerador Automático de Estrutura CDD v2.0 Completa

## 🎯 Objetivo
Analise completamente o projeto atual e construa automaticamente toda a estrutura **Context-Driven Documentation (CDD) v2.0** seguindo a metodologia rigorosa com task tracking obrigatório, patterns automatizados e qualidade empresarial.

## 📋 Instruções Completas para IA

### FASE 1: ANÁLISE PROFUNDA DO PROJETO

Execute esta análise sistemática e abrangente:

#### 1. **📁 Estrutura Geral e Arquitetura**
```bash
# Explore recursivamente e mapeia completamente:
find . -type f -name "*.json" -o -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" | head -50
ls -la
cat package.json 2>/dev/null || cat requirements.txt 2>/dev/null || cat Gemfile 2>/dev/null
```

**Identifique e catalogue:**
- **Arquitetura**: Monorepo, microservices, monolith, micro-frontends
- **Estrutura**: Feature-based, layer-based, domain-driven design
- **Organização**: Convenções existentes, patterns implícitos
- **Entry points**: Main files, index files, app entry points
- **Build system**: Webpack, Vite, Turbo, esbuild, custom scripts

#### 2. **⚙️ Stack Tecnológico Completo**
```bash
# Analise TODOS os arquivos de configuração:
package.json          # Dependencies, scripts, engines
tsconfig.json         # TypeScript configuration
next.config.js        # Next.js specific
vite.config.js        # Vite specific
tailwind.config.js    # Styling configuration
prisma/schema.prisma  # Database schema
docker-compose.yml    # Container orchestration
.env.example          # Environment variables
```

**Extraia meticulosamente:**
- **Frontend**: React, Vue, Angular, Svelte + versions específicas
- **Backend**: Node.js, Express, NestJS, Fastify, Python, Go + versions
- **Database**: PostgreSQL, MongoDB, MySQL, Redis, SQLite + ORMs
- **Testing**: Jest, Vitest, Cypress, Playwright, Testing Library
- **Build Tools**: Vite, Webpack, Rollup, Parcel, esbuild
- **Styling**: Tailwind, Styled Components, CSS Modules, Sass
- **State Management**: Redux, Zustand, Context, MobX, SWR
- **DevOps**: Docker, Kubernetes, CI/CD, deployment targets
- **Monitoring**: Sentry, Analytics, error tracking, APM tools

#### 3. **🏗️ Arquitetura de Código e Patterns**
```bash
# Analise estrutura de código profundamente:
src/                  # Main source directory patterns
components/           # Component organization patterns
services/             # Service layer patterns
utils/                # Utility organization patterns
hooks/                # Custom hooks patterns (if React)
lib/                  # Library and shared code patterns
api/ ou pages/api/    # API routes patterns
```

**Identifique patterns implícitos:**
- **Component structure**: Functional vs class, hooks usage, prop patterns
- **State management**: How state flows, where stored, update patterns
- **Data fetching**: API integration patterns, caching, error handling
- **Routing**: How navigation works, protected routes, nested routes
- **Authentication**: How auth is handled, JWT, sessions, protection
- **Error handling**: How errors are caught, displayed, logged
- **Performance**: Code splitting, lazy loading, optimization patterns

#### 4. **🎯 Propósito e Funcionalidades de Negócio**
```bash
# Analise para deduzir contexto de negócio:
README.md             # Existing documentation
src/components/       # Component names revealing features
src/pages/            # Page structure revealing user journeys
src/features/         # Feature modules
api/ routes           # Backend endpoints revealing business logic
database schemas      # Data models revealing domain
```

**Deduza sistematicamente:**
- **Domínio de negócio**: E-commerce, fintech, healthcare, SaaS, etc.
- **Usuários alvo**: End users, admins, developers, businesses
- **Core features**: Primary functionalities by analyzing components/routes
- **Business workflows**: User journeys by analyzing page flows
- **Data models**: Business entities by analyzing schemas/types
- **Integration points**: External APIs, services, webhooks
- **Compliance needs**: GDPR, HIPAA, PCI, industry-specific requirements

#### 5. **🔧 Configurações e DevOps Environment**
```bash
# Examine ambiente completo:
.env.example          # Environment variables
docker-compose.yml    # Container setup
Dockerfile           # Container configuration
.github/workflows/   # CI/CD pipelines
vercel.json          # Deployment configuration
netlify.toml         # Netlify specific
.gitignore           # Ignored files patterns
```

**Mapie ambiente:**
- **Development**: Local setup, dependencies, required services
- **Testing**: Test environments, CI/CD setup, quality gates
- **Staging**: Pre-production environments, testing procedures
- **Production**: Deployment targets, scaling, monitoring
- **Monitoring**: Error tracking, analytics, performance monitoring
- **Security**: Security headers, authentication, data protection

### FASE 2: CONSTRUÇÃO DA ESTRUTURA CDD v2.0 COMPLETA

Execute sistematicamente:

#### Passo 1: Criar Estrutura de Diretórios Robusta
```bash
# Crie exatamente esta estrutura CDD v2.0:
.kiro/
├── steering/                    # Tier 1: Strategic Authority
│   ├── product.md              # Business context and vision
│   ├── structure.md            # Code organization philosophy
│   └── tech.md                 # Technology stack decisions
├── patterns/                   # Tier 2: Technical Standards
│   ├── README.md               # Patterns overview and index
│   ├── conventions.md          # Naming and code conventions
│   ├── architecture.md         # SOLID principles and design patterns
│   ├── typescript.md           # TypeScript strict mode patterns
│   ├── security.md             # OWASP guidelines and security headers
│   ├── performance.md          # Core Web Vitals and optimization
│   ├── testing.md              # Testing strategies and coverage
│   ├── error-handling.md       # Error handling patterns
│   ├── accessibility.md        # WCAG 2.1 AA compliance
│   ├── frontend/               # Frontend-specific patterns
│   │   ├── README.md
│   │   ├── [framework].md      # React, Vue, Angular patterns
│   │   ├── components.md       # Component design patterns
│   │   ├── state-management.md # State patterns
│   │   ├── styling.md          # CSS/styling patterns
│   │   └── forms.md            # Form validation patterns
│   ├── backend/                # Backend-specific patterns
│   │   ├── README.md
│   │   ├── [framework].md      # Node.js, Express patterns
│   │   ├── api-design.md       # REST/GraphQL API patterns
│   │   ├── middleware.md       # Middleware patterns
│   │   ├── authentication.md   # Auth patterns
│   │   └── caching.md          # Cache strategies
│   ├── database/               # Database patterns
│   │   ├── README.md
│   │   ├── [database].md       # PostgreSQL, MongoDB patterns
│   │   ├── migrations.md       # Migration patterns
│   │   ├── indexing.md         # Index optimization
│   │   └── transactions.md     # Transaction patterns
│   ├── examples/               # Copy-paste ready templates
│   │   ├── README.md
│   │   ├── components/         # Component templates
│   │   ├── services/           # Service templates
│   │   ├── tests/              # Test templates
│   │   └── configs/            # Configuration templates
│   ├── linting/                # Automation configuration
│   │   ├── README.md
│   │   ├── .eslintrc.custom.js # ESLint configuration
│   │   ├── .prettierrc.custom.js # Prettier configuration
│   │   ├── tsconfig.patterns.json # TypeScript strict config
│   │   └── .husky/             # Git hooks configuration
│   └── CHANGELOG.md            # Pattern versioning
├── specs/                      # Tier 3: Feature Implementation
│   └── _template/              # Template for new features
│       ├── requirements.md     # User stories template
│       ├── design.md           # Technical design template
│       └── tasks.md            # Task tracking template
├── scripts/                    # Tier 4: Automation Engine
│   ├── package.json            # NPM scripts for task management
│   ├── task-manager.js         # Core task tracking system
│   ├── check-patterns.js       # Pattern compliance validation
│   ├── validate-tasks.js       # Task format validation
│   ├── backup-tasks.sh         # Backup and recovery
│   ├── metrics-completeness.sh # Progress metrics
│   ├── cleanup-dead-code.sh    # Housekeeping automation
│   └── interactive-cli.sh      # User-friendly interface
└── docs/                       # Tier 5: Process Documentation
    ├── README.md               # CDD v2.0 introduction
    ├── INDEX.md                # Navigation and quick start
    ├── implementation-guide.md # Complete setup guide
    ├── workflow-completo.md    # End-to-end workflow
    ├── principles-and-best-practices.md # Fundamental principles
    └── troubleshooting.md      # Common issues and solutions
```

#### Passo 2: Gerar product.md Baseado na Análise
```markdown
# [NOME_PROJETO] - Visão de Produto

## 🎯 Contexto de Negócio

### Problema que Resolve
**Domínio**: [DEDUZIR DO CÓDIGO: E-commerce, Fintech, Healthcare, SaaS, etc.]

**Context**: [BASEADO NA ANÁLISE DE COMPONENTES E FUNCIONALIDADES]
[Exemplo: Sistema de gestão de saúde com IA para tracking de métricas pessoais, 
insights automatizados e gamificação para motivar hábitos saudáveis]

**Pain Points Identificados**:
- **Primary**: [DEDUZIR DA FUNCIONALIDADE PRINCIPAL]
- **Secondary**: [PROBLEMAS IDENTIFICADOS PELOS COMPONENTES]
- **Impact**: [POR QUE É CRÍTICO RESOLVER - DEDUZIR DO CONTEXTO]

### Target Users
**Usuário Primário**: [DEDUZIR DOS COMPONENTES E FLUXOS]
- Demographics: [BASEADO NAS FEATURES DE USER MANAGEMENT]
- Needs: [INFERIR DAS FUNCIONALIDADES PRINCIPAIS]
- Pain Points: [DEDUZIR DOS FLUXOS DE UX]

**Usuários Secundários**: [OUTROS ROLES IDENTIFICADOS]

## 💡 Solução Proposta

### Value Proposition
[UMA FRASE QUE RESUME O VALOR - BASEADA NA ANÁLISE DE FEATURES]

### Core Features
[EXTRAIR DAS 3-5 FUNCIONALIDADES PRINCIPAIS IDENTIFICADAS]
1. **[FEATURE 1]**: [DESCRIÇÃO BASEADA NO CÓDIGO]
2. **[FEATURE 2]**: [DESCRIÇÃO BASEADA NO CÓDIGO]
3. **[FEATURE 3]**: [DESCRIÇÃO BASEADA NO CÓDIGO]

### Differentials
[O QUE TORNA ÚNICO - BASEADO NA IMPLEMENTAÇÃO TÉCNICA]
- **[DIFFERENTIAL 1]**: [JUSTIFICATIVA TÉCNICA]
- **[DIFFERENTIAL 2]**: [BASEADO EM PATTERNS IDENTIFICADOS]

## 📊 Objetivos de Negócio

### Success Metrics
[MÉTRICAS DEDUZIDAS DO TIPO DE APLICAÇÃO]
- **User Engagement**: [ESPECÍFICO PARA O DOMÍNIO]
- **Performance**: [BASEADO EM REQUIREMENTS TÉCNICOS]
- **Business Impact**: [DEDUZIR DO CONTEXTO DE NEGÓCIO]

### Technical Requirements
[BASEADO NA ANÁLISE DE STACK E PERFORMANCE]
- **Performance**: [TARGETS ESPECÍFICOS - Core Web Vitals, etc.]
- **Scalability**: [BASEADO NA ARQUITETURA IDENTIFICADA]
- **Security**: [REQUIREMENTS ESPECÍFICOS DO DOMÍNIO]
- **Compliance**: [BASEADO NO SETOR - GDPR, HIPAA, etc.]

## 🗺️ Progressive Strategy

### Phase 1: Foundation [ATUAL]
[FEATURES JÁ IMPLEMENTADAS IDENTIFICADAS]

### Phase 2: Enhancement [PRÓXIMA]
[FEATURES EM DESENVOLVIMENTO OU PLANEJADAS]

### Phase 3: Scale [FUTURO]
[BASEADO EM PATTERNS DE ESCALABILIDADE IDENTIFICADOS]

---
**Version**: 2.0.0
**Last Updated**: [DATA_ATUAL]
**Status**: ✅ Generated from codebase analysis
```

#### Passo 3: Gerar structure.md da Análise
```markdown
# [NOME_PROJETO] - Estrutura e Organização

## 🏗️ Filosofia Arquitetural

### Approach Identificado
**Pattern**: [FEATURE-BASED | LAYER-BASED | DOMAIN-DRIVEN baseado na análise]

**Philosophy**: [EXTRAIR DA ESTRUTURA ATUAL]
- **[PRINCÍPIO 1]**: [BASEADO NA ORGANIZAÇÃO DE PASTAS]
- **[PRINCÍPIO 2]**: [DEDUZIR DOS PATTERNS DE IMPORT]
- **[PRINCÍPIO 3]**: [INFERIR DA ESTRUTURA DE COMPONENTES]

### Separation of Concerns
[BASEADO NA ANÁLISE DE ESTRUTURA]
```
[MOSTRAR ESTRUTURA ATUAL MAPEADA]
├── [PASTA 1]/     # [FUNÇÃO IDENTIFICADA]
├── [PASTA 2]/     # [RESPONSABILIDADE DEDUZIDA]
└── [PASTA 3]/     # [PROPÓSITO INFERIDO]
```

## 📁 Estrutura de Diretórios

### Frontend Structure
[MAPEAR ESTRUTURA FRONTEND ATUAL]
```
[FRONTEND_DIR]/
├── [COMPONENTS_DIR]/    # [PADRÃO DE COMPONENTES IDENTIFICADO]
├── [PAGES_DIR]/         # [ESTRUTURA DE ROUTING IDENTIFICADA]
├── [HOOKS_DIR]/         # [CUSTOM HOOKS PATTERNS SE REACT]
├── [SERVICES_DIR]/      # [CAMADA DE SERVIÇOS IDENTIFICADA]
└── [UTILS_DIR]/         # [UTILITIES ORGANIZATION]
```

### Backend Structure (se aplicável)
[MAPEAR ESTRUTURA BACKEND SE EXISTIR]
```
[BACKEND_DIR]/
├── [API_DIR]/           # [API ROUTES PATTERN]
├── [CONTROLLERS_DIR]/   # [CONTROLLER ORGANIZATION]
├── [MODELS_DIR]/        # [DATA MODELS STRUCTURE]
└── [MIDDLEWARE_DIR]/    # [MIDDLEWARE PATTERNS]
```

## 🔧 Convenções Identificadas

### File Naming
[EXTRAIR PATTERNS DE NOMENCLATURA ATUAIS]
- **Components**: [PADRÃO IDENTIFICADO - PascalCase.tsx]
- **Utilities**: [PADRÃO IDENTIFICADO - camelCase.ts]
- **Constants**: [PADRÃO IDENTIFICADO - UPPER_CASE.ts]
- **Tests**: [PADRÃO IDENTIFICADO - .test.ts/.spec.ts]

### Import Strategies
[ANALISAR PATTERNS DE IMPORT EXISTENTES]
```typescript
// [PADRÃO IDENTIFICADO]
import [EXTERNAL_PATTERN]
import [INTERNAL_PATTERN]
import [RELATIVE_PATTERN]
```

### Path Mapping
[EXTRAIR DO tsconfig.json OU CRIAR RECOMENDADO]
```typescript
"paths": {
  "@/*": ["./src/*"],
  // [OUTROS MAPPINGS IDENTIFICADOS OU RECOMENDADOS]
}
```

## ⚡ Performance Considerations

### Code Splitting
[IDENTIFICAR ESTRATÉGIAS ATUAIS OU RECOMENDAR]
- **[ESTRATÉGIA 1]**: [BASEADA NO BUILD SETUP]
- **[ESTRATÉGIA 2]**: [BASEADA NO FRAMEWORK]

### Bundle Optimization
[BASEADO NO BUILD TOOL IDENTIFICADO]
- **Tool**: [WEBPACK | VITE | ROLLUP | ETC]
- **Strategy**: [INFERIR DO SETUP ATUAL]

---
**Generated from**: Codebase structure analysis
**Architecture**: [AUTO_DETECTED]
**Framework**: [FRAMEWORK_PRINCIPAL_IDENTIFICADO]
```

#### Passo 4: Gerar tech.md da Stack Identificada
```markdown
# [NOME_PROJETO] - Stack Tecnológico

## 🎯 Decisões Técnicas

### Core Technologies
[EXTRAIR EXATAMENTE DO PACKAGE.JSON E CONFIGS]

#### Frontend
- **Framework**: [REACT | VUE | ANGULAR] v[VERSION]
- **Language**: TypeScript v[VERSION] (strict mode)
- **Build Tool**: [VITE | WEBPACK | NEXT.JS] v[VERSION]
- **Styling**: [TAILWIND | STYLED-COMPONENTS | CSS MODULES] v[VERSION]
- **State Management**: [REDUX | ZUSTAND | CONTEXT] v[VERSION]
- **Routing**: [NEXT_ROUTER | REACT_ROUTER | VUE_ROUTER] v[VERSION]

#### Backend (se aplicável)
- **Runtime**: Node.js v[VERSION_IDENTIFICADA]
- **Framework**: [EXPRESS | NESTJS | FASTIFY] v[VERSION]
- **Language**: TypeScript v[VERSION]
- **Database**: [POSTGRESQL | MONGODB | MYSQL] v[VERSION]
- **ORM**: [PRISMA | TYPEORM | MONGOOSE] v[VERSION]
- **Authentication**: [JWT | PASSPORT | NEXT_AUTH] v[VERSION]

#### DevOps & Tools
- **Package Manager**: [NPM | YARN | PNPM] v[VERSION]
- **Testing**: [JEST | VITEST | CYPRESS] v[VERSION]
- **Linting**: ESLint v[VERSION] + Prettier v[VERSION]
- **CI/CD**: [GITHUB_ACTIONS | VERCEL | NETLIFY]
- **Monitoring**: [SENTRY | DATADOG | VERCEL_ANALYTICS]

## 🚀 Development Setup

### Prerequisites
[BASEADO NO ENGINES DO PACKAGE.JSON]
```bash
node >= [VERSION_MINIMUM]
npm >= [VERSION_MINIMUM]
# [OUTROS REQUIREMENTS IDENTIFICADOS]
```

### Installation
[EXTRAIR DOS SCRIPTS DO PACKAGE.JSON]
```bash
# [SETUP_COMMANDS_IDENTIFICADOS]
npm install
# [OUTROS_COMANDOS_SETUP]
```

### Development Commands
[EXTRAIR TODOS OS SCRIPTS DO PACKAGE.JSON]
```bash
npm run dev          # [COMANDO_IDENTIFICADO]
npm run build        # [COMANDO_IDENTIFICADO]
npm run test         # [COMANDO_IDENTIFICADO]
npm run lint         # [COMANDO_IDENTIFICADO]
# [OUTROS_SCRIPTS_IDENTIFICADOS]
```

## 🏗️ Architecture Decisions

### Frontend Choices
**[FRAMEWORK] escolhido porque**:
- [JUSTIFICAR BASEADO NO CONTEXTO DO PROJETO]
- [RAZÕES TÉCNICAS INFERIDAS]
- [BENEFÍCIOS PARA O DOMÍNIO ESPECÍFICO]

**TypeScript strict mode**:
- Zero tolerance para `any` types
- Explicit function return types
- Strict null checks enabled
- [OUTRAS_CONFIGS_STRICT_IDENTIFICADAS]

### Performance Strategy
[BASEADO NO BUILD SETUP E FRAMEWORK]
- **Code Splitting**: [ESTRATÉGIA_IDENTIFICADA]
- **Bundle Size**: Target <[SIZE_TARGET] gzipped
- **Core Web Vitals**: [TARGETS_ESPECÍFICOS]
- **Caching**: [ESTRATÉGIA_IDENTIFICADA]

### Security Approach
[BASEADO NO DOMÍNIO E DEPENDENCIES]
- **Authentication**: [MÉTODO_IDENTIFICADO]
- **Authorization**: [ESTRATÉGIA_IDENTIFICADA]
- **Data Protection**: [COMPLIANCE_REQUIREMENTS]
- **Security Headers**: [CONFIGURAÇÕES_IDENTIFICADAS]

## 🔄 LLM-First Development

### AI Integration Points
[PARA METODOLOGIA CDD v2.0]
- **Code Generation**: Templates em patterns/examples/
- **Pattern Enforcement**: ESLint rules automáticas
- **Documentation**: Context-driven approach
- **Quality Assurance**: Automated compliance checking

### Cursor IDE Optimization
[INTEGRAÇÃO COM .cursorrules]
- **Context Hierarchy**: steering → patterns → specs → code
- **Pattern Application**: Automatic application of established patterns
- **Task Tracking**: Integration with task ID system
- **Quality Gates**: Pre-commit validation automatic

---
**Stack Analysis Date**: [DATA_ATUAL]
**Total Dependencies**: [NÚMERO_TOTAL_DEPS]
**Framework Version**: [VERSÃO_PRINCIPAL]
**TypeScript**: ✅ Strict Mode Enabled
```

#### Passo 5: Gerar Patterns Completos da Stack
[EXECUTAR patterns-generator-prompt.md com stack identificada]

#### Passo 6: Gerar Scripts de Automação Funcionais
```javascript
// .kiro/scripts/task-manager.js
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

class TaskManager {
  constructor() {
    this.specsDir = path.join(__dirname, '../specs');
    this.statusFile = path.join(__dirname, 'tasks-status.json');
    this.loadStatus();
  }

  loadStatus() {
    try {
      this.status = JSON.parse(fs.readFileSync(this.statusFile, 'utf8'));
    } catch {
      this.status = { tasks: {}, lastUpdated: new Date().toISOString() };
    }
  }

  saveStatus() {
    this.status.lastUpdated = new Date().toISOString();
    fs.writeFileSync(this.statusFile, JSON.stringify(this.status, null, 2));
  }

  scan() {
    console.log('🔍 Scanning for tasks...');
    
    // [IMPLEMENTAÇÃO COMPLETA DO SISTEMA DE TRACKING]
    // [BASEADA NO FORMATO feature-name-X.Y]
    
    this.saveStatus();
    console.log('✅ Scan completed');
  }

  complete(taskId) {
    // [IMPLEMENTAÇÃO PARA MARCAR TASKS COMO CONCLUÍDAS]
    console.log(`✅ Task ${taskId} marked as completed`);
  }

  list(feature = null) {
    // [IMPLEMENTAÇÃO PARA LISTAR TASKS]
    console.log('📋 Task List:');
  }

  status() {
    // [IMPLEMENTAÇÃO PARA MOSTRAR STATUS GERAL]
    console.log('📊 Project Status:');
  }
}

// CLI interface
const command = process.argv[2];
const args = process.argv.slice(3);
const manager = new TaskManager();

switch (command) {
  case 'scan':
    manager.scan();
    break;
  case 'complete':
    manager.complete(args[0]);
    break;
  case 'list':
    manager.list(args[0]);
    break;
  case 'status':
    manager.status();
    break;
  default:
    console.log('Usage: node task-manager.js <scan|complete|list|status> [args]');
}
```

#### Passo 7: Gerar .cursorrules Otimizado
[EXECUTAR cursorrules-generator-prompt.md com análise completa]

### FASE 3: VALIDAÇÃO E QUALIDADE

#### Validação Automática da Estrutura
```bash
#!/bin/bash
# scripts/validate-cdd-structure.sh

echo "🔍 Validating CDD v2.0 structure..."

# Verificar estrutura obrigatória
required_dirs=(
  ".kiro/steering"
  ".kiro/patterns"
  ".kiro/specs"
  ".kiro/scripts"
  ".kiro/docs"
)

for dir in "${required_dirs[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "❌ Missing directory: $dir"
    exit 1
  fi
done

# Verificar arquivos obrigatórios
required_files=(
  ".kiro/steering/product.md"
  ".kiro/steering/structure.md"
  ".kiro/steering/tech.md"
  ".kiro/patterns/README.md"
  ".kiro/patterns/conventions.md"
  ".kiro/scripts/task-manager.js"
  ".kiro/scripts/package.json"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing file: $file"
    exit 1
  fi
done

# Verificar conteúdo gerado
if ! grep -q "CDD v2.0" .kiro/README.md; then
  echo "❌ README must reference CDD v2.0"
  exit 1
fi

echo "✅ CDD v2.0 structure validation passed!"
```

#### Métricas de Qualidade da Geração
```bash
# scripts/generation-quality-report.sh

echo "📊 CDD v2.0 Generation Quality Report"
echo "=================================="

# Análise de completude
total_files=$(find .kiro -name "*.md" -o -name "*.js" -o -name "*.sh" | wc -l)
echo "📁 Files generated: $total_files"

# Verificar customização (não deve ter placeholders)
placeholders=$(find .kiro -name "*.md" -exec grep -l "\[.*\]" {} \; | wc -l)
echo "🔧 Files with placeholders: $placeholders"

# Verificar especificidade tecnológica
if grep -q "React\|Vue\|Angular" .kiro/steering/tech.md; then
  echo "✅ Frontend technology identified and documented"
fi

if grep -q "Node.js\|Express\|NestJS" .kiro/steering/tech.md; then
  echo "✅ Backend technology identified and documented"
fi

# Score de qualidade
if [ $placeholders -eq 0 ]; then
  echo "🎯 Quality Score: 100% (no placeholders)"
else
  echo "⚠️  Quality Score: $((100 - placeholders * 10))% (placeholders need customization)"
fi
```

## 🎯 **Resultado**: Estrutura CDD v2.0 completa e funcional gerada automaticamente!

### ✅ **Entregáveis do Prompt:**
1. **Análise completa** do projeto existente (stack, arquitetura, patterns)
2. **Steering documents** customizados baseados na análise real
3. **Patterns directory** completo com tecnologias específicas identificadas
4. **Scripts funcionais** para task tracking e automação
5. **Templates** copy-paste ready baseados na stack real
6. **Configurações** de linting e automation específicas
7. **.cursorrules** otimizado para o projeto específico
8. **Documentação** de processo completa
9. **Validation scripts** para verificar qualidade da geração

### 🚀 **Características da Geração Automática:**
- **Context-Aware**: Baseada na análise real do código
- **Technology-Specific**: Patterns adaptados à stack identificada
- **Business-Contextualized**: Product.md reflete o domínio real
- **Automation-Ready**: Scripts funcionais imediatamente
- **Quality-Focused**: Validation automática da estrutura gerada
- **Production-Ready**: Configurações e workflows empresariais
- **Maintainable**: Versionamento e evolution guidelines
- **Trackable**: Sistema de task IDs integrado desde o início

### 🔧 **Comandos Pós-Geração:**
```bash
# Validar estrutura gerada
./kiro/scripts/validate-cdd-structure.sh

# Instalar automação
cd .kiro/scripts && npm install

# Configurar patterns
cp .kiro/patterns/linting/.eslintrc.custom.js .eslintrc.js

# Verificar qualidade
npm run check-patterns

# Gerar primeiro relatório
npm run status
```

### 📊 **Métricas Esperadas:**
- **Completude**: 95%+ de arquivos customizados (não placeholders)
- **Specificidade**: 100% tecnologias corretas identificadas
- **Funcionalidade**: Scripts executam sem erro
- **Compliance**: Validation passa em todos os checks
- **Usabilidade**: Desenvolvedor pode usar imediatamente

---

**Prompt Version**: 2.0.0  
**Generation Target**: Complete CDD v2.0 structure from codebase analysis  
**Automation Level**: Full automation with functional scripts and patterns  
**Quality Target**: Production-ready structure with 95%+ customization 