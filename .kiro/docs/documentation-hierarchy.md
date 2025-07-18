# Hierarquia da Documentação CDD v2.0

## 🎯 Single Source of Truth com Task Tracking Integrado

A documentação CDD v2.0 segue o princípio **Single Source of Truth** com hierarquia rigorosa e sistema de tracking obrigatório:

```
📋 .kiro/steering/     ← FONTE ÚNICA DA VERDADE (Tier 1)
├── product.md         ← Visão de produto e estratégia
├── structure.md       ← Organização e convenções  
└── tech.md           ← Stack e decisões técnicas

🎨 .kiro/patterns/     ← PADRÕES DE CÓDIGO OBRIGATÓRIOS (Tier 2)
├── README.md          ← Índice geral e visão geral
├── conventions.md     ← Convenções rigorosas de nomenclatura  
├── architecture.md    ← Padrões arquiteturais e SOLID
├── typescript.md      ← Padrões TypeScript (strict mode)
├── security.md        ← Diretrizes OWASP e security headers
├── performance.md     ← Otimizações e Core Web Vitals
├── testing.md         ← Padrões Jest/Vitest/Cypress
├── frontend/          ← Padrões React/Next.js específicos
├── backend/           ← Padrões Node.js/Express específicos  
├── database/          ← Padrões PostgreSQL/Prisma/migrations
├── examples/          ← Templates e código exemplo funcionais
└── linting/           ← Configurações ESLint/Prettier customizadas

📋 .kiro/specs/        ← ESPECIFICAÇÕES FUNCIONAIS (Tier 3)
├── feature-name/      ← Cada feature tem pasta própria
│   ├── requirements.md ← User stories e acceptance criteria
│   ├── design.md      ← Arquitetura técnica e diagramas
│   └── tasks.md       ← Tasks com IDs obrigatórios (feature-name-X.Y)
├── _template/         ← Template padrão para novas features
└── [outras features]

🤖 .kiro/scripts/      ← AUTOMAÇÃO E TRACKING (Tier 4)
├── package.json       ← Comandos npm para task management
├── task-manager.js    ← Sistema de tracking de tasks (Node.js)
├── check-patterns.js  ← Validação de compliance de patterns
├── validate-tasks.js  ← Validação de formato de task IDs
├── backup-tasks.sh    ← Backup automático de tasks
├── metrics-*.sh       ← Scripts de métricas e relatórios
├── cleanup-*.sh       ← Scripts de housekeeping
└── tasks-status.json  ← Estado atual das tasks (auto-gerado)

📚 .kiro/docs/         ← DOCUMENTAÇÃO DE PROCESSO (Tier 5)
├── README.md          ← Introdução ao CDD v2.0
├── INDEX.md           ← Navegação e quick start
├── implementation-guide.md ← Guia completo de implementação
├── workflow-completo.md    ← Workflow end-to-end
├── principles-and-best-practices.md ← Princípios fundamentais
├── todo-list-prompt-guide.md       ← Gestão de task IDs
├── template-structure.md           ← Templates e estruturas
├── patterns-workflow.md            ← Workflow de patterns
├── troubleshooting.md              ← Solução de problemas
└── [outros guias especializados]
```

## 🔄 Fluxo de Consulta Hierárquico CDD v2.0

### Workflow de Desenvolvimento Obrigatório
```mermaid
graph TD
    A[Task ID Atribuída] --> B{Consultar Steering}
    B --> C[steering/product.md - Contexto]
    C --> D[steering/tech.md - Stack]
    D --> E[steering/structure.md - Organização]
    E --> F{Consultar Patterns}
    F --> G[patterns/README.md - Índice]
    G --> H[patterns/[tech].md - Padrões específicos]
    H --> I[patterns/examples/ - Templates]
    I --> J{Consultar Specs}
    J --> K[specs/feature/requirements.md]
    K --> L[specs/feature/design.md]
    L --> M[specs/feature/tasks.md]
    M --> N[Implementar com Task ID]
    N --> O[npm run complete feature-name-X.Y]
    O --> P[Validar Patterns]
    P --> Q{Patterns OK?}
    Q -->|Sim| R[Task Concluída]
    Q -->|Não| H
```

### Hierarquia de Autoridade (Ordem de Precedência)
```
1. STEERING (product → tech → structure)    ← MÁXIMA AUTORIDADE
2. PATTERNS (por tecnologia específica)     ← REGRAS TÉCNICAS
3. SPECS (requirements → design → tasks)    ← IMPLEMENTAÇÃO
4. SCRIPTS (automação e validação)          ← CONFORMIDADE
5. DOCS (processo e guidelines)             ← REFERÊNCIA
```

### Comandos de Consulta por Tier

#### Tier 1 - Steering (Contexto Estratégico)
```bash
# Consulta obrigatória antes de qualquer implementação
cat .kiro/steering/product.md     # Por que este projeto existe?
cat .kiro/steering/tech.md        # Que tecnologias usamos e por quê?
cat .kiro/steering/structure.md   # Como organizamos o código?
```

#### Tier 2 - Patterns (Padrões Técnicos)
```bash
# Consulta obrigatória durante implementação
cat .kiro/patterns/README.md                    # Índice de todos os padrões
cat .kiro/patterns/typescript.md                # Para qualquer código TS
cat .kiro/patterns/frontend/react.md            # Para componentes React
cat .kiro/patterns/backend/nodejs.md            # Para APIs Node.js
cat .kiro/patterns/database/postgresql.md       # Para queries DB
ls .kiro/patterns/examples/                     # Templates práticos
npm run check-patterns                          # Validação automática
```

#### Tier 3 - Specs (Funcionalidades)
```bash
# Consulta para feature específica
cat .kiro/specs/feature-name/requirements.md    # O que fazer?
cat .kiro/specs/feature-name/design.md          # Como fazer?
cat .kiro/specs/feature-name/tasks.md           # Quando fazer?
npm run list feature-name                       # Ver task IDs
```

#### Tier 4 - Scripts (Automação)
```bash
# Comandos obrigatórios de tracking
npm run start feature-name-X.Y         # Iniciar task
npm run complete feature-name-X.Y      # Completar task (OBRIGATÓRIO)
npm run status                          # Ver progresso geral
npm run scan                            # Atualizar tracking
npm run validate-tasks                  # Validar formato de IDs
npm run backup                          # Backup automático
```

#### Tier 5 - Docs (Processo)
```bash
# Consulta para entendimento de processo
cat .kiro/docs/README.md                        # Introdução ao CDD
cat .kiro/docs/implementation-guide.md          # Como implementar CDD
cat .kiro/docs/workflow-completo.md             # Workflow completo
cat .kiro/docs/troubleshooting.md               # Solução de problemas
```

## 📊 Mapeamento Detalhado CDD v2.0

### .kiro/steering/ (Single Source of Truth)
**Role**: Autoridade máxima para todas as decisões

**Atualização**: Apenas por tech leads/arquitetos
**Frequência**: Apenas para mudanças estratégicas
**Impacto**: Propaga para todos os outros tiers

- **product.md**: Visão, objetivos, progressive strategy, success metrics
- **structure.md**: Organização de pastas, convenções, path aliases, filosofia
- **tech.md**: Stack tecnológico, decisões arquiteturais, LLM-First approach

### .kiro/patterns/ (Code Standards)
**Role**: Padrões técnicos obrigatórios e automatizados

**Atualização**: Por consenso da equipe
**Frequência**: Mensal ou quando necessário
**Impacto**: Validação automática via linting

- **README.md**: Índice navegável de todos os padrões
- **conventions.md**: Nomenclatura rigorosa (PascalCase, camelCase, kebab-case)
- **architecture.md**: SOLID, DRY, design patterns, dependency injection
- **typescript.md**: Strict mode, interfaces, types, no-any policy
- **security.md**: OWASP guidelines, input validation, security headers
- **performance.md**: Bundle size, lazy loading, Core Web Vitals
- **testing.md**: Jest/Vitest patterns, coverage >90%, naming conventions
- **frontend/**: React patterns, Next.js optimizations, accessibility
- **backend/**: Node.js/Express patterns, API design, error handling
- **database/**: PostgreSQL/Prisma patterns, migrations, indexing
- **examples/**: Working code templates, copy-paste ready
- **linting/**: ESLint/Prettier configs, automated enforcement

### .kiro/specs/ (Feature Implementation)
**Role**: Especificações funcionais com task tracking obrigatório

**Atualização**: Durante desenvolvimento das features
**Frequência**: Contínua durante sprints
**Impacto**: Tracking automático via scripts

Por feature:
- **requirements.md**: User stories, acceptance criteria, business rules
- **design.md**: Technical architecture, data flow, API contracts, Mermaid diagrams
- **tasks.md**: Implementation plan com task IDs obrigatórios (feature-name-X.Y)

### .kiro/scripts/ (Automation Engine)
**Role**: Automação total do sistema CDD

**Atualização**: Conforme necessidades de automação
**Frequência**: Contínua (melhorias e bugfixes)
**Impacto**: Conformidade e qualidade automatizadas

Scripts essenciais:
- **task-manager.js**: Core do sistema de tracking
- **check-patterns.js**: Validação de compliance
- **validate-tasks.js**: Validação de formato de task IDs
- **backup-tasks.sh**: Backup/recovery automático
- **metrics-completeness.sh**: Métricas de progresso
- **cleanup-*.sh**: Housekeeping automático
- **interactive-cli.sh**: Interface amigável

### .kiro/docs/ (Process Documentation)
**Role**: Documentação de processo e treinamento

**Atualização**: Conforme evolução do processo
**Frequência**: Quando há mudanças significativas
**Impacto**: Onboarding e referência

Documentos essenciais:
- **README.md**: Introdução e overview
- **implementation-guide.md**: Setup e configuração completa
- **workflow-completo.md**: Workflow end-to-end detalhado
- **principles-and-best-practices.md**: Princípios fundamentais
- **troubleshooting.md**: Solução de problemas comuns

## ⚠️ Princípios de Manutenção CDD v2.0

### Regras de Ouro
1. **Steering = Imutável**: Mudanças apenas para decisões estratégicas
2. **Patterns = Aplicação Automática**: Linting força compliance
3. **Specs = Task IDs Obrigatórios**: Sistema de tracking rigoroso
4. **Scripts = Automação Total**: Zero intervenção manual
5. **Docs = Living Documentation**: Evolui com o sistema

### Sistema de Validação Contínua
```bash
# Validações automáticas (executadas sempre)
npm run check-patterns     # Compliance de código
npm run validate-tasks     # Formato de task IDs
npm run scan              # Atualização de tracking
npm run backup            # Backup preventivo

# Validações periódicas (semanais)
npm run patterns:report   # Relatório de compliance
npm run metrics:velocity  # Métricas de produtividade
npm run cleanup:scan      # Housekeeping automático

# Validações críticas (antes de release)
npm run final-validation  # Checklist completo
npm run health-dashboard  # Status geral do projeto
```

### Anti-Patterns de Hierarquia
```markdown
❌ NÃO FAÇA:
- Contradizer steering em patterns ou specs
- Criar documentação duplicada entre tiers
- Pular consulta a patterns durante implementação
- Implementar sem task ID válido
- Modificar steering sem aprovação de arquitetos
- Usar patterns não documentados
- Deixar tasks sem tracking

✅ FAÇA:
- Seguir hierarquia rigorosa: steering → patterns → specs → code
- Atualizar documentação relevante quando código muda
- Usar task IDs no formato feature-name-X.Y obrigatoriamente
- Validar patterns antes de commit
- Propagar mudanças de steering para outros tiers
- Contribuir com patterns baseado em experiência
- Marcar progresso automaticamente com scripts
```

## 🔧 Ferramentas de Validação CDD v2.0

### Validação de Consistência
```bash
npm run validate-consistency    # Verifica alignment entre tiers
npm run check-staleness        # Detecta documentação desatualizada
npm run audit-patterns         # Auditoria de compliance
npm run validate-task-format   # Formato correto de task IDs
```

### Métricas de Qualidade
```bash
npm run quality-dashboard      # Dashboard geral de qualidade
npm run patterns-compliance    # Score de compliance de patterns
npm run task-velocity         # Métricas de velocity por feature
npm run documentation-health  # Saúde da documentação
```

### Automação de Manutenção
```bash
npm run auto-cleanup          # Limpeza automática semanal
npm run sync-patterns         # Sincronização de patterns
npm run update-metrics        # Atualização de métricas
npm run health-check          # Verificação de saúde geral
```

## 🎯 **Resultado**: Hierarquia CDD v2.0 com autoridade clara, automação total e tracking obrigatório garantindo consistência e qualidade empresarial!

### ✅ **Principais Benefícios da Hierarquia:**
- **Clarity**: Ordem de precedência clara para consultas
- **Automation**: Scripts garantem conformidade automática
- **Traceability**: Task IDs permitem tracking completo
- **Consistency**: Single Source of Truth rigorosamente aplicado
- **Quality**: Validação contínua em todos os tiers
- **Productivity**: Redução de 50% em tempo de onboarding
- **Maintainability**: Sistema auto-gerenciado com housekeeping automático

---

**Última atualização**: 2025-01-14T10:30:00.000Z
**Status**: ✅ Hierarquia CDD v2.0 implementada com task tracking obrigatório e automação completa