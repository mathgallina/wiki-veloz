# Guia de Task Management CDD v2.0

## 🎯 Quando Usar Este Guia

Use estas instruções sempre que um usuário solicitar:
- "Crie uma todo list para..."
- "Preciso organizar as tarefas de..."
- "Monte um checklist para..."
- "Lista as etapas para implementar..."
- Qualquer request que envolva **organização de tasks com tracking automático**

## 🚨 SISTEMA DE TASK IDS OBRIGATÓRIO

### Formato Rígido: `feature-name-X.Y`
- **feature-name**: Nome da pasta da feature (kebab-case)
- **X**: Número da fase (1, 2, 3, etc.)
- **Y**: Número da task dentro da fase (1, 2, 3, etc.)

### Exemplos Corretos:
```
user-authentication-1.1    # Feature: user-authentication, Fase 1, Task 1
design-system-2.3          # Feature: design-system, Fase 2, Task 3
api-integration-1.2        # Feature: api-integration, Fase 1, Task 2
payment-gateway-3.1        # Feature: payment-gateway, Fase 3, Task 1
```

### ❌ Formatos Inválidos:
```
task-1                      # Falta feature name
user-auth-1                 # Falta número da task
authentication-A.1          # Letra no lugar de número
auth-1.0                   # Zero não é permitido
```

## 📋 TEMPLATE DE PROMPT PARA TASK LISTS

```
Preciso criar uma task list CDD v2.0 para [OBJETIVO/PROJETO].

CONTEXTO:
- Feature Name: [nome-da-feature] (kebab-case para IDs)
- Projeto: [Nome e descrição breve]
- Stack: [Tecnologias principais]
- Prazo: [Se aplicável]
- Complexidade: [Simples/Média/Alta]

ESCOPO:
- [Funcionalidade/Feature principal]
- [Requisitos específicos]
- [Limitações/Restrições]

PRIORIDADES:
1. [Alta prioridade]
2. [Média prioridade] 
3. [Baixa prioridade]

FORMATO OBRIGATÓRIO:
- Use task IDs: feature-name-X.Y
- Numeração sequencial sem gaps
- Estimativas de tempo incluídas
- Dependências explícitas
- Comandos de tracking integrados
```

## 🔧 Estrutura Ideal com Task IDs CDD v2.0

### Formato Padrão
```markdown
# [Feature Name] - Implementation Plan

## 📊 Resumo
- **Feature ID**: feature-name
- **Total de tasks**: X
- **Estimativa total**: X horas/dias
- **Status atual**: Planejamento/Em andamento/Concluído

## 🎯 Objetivos
- **Objetivo principal**: [Descrição]
- **Métricas de sucesso**: [Como medir]
- **Acceptance criteria**: [Critérios finais]

## 📋 Tasks por Fase (IDs Obrigatórios)

### Phase 1: Foundation
- [ ] 1.1 Setup base structure
  - [ ] Create main component files
  - [ ] Setup routing (if needed)
  - _Requirements: [1.1, 1.2]_
  - _Estimated: 2h_
  - _Dependencies: none_
  - **Task ID**: `feature-name-1.1`

- [ ] 1.2 Implement core logic
  - [ ] Business logic implementation
  - [ ] Data validation
  - _Requirements: [2.1, 2.2]_
  - _Estimated: 4h_
  - _Dependencies: [1.1]_
  - **Task ID**: `feature-name-1.2`

### Phase 2: Integration
- [ ] 2.1 Backend integration
  - [ ] API endpoints
  - [ ] Data fetching
  - _Requirements: [4.1, 4.2]_
  - _Estimated: 3h_
  - _Dependencies: [1.1, 1.2]_
  - **Task ID**: `feature-name-2.1`

### 🤖 Comandos de Tracking Automático

#### Durante Desenvolvimento:
```bash
# Ver tasks disponíveis
npm run list feature-name

# Verificar progresso
npm run status

# Marcar task como concluída (OBRIGATÓRIO)
npm run complete feature-name-1.1
npm run complete feature-name-1.2
npm run complete feature-name-2.1
```

#### Monitoramento:
```bash
# Monitoramento em tempo real
npm run watch

# Relatórios de progresso
npm run report

# Métricas de velocity
./scripts/velocity-metrics.sh

# Health check
./scripts/health-dashboard.sh
```

## ⚡ Automação Integrada

### Scripts Obrigatórios:
```bash
# Validação de formato
./scripts/validate-task-format.sh feature-name

# Backup automático
./scripts/backup-tasks.sh

# Limpeza e manutenção
./scripts/weekly-cleanup.sh

# Validação completa
./scripts/final-validation.sh
```
```

## 🎨 Templates por Categoria CDD v2.0

### Para Features Novas
```markdown
# [Feature Name] - Implementation Plan

### Phase 1: Foundation
- [ ] 1.1 Research and planning
  - [ ] Technical research
  - [ ] Architecture design
  - _Requirements: [All]_
  - _Estimated: 3h_
  - **Task ID**: `feature-name-1.1`

- [ ] 1.2 Setup base structure  
  - [ ] Create folders and files
  - [ ] Setup basic configuration
  - _Requirements: [1.1]_
  - _Estimated: 1h_
  - _Dependencies: [1.1]_
  - **Task ID**: `feature-name-1.2`

### Phase 2: Implementation
- [ ] 2.1 Core functionality
  - [ ] Main feature logic
  - [ ] Data handling
  - _Requirements: [2.1, 2.2]_
  - _Estimated: 6h_
  - _Dependencies: [1.2]_
  - **Task ID**: `feature-name-2.1`

- [ ] 2.2 Integration points
  - [ ] API integration
  - [ ] External services
  - _Requirements: [2.3, 2.4]_
  - _Estimated: 4h_
  - _Dependencies: [2.1]_
  - **Task ID**: `feature-name-2.2`

### Phase 3: Quality & Polish  
- [ ] 3.1 Testing & validation
  - [ ] Unit tests
  - [ ] Integration tests
  - _Requirements: [All]_
  - _Estimated: 3h_
  - _Dependencies: [2.1, 2.2]_
  - **Task ID**: `feature-name-3.1`

- [ ] 3.2 Documentation & deployment
  - [ ] Update docs
  - [ ] Deploy to staging
  - _Requirements: [All]_
  - _Estimated: 2h_
  - _Dependencies: [3.1]_
  - **Task ID**: `feature-name-3.2`
```

### Para Refatoração
```markdown
# [Component] Refactoring - Modernization Plan

### Phase 1: Analysis
- [ ] 1.1 Code audit and assessment
  - [ ] Identify code smells
  - [ ] Map dependencies
  - [ ] Performance baseline
  - _Estimated: 2h_
  - **Task ID**: `component-refactor-1.1`

- [ ] 1.2 Strategy definition
  - [ ] Define refactoring approach
  - [ ] Plan migration steps
  - [ ] Risk assessment
  - _Estimated: 1h_
  - _Dependencies: [1.1]_
  - **Task ID**: `component-refactor-1.2`

### Phase 2: Execution
- [ ] 2.1 Backup and preparation
  - [ ] Create feature branch
  - [ ] Backup current state
  - [ ] Setup testing environment
  - _Estimated: 30min_
  - _Dependencies: [1.2]_
  - **Task ID**: `component-refactor-2.1`

- [ ] 2.2 Core refactoring
  - [ ] Refactor main module
  - [ ] Update imports/exports
  - [ ] Maintain API compatibility
  - _Estimated: 4h_
  - _Dependencies: [2.1]_
  - **Task ID**: `component-refactor-2.2`

### Phase 3: Validation
- [ ] 3.1 Testing and validation
  - [ ] Run test suite
  - [ ] Performance comparison
  - [ ] Integration validation
  - _Estimated: 2h_
  - _Dependencies: [2.2]_
  - **Task ID**: `component-refactor-3.1`
```

### Para Bug Fixes
```markdown
# [Bug Description] - Fix Implementation

### Phase 1: Investigation
- [ ] 1.1 Bug reproduction
  - [ ] Reproduce locally
  - [ ] Document steps
  - [ ] Identify affected users
  - _Estimated: 1h_
  - **Task ID**: `bug-fix-issue-id-1.1`

- [ ] 1.2 Root cause analysis
  - [ ] Debug and trace issue
  - [ ] Identify root cause
  - [ ] Assess impact scope
  - _Estimated: 2h_
  - _Dependencies: [1.1]_
  - **Task ID**: `bug-fix-issue-id-1.2`

### Phase 2: Resolution
- [ ] 2.1 Implement fix
  - [ ] Code the solution
  - [ ] Add regression tests
  - [ ] Validate edge cases
  - _Estimated: 3h_
  - _Dependencies: [1.2]_
  - **Task ID**: `bug-fix-issue-id-2.1`

- [ ] 2.2 Prevention measures
  - [ ] Improve logging
  - [ ] Add monitoring
  - [ ] Update documentation
  - _Estimated: 1h_
  - _Dependencies: [2.1]_
  - **Task ID**: `bug-fix-issue-id-2.2`
```

## ✅ Regras Obrigatórias CDD v2.0

### ✅ SEMPRE FAÇA
- **IDs únicos**: Cada task deve ter ID único no formato `feature-name-X.Y`
- **Numeração sequencial**: 1.1, 1.2, 1.3, 2.1, 2.2 (sem gaps)
- **Estimativas**: Inclua tempo estimado para cada task
- **Dependências**: Mapeie dependências entre tasks
- **Requirements**: Referencie requirements específicos
- **Tracking**: Marque progresso com `npm run complete feature-name-X.Y`
- **Validação**: Execute `./scripts/validate-task-format.sh` regularmente

### ❌ NUNCA FAÇA
- **IDs inválidos**: task-1, auth-A.1, component-1.0
- **Gaps na numeração**: 1.1, 1.3 (sem 1.2)
- **Tasks sem ID**: Tasks genéricas sem identificação
- **Estimativas vagas**: "Algumas horas" vs "3h"
- **Dependências omitidas**: Não documentar pré-requisitos
- **Tracking esquecido**: Implementar sem marcar progresso

### 🔧 Automação Obrigatória
- **Usar scripts**: npm run complete após cada task
- **Monitoramento**: npm run watch durante desenvolvimento
- **Backup**: ./scripts/backup-tasks.sh regularmente
- **Validação**: ./scripts/final-validation.sh antes de releases
- **Housekeeping**: ./scripts/weekly-cleanup.sh semanalmente

## 🔄 Integração Total com CDD

### Para Projetos com .kiro/
```markdown
## 📂 CDD Integration Checklist

### Steering Compliance
- [ ] Alinhado com product.md objectives
- [ ] Segue estrutura de structure.md
- [ ] Usa tecnologias de tech.md
- **Task ID**: `feature-name-0.1`

### Pattern Compliance  
- [ ] Segue patterns/[technology].md
- [ ] Nomenclatura de patterns/conventions.md
- [ ] Linting de patterns/linting/
- **Task ID**: `feature-name-0.2`

### Automation Setup
- [ ] Scripts instalados (.kiro/scripts/)
- [ ] Tracking funcionando (npm run status)
- [ ] Validation ativa (./scripts/final-validation.sh)
- **Task ID**: `feature-name-0.3`

### Documentation Updates
- [ ] Spec atualizada em specs/feature-name/
- [ ] Requirements documentados
- [ ] Design documented
- [ ] Tasks com IDs válidos
- **Task ID**: `feature-name-0.4`
```

## 📊 Monitoring & Metrics CDD v2.0

### Dashboard de Progresso
```bash
# Status geral do projeto
npm run status

# Progresso por feature
npm run list feature-name

# Métricas de velocity
./scripts/velocity-metrics.sh

# Health check completo
./scripts/health-dashboard.sh

# Relatório para stakeholders
npm run report
```

### Template de Status Report Automático
```markdown
## 📈 Progress Report: [Feature Name] - [Data]

### 📊 Metrics (Auto-Generated)
- **Completion Rate**: X% (Y/Z tasks)
- **Velocity**: X tasks/week
- **ETA**: X days (based on current velocity)
- **Health Score**: X/100

### ✅ Completed Tasks
- [feature-name-1.1] Setup base structure ✅
- [feature-name-1.2] Implement core logic ✅

### 🚧 In Progress
- [feature-name-2.1] Backend integration - 60% ⏳

### ⏸️ Pending
- [feature-name-2.2] Frontend integration ⏸️
- [feature-name-3.1] Testing & validation ⏸️

### 🔄 Next Actions (Auto-Prioritized)
1. Complete feature-name-2.1 (blocking 2.2)
2. Start feature-name-2.2 (high priority)

### ⚠️ Issues & Blockers
- [Auto-detected from tracking]

### 🎯 Quality Metrics
- **Pattern Compliance**: X% (npm run check-patterns)
- **Test Coverage**: X%
- **Documentation**: Up to date ✅

### 🤖 Automation Status
- **Backup**: Last run [date] ✅
- **Housekeeping**: Last run [date] ✅  
- **Validation**: Last run [date] ✅
```

## 🚀 Exemplo Prático Completo CDD v2.0

### Solicitação do Usuário:
> "Crie uma task list para implementar sistema de notificações push no app React Native"

### Task List CDD v2.0 Gerada:
```markdown
# Push Notifications - Implementation Plan

## 📊 Resumo
- **Feature ID**: push-notifications
- **Total de tasks**: 12
- **Estimativa total**: 18-22 horas
- **Status atual**: Planejamento

## 🎯 Objetivos
- **Principal**: Sistema completo de notificações push
- **Métricas**: 90%+ delivery rate, <2s response time
- **Acceptance**: iOS/Android funcionando + dashboard admin

## 📋 Tasks por Fase (IDs Obrigatórios)

### Phase 1: Foundation
- [ ] 1.1 Setup Firebase & dependencies
  - [ ] Configure Firebase Cloud Messaging
  - [ ] Install @react-native-push-notification
  - [ ] Setup certificates iOS/Android
  - _Requirements: [1.1, 1.2]_
  - _Estimated: 3h_
  - _Dependencies: none_
  - **Task ID**: `push-notifications-1.1`

- [ ] 1.2 Backend infrastructure
  - [ ] API endpoint for device tokens
  - [ ] Push notification service
  - [ ] Database schema for notifications
  - _Requirements: [1.3, 1.4]_
  - _Estimated: 4h_
  - _Dependencies: [1.1]_
  - **Task ID**: `push-notifications-1.2`

### Phase 2: Core Implementation
- [ ] 2.1 Mobile app integration
  - [ ] SDK integration
  - [ ] Permission management
  - [ ] Token registration
  - _Requirements: [2.1, 2.2]_
  - _Estimated: 3h_
  - _Dependencies: [1.1]_
  - **Task ID**: `push-notifications-2.1`

- [ ] 2.2 Notification handling
  - [ ] Foreground notifications
  - [ ] Background notifications
  - [ ] Deep linking
  - _Requirements: [2.3, 2.4]_
  - _Estimated: 4h_
  - _Dependencies: [2.1]_
  - **Task ID**: `push-notifications-2.2`

- [ ] 2.3 Admin dashboard
  - [ ] Send notification interface
  - [ ] User segmentation
  - [ ] Notification history
  - _Requirements: [3.1, 3.2]_
  - _Estimated: 5h_
  - _Dependencies: [1.2]_
  - **Task ID**: `push-notifications-2.3`

### Phase 3: Testing & Validation
- [ ] 3.1 Testing suite
  - [ ] Unit tests for services
  - [ ] Integration tests
  - [ ] E2E tests on physical devices
  - _Requirements: [All]_
  - _Estimated: 3h_
  - _Dependencies: [2.1, 2.2, 2.3]_
  - **Task ID**: `push-notifications-3.1`

- [ ] 3.2 Documentation & deployment
  - [ ] Developer documentation
  - [ ] Admin user manual
  - [ ] Deploy to staging
  - _Requirements: [All]_
  - _Estimated: 2h_
  - _Dependencies: [3.1]_
  - **Task ID**: `push-notifications-3.2`

## 🤖 Tracking Commands
```bash
# Monitor development
npm run watch

# Check progress
npm run list push-notifications

# Mark tasks complete (after each implementation)
npm run complete push-notifications-1.1
npm run complete push-notifications-1.2
# ... continue for each task

# Generate reports
npm run report
./scripts/velocity-metrics.sh
```

## ⚠️ Dependencies & Prerequisites
- Firebase project must be configured before 1.1
- Backend API ready before mobile testing (2.1 → 2.2)
- Valid iOS certificates required for testing
- Physical devices needed (simulators don't support push)

## 🔧 Automation Setup
```bash
# Initial setup
cd .kiro/scripts && ./install.sh

# Validate task format
./scripts/validate-task-format.sh push-notifications

# Setup monitoring
npm run watch &

# Schedule housekeeping
crontab -e
# Add: 0 2 * * 1 cd /project/.kiro/scripts && ./weekly-cleanup.sh
```

## 📊 Success Metrics
- **Technical**: 95%+ task completion rate
- **Quality**: 0 critical bugs in production
- **Performance**: <2s notification delivery
- **Adoption**: 80%+ users opt-in to notifications
- **Tracking**: 100% tasks marked with correct IDs
```

---

## 💡 Integração com LLMs (Cursor IDE)

### Instruções para .cursorrules
O LLM deve sempre:
- **Identificar task ID** antes de implementar
- **Consultar .kiro/patterns/** para padrões
- **Marcar progresso** com `npm run complete feature-name-X.Y`
- **Validar formato** com scripts automáticos
- **Sugerir próxima task** baseada em dependências

### Workflow Automático Esperado:
```
User: "Implemente autenticação JWT"
LLM: "Vou implementar seguindo a task list:

1. 📋 Identifiquei tasks:
   - user-authentication-1.1: Setup JWT middleware ⏳
   - user-authentication-1.2: Login endpoint 🔄
   
2. 📐 Aplicando patterns de .kiro/patterns/backend/
3. 🔧 Implementando...
4. ✅ Executando: npm run complete user-authentication-1.1
5. 📊 Progresso: 50% (1/2 tasks)

Próxima: user-authentication-1.2. Continuar?"
```

---

> **🎯 Resultado**: Task lists que se integram perfeitamente ao sistema CDD v2.0 com tracking automático, validação contínua e qualidade empresarial garantida! 