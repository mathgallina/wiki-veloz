# Exemplo: .cursorrules CDD v2.0 Conciso

## 🎯 Preview do Resultado Inteligente

Exemplo de `.cursorrules` **conciso e automatizado** (150-200 linhas vs 500+):

---

```markdown
# .cursorrules - CDD v2.0 Auto

## 🎯 PROJETO
**Domínio**: HealthTech (HIPAA compliance)
**Stack**: React 18 + Next.js 14 + TypeScript + PostgreSQL + Prisma
**Task Format**: health-feature-X.Y

## 📐 REGRAS AUTO-APLICADAS

### Convenções (ESLint enforced):
```typescript
✅ SEMPRE:
- PascalCase: Components (HealthDashboard.tsx)
- camelCase: functions (calculateBMI)
- kebab-case: files (user-profile.ts)
- Zero any types (TypeScript strict 100%)

❌ NUNCA:
- Class components, inline styles
- Hardcoded secrets, missing validation
- PHI data sem encryption
```

### Stack Patterns:
```typescript
// React/Next.js
✅ Functional components, explicit types, performance hooks
✅ Error boundaries, loading states, accessibility
❌ Class components, any types, >250 lines per component

// Node.js/Express  
✅ Input validation (Zod), error handling, audit logging
✅ JWT auth, security headers, HIPAA compliance
❌ Missing auth, unvalidated inputs, PHI exposure

// PostgreSQL/Prisma
✅ Indexed queries, transactions, encrypted PHI
✅ Migrations, optimized aggregations
❌ Raw SQL, N+1 queries, unencrypted sensitive data
```

## 🤖 AUTOMAÇÃO INTEGRADA

### Workflow (Auto-executar):
```bash
ANTES: npm run list health-tracking
INICIAR: npm run start health-tracking-2.1  
VALIDAR: npm run check-patterns (se violations detectadas)
COMPLETAR: npm run complete health-tracking-2.1 (OBRIGATÓRIO)
```

### Auto-Triggers:
- **Linting errors** → npm run lint --fix
- **Security issues** → npm run security:scan  
- **Performance problems** → otimizações automáticas
- **Missing task ID** → npm run list para sugerir
- **Code smells** → ./scripts/cleanup-dead-code.sh

## 🧠 DECISÕES LLM

### Autônomas (não interromper usuário):
- Aplicar HIPAA patterns para health data
- Corrigir imports/exports automaticamente
- Adicionar error handling padrão
- Implementar TypeScript strict compliance
- Organizar file structure conforme patterns

### Consultar para:
- Nova integração health APIs
- Mudanças em business rules médicas
- Performance vs security tradeoffs
- Compliance requirements específicos

## ⚡ TRIGGERS INTELIGENTES

### Context Detection:
```typescript
/health/ → HIPAA patterns + PHI encryption
.tsx + useState → React performance patterns
/api/ → security headers + input validation
database queries → optimization + indexes
new feature → task ID obrigatório
```

### Script Execution:
```bash
Implementação completa → npm run complete [auto-detect-task-id]
Pattern violations → npm run check-patterns  
Dead code detected → ./scripts/cleanup-dead-code.sh
Security scan needed → npm run security:scan
Performance issues → otimizações automáticas
```

## 🎯 COMPLIANCE AUTO

- **HIPAA**: PHI encryption + audit logging (100%)
- **TypeScript**: Zero any types (strict mode)
- **Security**: OWASP patterns + security headers
- **Performance**: <2.5s LCP, <250KB bundle
- **Testing**: 90%+ coverage health business logic
- **Accessibility**: WCAG 2.1 AA compliance

## 🔄 ESTADO DINÂMICO

**Ativo**: health-tracking-2.1 (Dashboard visualization)
**Próximo**: health-tracking-2.2 (Metrics analytics)
**Compliance**: 97% patterns, A+ security, HIPAA ✅

---

**Auto-generated** | **v2.0.0** | **Health-optimized** | **97% automation**
```

---

## 📊 Comparação: Verboso vs Conciso

| Aspecto | v1.0 Verboso | v2.0 Conciso |
|---------|-------------|--------------|
| **Linhas** | 500-1000+ | 150-200 |
| **Foco** | Documentação | Automação |
| **Decisões** | Manual | 95% automática |
| **Scripts** | Listados | Auto-executados |
| **Patterns** | Descritos | Auto-aplicados |
| **Validação** | Manual | Contínua |
| **Eficiência** | Média | Máxima |

## 🚀 Exemplo de Interação

### **Antes (Verboso):**
```
User: "Crie um componente de botão"
LLM: "Vou seguir os patterns... [lê 500 linhas]... 
     Primeiro preciso verificar... [pergunta 5 coisas]...
     Aqui está o componente... [implementa]...
     Agora você precisa executar..."
```

### **Depois (Conciso + Inteligente):**
```
User: "Crie um componente de botão"
LLM: [Auto-detecta: design-system-2.1]
     [Auto-aplica: React + TypeScript patterns]
     [Auto-implementa: Button.tsx seguindo conventions]
     [Auto-executa: npm run complete design-system-2.1]
     
     "✅ Button criado seguindo health patterns!
     📈 Task design-system-2.1 marcada como completa
     🎯 Próxima: design-system-2.2 (Input component)"
```

## 🎯 Benefícios da Versão Concisa

### ✅ **Produtividade Máxima:**
- 95% menos perguntas ao usuário
- Automação de decisions rotineiras  
- Scripts executados automaticamente
- Patterns aplicados sem confirmação

### ⚡ **Eficiência Total:**
- Context detection instantânea
- Zero tempo perdido com confirmações
- Troubleshooting automático
- Compliance mantido continuamente

### 🧠 **Inteligência Contextual:**
- Detecta tipo de implementação
- Aplica patterns específicos
- Executa scripts adequados
- Resolve problemas autonomamente

---

**Resultado**: .cursorrules que funciona como senior developer especializado no domínio, com máxima automação e zero overhead! 

**Philosophy**: "Máxima automação, mínima interrupção, total compliance" 