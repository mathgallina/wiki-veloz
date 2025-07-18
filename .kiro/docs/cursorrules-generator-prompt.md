# Generator: .cursorrules CDD v2.0 (Inteligente)

## 🎯 Objetivo
Gerar `.cursorrules` conciso e automatizado analisando `.kiro/` para máxima produtividade.

---

## 📋 PROMPT PARA IA

```markdown
Analise .kiro/ e gere .cursorrules conciso (150-200 linhas) com automação máxima.

### ANÁLISE AUTOMÁTICA:
1. **Steering** → extrair: domínio, stack, objetivos
2. **Patterns** → extrair: convenções rigorosas, anti-patterns  
3. **Specs** → extrair: task IDs ativos, features prioritárias
4. **Scripts** → extrair: comandos essenciais

### TEMPLATE CONCISO:

```markdown
# .cursorrules - CDD v2.0 Auto

## 🎯 PROJETO
**Domínio**: [EXTRAIR]
**Stack**: [EXTRAIR stack completo]
**Task Format**: feature-name-X.Y

## 📐 REGRAS AUTO-APLICADAS

### Convenções (ESLint enforced):
```typescript
✅ SEMPRE: [padrões de conventions.md]
❌ NUNCA: [anti-patterns específicos]
```

### Stack Patterns:
```typescript
// [FRONTEND_STACK] - ex: React/Next.js
✅ Functional components, tipos explícitos, hooks otimizados
❌ Class components, any types, inline styles

// [BACKEND_STACK] - ex: Node.js/Express
✅ Error handling robusto, validation rigorosa, audit logging
❌ Errors não tratados, inputs sem validação, hardcoded secrets

// [DATABASE_STACK] - ex: PostgreSQL/Prisma
✅ Migrations versionadas, queries otimizadas, indexes adequados
❌ Raw SQL sem sanitização, N+1 queries, missing indexes
```

## 🤖 AUTOMAÇÃO INTEGRADA

### Workflow Obrigatório:
```bash
ANTES: npm run list [feature] && npm run start [task-id]
DURANTE: npm run check-patterns (auto-executar se errors)
APÓS: npm run complete [task-id] (OBRIGATÓRIO)
```

### Scripts Auto-Trigger:
- **Linting errors** → npm run lint --fix
- **Task sem ID** → npm run list para mostrar opções
- **Pattern violations** → npm run check-patterns
- **Code smells** → ./scripts/cleanup-dead-code.sh

## 🧠 DECISÕES LLM

### Autônomas (não perguntar):
- Aplicar patterns de .kiro/patterns/
- Corrigir linting automaticamente
- Organizar imports conforme convenções
- Implementar error handling padrão
- Adicionar tipos TypeScript rigorosos

### Consultar usuário:
- Decisões arquiteturais significativas
- Business rules não documentadas
- Trade-offs performance vs simplicidade
- Integrações com APIs externas

## ⚡ TRIGGERS INTELIGENTES

### Auto-detectar contexto:
```typescript
Se (.tsx + useState) → aplicar React patterns
Se (/api/ route) → aplicar backend security patterns  
Se (database query) → aplicar performance patterns
Se (nova feature) → verificar task ID obrigatório
```

### Auto-executar scripts:
```bash
Ao completar implementação → npm run complete [detectar task-id]
Ao detectar violations → npm run check-patterns
Ao identificar cleanup → ./scripts/cleanup-dead-code.sh
Ao encontrar security issues → npm run security:scan
```

## 🎯 COMPLIANCE AUTO

- **Task Tracking**: 100% obrigatório
- **Type Safety**: Zero any types
- **Security**: Patterns aplicados automaticamente
- **Performance**: Otimizações padrão sempre
- **Testing**: Coverage mínimo [EXTRAIR de patterns]

---

**Estado Atual**: [EXTRAIR de tasks-status.json se existir]
**Next Priority**: [EXTRAIR próxima task pendente]
```

### RESULTADO: .cursorrules que atua como developer experiente:
1. **Detecta contexto** automaticamente
2. **Aplica patterns** sem confirmação  
3. **Executa scripts** no momento certo
4. **Resolve problemas** autonomamente
5. **Mantém compliance** continuamente
```

## 🎯 Características

### ✅ **Concisão Máxima:**
- 150-200 linhas (vs 500+ anterior)
- Foco no essencial
- Zero redundância
- Informação densa

### 🤖 **Automação Inteligente:**
- Context detection automática
- Script triggering baseado em situações
- Pattern application sem confirmação
- Problem resolution autônoma

### ⚡ **Eficiência Total:**
- Regras que se ativam quando necessário
- Comandos que executam automaticamente
- Validações que rodam em background
- Troubleshooting que se resolve sozinho

---

**Versão**: 2.0.0 Conciso  
**Target**: Máxima automação, mínima verbosidade  
**Resultado**: Expert developer automatizado 