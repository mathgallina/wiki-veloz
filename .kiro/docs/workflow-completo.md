# Workflow Completo - Context-Driven Documentation

## 🎯 Fluxo Completo de Implementação

### FASE 1: Setup Inicial

#### Para Projetos Novos
```bash
# 1. Gerar estrutura .kiro automaticamente
# Use: docs/prompt-execucao-direto.md

# 2. Gerar padrões de código específicos
# Use: docs/patterns-prompt-direto.md

# 3. Configurar scripts de gerenciamento
cd .kiro/scripts
./install.sh

# 4. Validar setup inicial
./scripts/final-validation.sh

# 5. Gerar .cursorrules para Cursor IDE  
# Use: docs/cursorrules-prompt-direto.md
```

#### Para Projetos Existentes
```bash
# 1. Implementar manualmente
# Seguir: docs/implementation-guide.md

# 2. Gerar padrões de código baseados no projeto
# Use: docs/patterns-prompt-direto.md

# 3. Configurar scripts
cd .kiro/scripts  
./install.sh

# 4. Validar migração
./scripts/final-validation.sh

# 5. Otimizar para LLM
# Use: docs/cursorrules-prompt-direto.md
```

### FASE 2: Desenvolvimento Diário

#### 🚨 OBRIGATÓRIO: Sistema de Task IDs
**Formato Padrão**: `feature-name-X.Y`

```bash
# Exemplos de IDs corretos:
user-authentication-1.1    # Feature: user-authentication, Fase 1, Task 1
design-system-2.3          # Feature: design-system, Fase 2, Task 3
api-integration-1.2        # Feature: api-integration, Fase 1, Task 2
payment-gateway-3.1        # Feature: payment-gateway, Fase 3, Task 1
```

#### Workflow do Desenvolvedor (Atualizado)
```bash
# 1. Começar o dia
cd .kiro/scripts
npm run status        # Ver progresso geral
npm run watch         # Monitorar tarefas automaticamente (background)

# 2. Listar tarefas disponíveis
npm run list                    # Todas as features
npm run list user-auth          # Feature específica

# 3. Implementar feature
# - Consultar .kiro/steering/ para contexto
# - **OBRIGATÓRIO**: Consultar .kiro/patterns/ para padrões específicos
# - Ler .kiro/specs/feature-name/ para detalhes
# - Implementar seguindo padrões definidos em patterns/

# 4. Marcar progresso (CRÍTICO - OBRIGATÓRIO)
npm run complete user-authentication-1.1
npm run complete design-system-2.3
npm run complete api-integration-1.2

# 5. Verificar progresso
npm run status
npm run report        # Para stakeholders

# 6. CLI interativo (alternativa mais fácil)
./scripts/interactive-cli.sh
```

#### ⚠️ CRÍTICO: Task IDs e Progresso
```bash
# FORMATO OBRIGATÓRIO para task IDs
feature-name-X.Y

# Onde:
# - feature-name: Nome da pasta da feature (kebab-case)
# - X: Número da fase (1, 2, 3, etc.)
# - Y: Número da task dentro da fase (1, 2, 3, etc.)

# SEMPRE executar após completar qualquer implementação
npm run complete [task-id]

# Exemplos práticos com IDs corretos:
npm run complete user-authentication-1.1    # Setup JWT
npm run complete user-authentication-1.2    # Middleware auth
npm run complete user-authentication-2.1    # Login endpoint
npm run complete user-management-2.2        # CRUD usuários  
npm run complete design-system-3.1          # Button component
npm run complete notification-system-2.1    # Email provider

# Para encontrar task-id correto:
npm run list user-authentication            # Listar tarefas da feature
grep -n "^-\s\[" .kiro/specs/user-authentication/tasks.md  # Ver formato correto
```

#### Sistema de Backup e Recovery
```bash
# Backup automático (executar semanalmente)
./scripts/backup-tasks.sh

# Rollback de task específica
./scripts/rollback-task.sh user-authentication-1.2

# Rollback de feature completa
./scripts/rollback-feature.sh user-authentication all
./scripts/rollback-feature.sh design-system 2    # Apenas fase 2

# Restaurar de backup
./scripts/restore-tasks.sh 2024-01-15_14-30-00
```

#### Workflow do Team Lead (Expandido)
```bash
# Daily standup
npm run status
./scripts/velocity-metrics.sh    # Métricas de velocity

# Relatórios semanais  
npm run report
npm run report --json           # Para integrações
./scripts/health-dashboard.sh   # Saúde geral do projeto

# Planejamento e ETA
npm run list                    # Ver todas as tarefas
./scripts/eta-calculator.sh user-authentication  # Estimativa de conclusão

# Housekeeping semanal
./scripts/weekly-cleanup.sh     # Limpeza automática
```

### FASE 3: Manutenção e Qualidade

#### Housekeeping Automático
```bash
# Limpeza semanal (automatizar no cron)
./scripts/weekly-cleanup.sh

# Verificações específicas
./scripts/cleanup-dead-code.sh     # Código não utilizado
./scripts/cleanup-dependencies.sh  # Dependências orfãs
./scripts/cleanup-docs.sh          # Documentação orfã

# Validação de formato de tasks
./scripts/validate-task-format.sh user-authentication
```

#### Validação e Qualidade
```bash
# Validação completa do projeto
./scripts/final-validation.sh

# Métricas específicas
./scripts/metrics-completeness.sh  # Completude da documentação
./scripts/metrics-code-quality.sh  # Qualidade do código
./scripts/metrics-progress.sh      # Progresso das tasks

# Dashboard web
./scripts/generate-web-dashboard.sh
```

### FASE 4: Evolução do Projeto

#### Adicionando Nova Feature (Processo Robusto)
```bash
# 1. Usar script automatizado
./scripts/new-feature.sh payment-gateway

# Ou processo manual:
# 1.1. Copiar template
cp -r .kiro/specs/_template .kiro/specs/payment-gateway

# 1.2. Personalizar template (remover placeholders)
# Editar: requirements.md, design.md, tasks.md
# IMPORTANT: Tasks devem seguir formato payment-gateway-X.Y

# 2. Validar formato
./scripts/validate-task-format.sh payment-gateway

# 3. Revisar patterns aplicáveis
ls .kiro/patterns/              # Ver patterns disponíveis
cat .kiro/patterns/README.md    # Índice de patterns

# 4. Escanear novas tarefas
npm run scan

# 5. Verificar se tasks foram detectadas
npm run list payment-gateway

# 6. Atualizar .cursorrules se necessário
# Use: docs/cursorrules-prompt-direto.md
```

#### Atualizando Documentação (Processo Sistemático)
```bash
# 1. Identificar o que mudou
git diff HEAD~1 --name-only | grep -E "\.(md|ts|tsx|js|jsx)$"

# 2. Atualizar documentação relevante
# - .kiro/steering/ para mudanças arquiteturais
# - .kiro/specs/ para mudanças de feature
# - .kiro/patterns/ para novos padrões

# 3. Re-escanear tarefas
npm run scan

# 4. Validar consistência
npm run validate-docs

# 5. Atualizar .cursorrules se mudanças significativas
# Use: docs/cursorrules-prompt-direto.md

# 6. Verificar se não quebrou nada
./scripts/final-validation.sh
```

## 🔄 Integrações e Automação

### CI/CD Pipeline (Robusta)
```yaml
# .github/workflows/kiro-status.yml
name: CDD Status Check
on: [push, pull_request]

jobs:
  validate-cdd:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
          
      - name: Install CDD scripts
        run: |
          cd .kiro/scripts
          npm install
          
      - name: Validate CDD structure
        run: ./scripts/final-validation.sh
        
      - name: Check task format
        run: |
          for feature in .kiro/specs/*/; do
            if [ -d "$feature" ] && [ "$(basename "$feature")" != "_template" ]; then
              ./scripts/validate-task-format.sh $(basename "$feature")
            fi
          done
          
      - name: Generate status report
        run: |
          npm run scan
          npm run status
          npm run report --json > cdd-report.json
          
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: cdd-report
          path: cdd-report.json
```

### Slack/Discord Integration
```bash
# Configurar webhook
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."

# Notificações automáticas
./scripts/slack-notify.sh complete user-authentication-1.1
./scripts/slack-notify.sh feature-complete payment-gateway

# Relatório automático (adicionar ao cron)
0 9 * * 1 cd /projeto/.kiro/scripts && npm run report | ./slack-notify.sh report
```

### Dashboard Integration
```javascript
// Consumir dados do CDD
class CDDDashboard {
  async loadData() {
    const [status, metrics, health] = await Promise.all([
      fetch('.kiro/scripts/task-report.json').then(r => r.json()),
      fetch('.kiro/scripts/metrics-report.json').then(r => r.json()),
      fetch('.kiro/scripts/health-report.json').then(r => r.json())
    ]);
    
    return { status, metrics, health };
  }
  
  updateDashboard(data) {
    // Atualizar componentes do dashboard
    this.updateProgress(data.status);
    this.updateMetrics(data.metrics);
    this.updateHealth(data.health);
  }
}
```

## 📊 Métricas e Monitoramento Avançado

### KPIs Principais (Expandidos)
- **Progresso Geral**: % de tarefas concluídas por feature
- **Velocidade**: Tasks/semana por desenvolvedor
- **Qualidade**: % de tasks sem retrabalho ou rollback
- **Documentação**: % de features com docs completas e atualizadas
- **Conformidade**: % de código seguindo patterns definidos
- **Saúde Técnica**: Debt score, código morto, dependências desatualizadas
- **Task ID Compliance**: % de tasks seguindo formato correto

### Relatórios Automáticos (Robustos)
```bash
# Relatório completo semanal
crontab -e
0 9 * * 1 cd /projeto/.kiro/scripts && ./scripts/full-dashboard.sh > weekly-report.txt

# Backup automático
0 2 * * 1 cd /projeto/.kiro/scripts && ./scripts/backup-tasks.sh

# Limpeza automática
0 3 * * 1 cd /projeto/.kiro/scripts && ./scripts/weekly-cleanup.sh
```

### Alertas Automáticos
```bash
# Script de alertas
#!/bin/bash
# scripts/check-alerts.sh

# Verificar tasks com formato inválido
invalid_tasks=$(find .kiro/specs -name "tasks.md" -exec grep -l "\[ \].*[^0-9\.]" {} \; | wc -l)
if [ $invalid_tasks -gt 0 ]; then
    echo "🚨 ALERT: $invalid_tasks features have invalid task format"
    ./scripts/slack-notify.sh alert "Invalid task format detected"
fi

# Verificar documentação desatualizada
stale_docs=$(find .kiro -name "*.md" -mtime +30 | wc -l)
if [ $stale_docs -gt 5 ]; then
    echo "⚠️ ALERT: $stale_docs documents older than 30 days"
fi

# Verificar progresso estagnado
if [ $(git log --since="1 week ago" --oneline .kiro/ | wc -l) -eq 0 ]; then
    echo "🐌 ALERT: No CDD activity in the last week"
fi
```

## 🎯 Cenários de Uso (Atualizados)

### Time Pequeno (1-3 devs)
```bash
# Setup essencial
./install.sh
npm run watch &        # Background monitoring
./scripts/interactive-cli.sh  # Interface amigável

# Rotina diária
npm run list           # Ver tasks
npm run complete [task-id]  # Marcar progresso
```

### Time Médio (4-10 devs)
```bash
# Setup completo
./install.sh
npm run watch &
./scripts/weekly-cleanup.sh  # Agendado

# Integrações
# + CI/CD validation
# + Slack notifications  
# + Dashboard básico

# Rotina semanal
./scripts/velocity-metrics.sh
./scripts/health-dashboard.sh
```

### Time Grande (10+ devs)
```bash
# Setup enterprise
./install.sh
npm run watch &

# Automação completa
# + Dashboard web integrado
# + Alertas automáticos
# + Métricas avançadas
# + Backup automático
# + Relatórios executivos

# Governança
./scripts/final-validation.sh  # Pre-release
./scripts/full-dashboard.sh    # Stakeholders
```

## 💡 Dicas Práticas e Automação

### Aliases e Shortcuts Essenciais
```bash
# Adicionar ao .bashrc/.zshrc
alias kiro="cd .kiro/scripts"
alias ks="npm run status"
alias kl="npm run list"
alias kc="npm run complete"
alias kr="npm run report"
alias kw="npm run watch"
alias ki="./scripts/interactive-cli.sh"
alias kh="./scripts/health-dashboard.sh"
alias kb="./scripts/backup-tasks.sh"

# Uso:
kl user-auth           # Listar tasks da feature
kc user-auth-1.1       # Marcar task como concluída
ks                     # Ver status geral
```

### Snippets para IDE
```json
// VS Code/Cursor snippets (.vscode/snippets.json)
{
  "kiro-complete": {
    "prefix": "kc",
    "body": ["npm run complete $1"],
    "description": "Mark task as complete"
  },
  "kiro-task-id": {
    "prefix": "ktid",
    "body": ["${1:feature-name}-${2:1}.${3:1}"],
    "description": "Generate task ID format"
  },
  "kiro-task": {
    "prefix": "ktask",
    "body": [
      "- [ ] ${1:1}.${2:1} ${3:Task description}",
      "  - ${4:Subtask details}",
      "  - _Requirements: [${5:1.1}]_",
      "  - _Estimated: ${6:2h}_",
      "  - _Dependencies: [${7:none}]_"
    ],
    "description": "Create task with proper format"
  }
}
```

### Hooks Git Personalizados
```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "🔍 Validating CDD before commit..."

# Verificar task format se houve mudanças em tasks.md
git diff --cached --name-only | grep "tasks\.md$" | while read file; do
    if [[ $file == .kiro/specs/*/tasks.md ]]; then
        feature=$(echo $file | cut -d/ -f3)
        ./scripts/validate-task-format.sh $feature
    fi
done

# Executar limpeza automática leve
./scripts/cleanup-dead-code.sh --quick

echo "✅ CDD validation passed"
```

### Integração com LLMs (Avançada)
```bash
# Script para otimizar contexto para LLMs
#!/bin/bash
# scripts/optimize-llm-context.sh

echo "🤖 Optimizing context for LLMs..."

# Gerar resumo executivo para LLM
cat > llm-context.md << EOF
# CDD Project Context

## Current Status
$(npm run status --silent)

## Active Features
$(npm run list --silent | head -20)

## Recent Progress
$(git log --oneline --since="1 week ago" .kiro/ | head -10)

## Key Patterns
$(ls .kiro/patterns/*.md | head -5 | xargs -I {} basename {} .md)

## Priority Tasks
$(grep -h "^-\s\[ \]" .kiro/specs/*/tasks.md | head -10)
EOF

echo "✅ Context optimized: llm-context.md"
```

## 🚨 Troubleshooting Detalhado

### Sistema de Task IDs
```bash
# Problema: Tasks não seguem formato correto
# Solução:
./scripts/validate-task-format.sh [feature]
# Editar manualmente .kiro/specs/[feature]/tasks.md
# Formato: - [ ] X.Y Description

# Problema: Task IDs não são reconhecidos  
# Solução:
npm run scan --verbose            # Re-escanear
rm .kiro/scripts/tasks-status.json && npm run scan  # Reset cache

# Problema: Gaps na numeração (1.1, 1.3 sem 1.2)
# Solução:
./scripts/renumber-tasks.sh [feature]
```

### Scripts e Automação
```bash
# Problema: Scripts não executam
chmod +x .kiro/scripts/*.sh      # Corrigir permissões
node --version                   # Verificar Node 14+
cd .kiro/scripts && npm install  # Reinstalar deps

# Problema: Watch não funciona
pkill -f "npm run watch"         # Matar processos antigos
npm run watch                    # Reiniciar

# Problema: Backup falha
mkdir -p .kiro/backups           # Criar diretório
ls -la .kiro/backups             # Verificar permissões
```

### Integração com LLMs
```bash
# Problema: LLM não segue padrões
# 1. Verificar .cursorrules atualizado
ls -la .cursorrules
cat .cursorrules | grep -A5 "patterns"

# 2. Regenerar se necessário
# Use: docs/cursorrules-prompt-direto.md

# 3. Verificar patterns estão documentados
ls .kiro/patterns/
cat .kiro/patterns/README.md
```

### Performance e Cache
```bash
# Problema: Scan muito lento
# Usar cache otimizado:
./scripts/optimized-scan.sh

# Limpar cache se corrompido:
rm .kiro/scripts/tasks-cache.json
rm .kiro/scripts/last-scan.timestamp
npm run scan
```

## ✅ Checklist de Qualidade Robusto

### Projeto Bem Configurado ✅
- [ ] Estrutura .kiro completa e validada (`./scripts/final-validation.sh`)
- [ ] Scripts funcionando (`npm run status`)  
- [ ] Task IDs seguem formato `feature-name-X.Y` (`./scripts/validate-task-format.sh`)
- [ ] .cursorrules gerado e atualizado
- [ ] Sistema de backup configurado (`./scripts/backup-tasks.sh`)
- [ ] Housekeeping automático agendado
- [ ] CI/CD integrado com validação CDD

### Feature Bem Documentada ✅
- [ ] requirements.md completo e específico
- [ ] design.md com arquitetura e diagramas
- [ ] tasks.md com plano detalhado usando IDs corretos
- [ ] Patterns aplicáveis identificados e documentados
- [ ] Tarefas escaneadas e validadas (`npm run scan && npm run list [feature]`)

### Desenvolvimento Eficiente ✅
- [ ] LLM seguindo padrões (via .cursorrules)
- [ ] **Tarefas marcadas como concluídas após CADA implementação** (`npm run complete feature-name-X.Y`)
- [ ] Sistema de task IDs funcionando corretamente
- [ ] Progresso visível em relatórios (`npm run status`)
- [ ] Documentação atualizada quando necessário
- [ ] Limpeza regular executada (`./scripts/weekly-cleanup.sh`)

### Qualidade e Manutenção ✅
- [ ] Código segue patterns definidos (verificação automática)
- [ ] Sem código morto ou dependências orfãs
- [ ] Documentação sem placeholders
- [ ] Tasks sem gaps na numeração
- [ ] Backups regulares funcionando
- [ ] Métricas de velocidade e qualidade coletadas

---

> **Resultado**: Workflow robusto e automatizado onde documentação, implementação, progresso e qualidade estão perfeitamente sincronizados, com máxima eficiência para humanos e LLMs, incluindo sistema completo de task tracking, backup/recovery, housekeeping automático e métricas avançadas. 