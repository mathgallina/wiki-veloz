# Scripts de Gerenciamento de Tarefas .kiro

Este diretório contém scripts para gerenciar e monitorar as tarefas definidas nas specs do projeto .kiro.

> 🚀 **Início Rápido**: Veja [quick-start.md](quick-start.md) para começar imediatamente!

## 🛠️ Scripts Disponíveis

### 📋 task-manager.js
**Script principal para gerenciar tarefas**

```bash
# Escanear todas as tarefas
node task-manager.js scan
npm run scan

# Ver status geral
node task-manager.js status
npm run status

# Listar tarefas
node task-manager.js list
node task-manager.js list design-system  # filtrar por feature

# Marcar tarefa como concluída
node task-manager.js complete design-system-1.1
npm run complete design-system-1.1

# Ver status dos padrões de código
node task-manager.js patterns
npm run patterns

# Verificar conformidade com padrões
node check-patterns.js
npm run check-patterns

# Ajuda
node task-manager.js help
```

### 📊 generate-report.js
**Gerador de relatórios**

```bash
# Relatório completo em Markdown
node generate-report.js
npm run report

# Relatório em JSON
node generate-report.js --json

# Relatório de feature específica
node generate-report.js --feature design-system
```

### 👀 watch.js
**Monitor automático de mudanças**

```bash
# Monitorar mudanças automaticamente
node watch.js
npm run watch

# Para monitoramento em background
npm run watch &
```

### 📐 check-patterns.js
**Validador de conformidade com padrões**

```bash
# Verificação completa de padrões
node check-patterns.js
npm run check-patterns

# Verificar apenas nomenclatura
node check-patterns.js --naming

# Verificar apenas ordem de imports
node check-patterns.js --imports

# Verificar apenas padrões TypeScript
node check-patterns.js --types
```

## 📐 Funcionalidades de Patterns

### Status dos Padrões
```bash
# Ver se patterns estão configurados
npm run patterns
```

### Validação de Conformidade
```bash
# Verificar se o código segue os padrões estabelecidos
npm run check-patterns

# Verificações específicas
npm run check-patterns --naming     # Nomenclatura
npm run check-patterns --imports    # Ordem de imports  
npm run check-patterns --types      # Padrões TypeScript
```

### Integração com Relatórios
Os relatórios agora incluem automaticamente:
- Status dos patterns configurados
- Recomendações baseadas nos padrões
- Sugestões para configurar patterns se não existirem

## 📁 Arquivos de Estado

### tasks-status.json
Arquivo central que mantém o estado atualizado de todas as tarefas:

```json
{
  "lastUpdated": "2024-01-15T10:30:00.000Z",
  "tasks": {
    "design-system-implementation": [
      {
        "id": "design-system-1.1",
        "description": "Configurar Tailwind CSS",
        "completed": true,
        "phase": "Phase 1: Foundation",
        "file": "tasks.md",
        "lineNumber": 15,
        "subtasks": [...]
      }
    ]
  }
}
```

## 🚀 Setup Inicial

### 1. Instalação
```bash
cd .kiro/scripts
./install.sh
# ou
npm run setup
```

### 2. Primeira Execução Manual
```bash
npm run scan
```

## 🔄 Workflow de Uso

### 2. Monitoramento Contínuo (Recomendado)
```bash
# Inicia monitoramento automático
npm run watch
```

### 3. Monitoramento Manual
```bash
npm run status
```

### 4. Marcando Tarefas como Concluídas
```bash
npm run complete feature-name-X.Y
```

### 5. Validação de Padrões
```bash
npm run check-patterns
```

### 6. Relatórios Periódicos
```bash
npm run report
```

## ⚙️ Funcionamento Interno

### Leitura de Tarefas
- **read-tasks.js** escaneia todos os arquivos `tasks.md` em `.kiro/specs/`
- Identifica fases, tarefas principais e subtarefas
- Gera IDs únicos no formato `feature-X.Y`
- Extrai informações de linha para edição posterior

### Atualização de Status
- **update-task.js** localiza tarefas por ID
- Modifica os checkboxes `[ ]` para `[x]` nos arquivos originais
- Marca subtarefas automaticamente quando tarefa principal é concluída
- Preserva formatação e comentários

### Estado Centralizado
- **tasks-status.json** mantém estado sincronizado
- Permite queries rápidas sem reprocessar arquivos
- Inclui metadados como timestamps e localização
- **watch.js** monitora mudanças em tempo real e atualiza automaticamente

## 📊 Formato de IDs de Tarefas

```
feature-name-X.Y

Onde:
- feature-name: nome da pasta em .kiro/specs/
- X.Y: número da tarefa (ex: 1.1, 2.3)

Exemplos:
- design-system-implementation-1.1
- ai-health-insights-2.4
- user-authentication-3.2
```

## 🚨 Resolução de Problemas

### Tarefa não encontrada
```bash
# Re-escanear tarefas
npm run scan

# Verificar ID correto
npm run list
```

### Arquivo não atualizado
- Verificar permissões de escrita
- Confirmar formato correto do tasks.md
- Validar estrutura de checkboxes

### JSON corrompido
```bash
# Deletar e regenerar
rm tasks-status.json
npm run scan
```

## 📈 Métricas Disponíveis

- **Por Feature**: Total, concluídas, progresso
- **Geral**: Todas as features combinadas
- **Temporal**: Histórico de atualizações
- **Detalhes**: Subtarefas e fases

## 🔧 Personalização

### Adicionando Novos Comandos
Edite `task-manager.js` e adicione novos cases no switch.

### Modificando Formato de Relatórios
Ajuste `generate-report.js` e `utils.js` para novos formatos.

### Integrações
- **CI/CD**: Use `npm run status` para verificar progresso
- **Slack/Discord**: Parse do JSON para notificações
- **Dashboards**: Consuma `task-report.json`
- **IDEs**: Use `npm run watch` durante desenvolvimento
- **Automação**: Monitore `tasks-status.json` para triggers

---

> **Dica**: Use `npm run watch` durante desenvolvimento para monitoramento automático, ou `npm run scan` após modificar arquivos tasks.md manualmente. 