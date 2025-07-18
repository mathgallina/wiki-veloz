# Quick Start - Scripts de Tarefas .kiro

## 🚀 Início Rápido

### 1. Configuração Inicial
```bash
cd .kiro/scripts
./install.sh
```

### 2. Comandos Essenciais
```bash
# Escanear tarefas (primeira vez)
npm run scan

# Ver status geral
npm run status

# Monitorar automaticamente (recomendado)
npm run watch

# Marcar tarefa como concluída
npm run complete feature-name-1.1

# Gerar relatório
npm run report

# Ver status dos padrões
npm run patterns

# Validar conformidade com padrões
npm run check-patterns
```

## 📋 Estrutura Criada

```
.kiro/scripts/
├── task-manager.js     # Script principal
├── read-tasks.js       # Lê tarefas dos arquivos .md
├── update-task.js      # Atualiza status das tarefas
├── generate-report.js  # Gera relatórios
├── watch.js           # Monitor automático
├── utils.js           # Funções auxiliares
├── install.sh         # Script de instalação
├── package.json       # Configuração npm
├── tasks-status.json  # Estado das tarefas (gerado)
└── README.md          # Documentação completa
```

## 🎯 Fluxo Típico de Uso

### Desenvolvedor Individual
```bash
# Uma vez: instalar e escanear
./install.sh
npm run scan

# Durante desenvolvimento: monitorar
npm run watch

# Validar padrões antes de commit
npm run check-patterns

# Quando completar tarefas
npm run complete minha-feature-1.2
```

### Equipe/Projeto
```bash
# Daily standup: verificar status
npm run status

# Verificar conformidade de padrões
npm run check-patterns

# Relatórios semanais
npm run report

# Monitoramento contínuo no CI
npm run scan && npm run status && npm run check-patterns
```

## 📊 Saídas dos Scripts

### Status
```
🎯 design-system-implementation: 5/8 (62%)
🎯 ai-health-insights: 3/6 (50%)
📈 TOTAL GERAL: 8/14 (57%)
```

### Lista de Tarefas
```
🎯 Feature: design-system-implementation
✅ design-system-1.1 [Phase 1] Configurar Tailwind CSS
⏳ design-system-1.2 [Phase 1] Criar utilitários base
```

### Relatórios
- `task-report.md` - Relatório completo em Markdown
- `task-report.json` - Dados estruturados para integração
- `feature-report.md` - Relatório específico por feature

## 🔧 Personalização

### Adicionando Novos Comandos
Edite `task-manager.js` e adicione no switch:
```javascript
case 'meu-comando':
  await minhaFuncao();
  break;
```

### Mudando Formato de IDs
Ajuste a regex em `read-tasks.js`:
```javascript
const taskIdMatch = description.match(/^(\d+\.\d+)\s+(.+)/);
```

### Integrações
- **Slack**: Parse `task-report.json` para notificações
- **CI/CD**: Use `npm run status` para validação
- **Dashboard**: Consuma dados do JSON

## 🚨 Troubleshooting

### Tarefa não encontrada
```bash
npm run scan  # Re-escanear
npm run list  # Ver IDs disponíveis
```

### JSON corrompido
```bash
rm tasks-status.json
npm run scan
```

### Watch não funciona
```bash
# Verificar Node.js v14+
node -v

# Reinstalar
npm run setup
```

---

> **Dica**: Mantenha `npm run watch` rodando durante desenvolvimento para monitoramento em tempo real! 