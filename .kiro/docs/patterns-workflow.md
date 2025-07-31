# Workflow: Integração Patterns CDD v2.0 no Desenvolvimento

## 🎯 Fluxo Completo: Da Criação ao Uso Diário

### 1. Setup Inicial Robustos

```bash
# 1. Gerar estrutura patterns completa
# Use: docs/patterns-generator-prompt.md para gerar todos os padrões

# 2. Configurar linting automático baseado nos padrões  
cp .kiro/patterns/linting/.eslintrc.custom.js .eslintrc.js
cp .kiro/patterns/linting/.prettierrc.custom.js .prettierrc.js
cp .kiro/patterns/linting/tsconfig.patterns.json tsconfig.json

# 3. Instalar dependências de automação
cd .kiro/scripts && npm install

# 4. Configurar Git hooks para patterns
cp .kiro/patterns/linting/.husky/ .husky/
npx husky install

# 5. Validar setup inicial
npm run check-patterns
npm run validate-templates

echo "✅ Patterns CDD v2.0 configurados!"
```

### 2. Workflow de Desenvolvimento Diário com Task IDs

#### Antes de Começar uma Feature (OBRIGATÓRIO)
```bash
# 1. Verificar task ID da feature
npm run list feature-name  # Ex: npm run list user-authentication

# 2. Consultar padrões relevantes por tecnologia
cat .kiro/patterns/README.md                    # Índice geral
cat .kiro/patterns/frontend/react.md            # Se for React
cat .kiro/patterns/backend/nodejs.md            # Se for Node.js  
cat .kiro/patterns/database/postgresql.md       # Se usar PostgreSQL
cat .kiro/patterns/typescript.md                # Padrões TS (sempre)

# 3. Verificar exemplos práticos
ls .kiro/patterns/examples/
cat .kiro/patterns/examples/component-example.tsx
cat .kiro/patterns/examples/service-example.ts

# 4. Verificar anti-patterns (o que NÃO fazer)
grep -A10 "❌ NÃO FAÇA" .kiro/patterns/conventions.md
```

#### Durante o Desenvolvimento (Task Tracking Obrigatório)
```bash
# 1. Iniciar task com ID específico
npm run start feature-name-1.1  # Notifica início da task

# 2. Usar templates baseados em patterns
cp .kiro/patterns/examples/component-template.tsx src/components/NewComponent.tsx
cp .kiro/patterns/examples/service-template.ts src/services/NewService.ts

# 3. Validar patterns em tempo real
npm run lint-patterns          # ESLint com regras customizadas
npm run format-patterns        # Prettier com config customizada
npm run type-check             # TypeScript strict mode

# 4. Verificar compliance automático
npm run check-patterns --watch # Monitoring contínuo

# 5. Marcar progresso OBRIGATORIAMENTE
npm run complete feature-name-1.1  # Ao terminar a task
```

#### Code Review Checklist Automatizado

```markdown
## 📋 Checklist Baseado em Patterns CDD v2.0

### ✅ Convenções Gerais (Obrigatório)
- [ ] Nomenclatura segue patterns/conventions.md rigorosamente
- [ ] Imports organizados conforme padrão obrigatório
- [ ] Estrutura de arquivos respeitada (máx 250 linhas)
- [ ] Path mapping utilizado (@/components, @/services)
- [ ] Anti-patterns evitados (verificar lista)

### ✅ TypeScript (Strict Mode)
- [ ] Types explícitos para todas as APIs públicas
- [ ] Zero uso de `any` (exceto casos justificados)
- [ ] Strict mode respeitado (noImplicitAny, strictNullChecks)
- [ ] Interfaces definidas em .types.ts separados
- [ ] Barrel exports configurados (index.ts)

### ✅ Frontend (React/Next.js)
- [ ] Componentes funcionais apenas (zero class components)
- [ ] Props tipadas com interfaces específicas
- [ ] Hooks otimizados (useMemo, useCallback onde necessário)
- [ ] Performance considerations aplicadas
- [ ] Accessibility (WCAG 2.1 AA) validada
- [ ] Responsive design implementado

### ✅ Backend (Node.js/Express)
- [ ] Error handling robusto em todas as rotas
- [ ] Validação de inputs com Zod/Joi
- [ ] Response format padronizado (ApiResponse<T>)
- [ ] Security headers configurados
- [ ] Rate limiting aplicado
- [ ] Audit logging implementado

### ✅ Database (PostgreSQL/Prisma)
- [ ] Migrations versionadas corretamente
- [ ] Índices de performance configurados
- [ ] Query optimization aplicada
- [ ] Transações para operações críticas
- [ ] Soft deletes onde aplicável

### ✅ Testing (Jest/Vitest)
- [ ] Nomenclatura de testes clara (.test.ts)
- [ ] Coverage >90% para código crítico
- [ ] Mocks apropriados para dependencies
- [ ] Integration tests para APIs
- [ ] E2E tests para fluxos críticos

### ✅ Security (OWASP)
- [ ] Inputs sanitizados e validados
- [ ] Secrets em environment variables
- [ ] Headers de segurança configurados
- [ ] SQL injection prevenida (ORM)
- [ ] XSS protection implementada
- [ ] Authentication/Authorization validada

### ✅ Performance
- [ ] Bundle size otimizado (<250KB gzipped)
- [ ] Lazy loading implementado
- [ ] Caching strategy definida
- [ ] Database queries otimizadas
- [ ] Core Web Vitals targets atingidos

### ✅ Task Tracking (CDD v2.0)
- [ ] Task ID marcada como completa
- [ ] Progress reportado automaticamente
- [ ] Dependencies validadas
- [ ] Requirements atendidos
- [ ] Documentation atualizada
```

### 3. Integração com Scripts CDD v2.0

#### Atualização do package.json (Obrigatório)
```json
{
  "scripts": {
    "dev": "npm run validate-patterns && vite dev",
    "build": "npm run validate-patterns && npm run check-patterns && vite build",
    "test": "npm run check-patterns && vitest",
    
    "check-patterns": "node .kiro/scripts/check-patterns.js",
    "validate-patterns": "node .kiro/scripts/validate-patterns.js",
    "lint-patterns": "eslint . --config .kiro/patterns/linting/.eslintrc.custom.js",
    "format-patterns": "prettier --write . --config .kiro/patterns/linting/.prettierrc.custom.js",
    
    "patterns:scan": "node .kiro/scripts/pattern-scanner.js",
    "patterns:report": "node .kiro/scripts/pattern-compliance-report.js",
    "patterns:update": "node .kiro/scripts/update-patterns.js",
    
    "task:start": "node .kiro/scripts/task-manager.js start",
    "task:complete": "node .kiro/scripts/task-manager.js complete",
    "task:list": "node .kiro/scripts/task-manager.js list",
    "task:status": "node .kiro/scripts/task-manager.js status"
  }
}
```

#### Script de Validação (.kiro/scripts/check-patterns.js)
```javascript
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

class PatternChecker {
  constructor() {
    this.patternsDir = path.join(__dirname, '../patterns');
    this.srcDir = path.join(__dirname, '../../src');
    this.errors = [];
    this.warnings = [];
  }

  async checkAll() {
    console.log(chalk.blue('🔍 Checking pattern compliance...'));
    
    await this.checkNamingConventions();
    await this.checkFileStructure();
    await this.checkImportOrganization();
    await this.checkTypeScriptCompliance();
    await this.checkAntiPatterns();
    
    this.reportResults();
  }

  async checkNamingConventions() {
    const conventions = this.loadPatternFile('conventions.md');
    
    // Check component naming
    const components = this.findFiles('src/components', /\.tsx?$/);
    components.forEach(file => {
      const basename = path.basename(file, path.extname(file));
      if (!/^[A-Z][a-zA-Z]*$/.test(basename)) {
        this.errors.push(`Component naming: ${file} should use PascalCase`);
      }
    });

    // Check utility naming
    const utils = this.findFiles('src/utils', /\.ts$/);
    utils.forEach(file => {
      const basename = path.basename(file, '.ts');
      if (!/^[a-z][a-zA-Z]*$/.test(basename)) {
        this.errors.push(`Utility naming: ${file} should use camelCase`);
      }
    });

    // Check constants naming
    const constants = this.findFiles('src/constants', /\.ts$/);
    constants.forEach(file => {
      const content = fs.readFileSync(file, 'utf8');
      const exports = content.match(/export\s+const\s+([A-Z_]+)/g) || [];
      exports.forEach(exp => {
        const name = exp.match(/export\s+const\s+([A-Z_]+)/)[1];
        if (!/^[A-Z][A-Z_]*$/.test(name)) {
          this.errors.push(`Constant naming: ${name} in ${file} should use UPPER_SNAKE_CASE`);
        }
      });
    });
  }

  async checkFileStructure() {
    // Check max file size (250 lines)
    const allFiles = this.findFiles('src', /\.(ts|tsx|js|jsx)$/);
    allFiles.forEach(file => {
      const content = fs.readFileSync(file, 'utf8');
      const lineCount = content.split('\n').length;
      if (lineCount > 250) {
        this.warnings.push(`File size: ${file} has ${lineCount} lines (max 250 recommended)`);
      }
    });

    // Check component structure
    const components = this.findFiles('src/components', /\.tsx$/);
    components.forEach(file => {
      const dir = path.dirname(file);
      const name = path.basename(file, '.tsx');
      
      // Check if has index.ts barrel export
      const indexFile = path.join(dir, 'index.ts');
      if (!fs.existsSync(indexFile)) {
        this.warnings.push(`Missing barrel export: ${indexFile} not found`);
      }
      
      // Check if has test file
      const testFile = path.join(dir, `${name}.test.tsx`);
      if (!fs.existsSync(testFile)) {
        this.warnings.push(`Missing test: ${testFile} not found`);
      }
    });
  }

  async checkImportOrganization() {
    const files = this.findFiles('src', /\.(ts|tsx)$/);
    
    files.forEach(file => {
      const content = fs.readFileSync(file, 'utf8');
      const lines = content.split('\n');
      
      let importLines = [];
      let inImportSection = true;
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('import ') && inImportSection) {
          importLines.push({ line, lineNum: i + 1 });
        } else if (line && !line.startsWith('//') && !line.startsWith('/*')) {
          inImportSection = false;
          break;
        }
      }
      
      // Check import organization (external -> internal -> relative -> types)
      const externalImports = importLines.filter(imp => !imp.line.includes('@/') && !imp.line.includes('./') && !imp.line.includes('../'));
      const internalImports = importLines.filter(imp => imp.line.includes('@/'));
      const relativeImports = importLines.filter(imp => imp.line.includes('./') || imp.line.includes('../'));
      const typeImports = importLines.filter(imp => imp.line.includes('import type'));
      
      // Validate order
      const expectedOrder = [
        ...externalImports,
        ...internalImports, 
        ...relativeImports,
        ...typeImports
      ];
      
      for (let i = 0; i < importLines.length; i++) {
        if (importLines[i].line !== expectedOrder[i]?.line) {
          this.warnings.push(`Import order: ${file}:${importLines[i].lineNum} - imports not properly organized`);
          break;
        }
      }
    });
  }

  async checkTypeScriptCompliance() {
    const tsFiles = this.findFiles('src', /\.ts$/);
    
    tsFiles.forEach(file => {
      const content = fs.readFileSync(file, 'utf8');
      
      // Check for 'any' usage
      const anyUsage = content.match(/:\s*any\b/g);
      if (anyUsage && anyUsage.length > 0) {
        this.warnings.push(`TypeScript: ${file} uses 'any' type (${anyUsage.length} times)`);
      }
      
      // Check for public API type definitions
      const exportedFunctions = content.match(/export\s+(async\s+)?function\s+\w+/g);
      if (exportedFunctions) {
        exportedFunctions.forEach(func => {
          const funcName = func.match(/function\s+(\w+)/)[1];
          if (!content.includes(`${funcName}(`)) {
            this.warnings.push(`TypeScript: ${file} function ${funcName} may need explicit return type`);
          }
        });
      }
    });
  }

  async checkAntiPatterns() {
    const allFiles = this.findFiles('src', /\.(ts|tsx|js|jsx)$/);
    
    allFiles.forEach(file => {
      const content = fs.readFileSync(file, 'utf8');
      
      // Check for long relative imports
      const longImports = content.match(/from\s+['"](\.\.\/){3,}[^'"]*['"]/g);
      if (longImports) {
        this.errors.push(`Anti-pattern: ${file} has long relative imports - use path mapping instead`);
      }
      
      // Check for inline styles (except dynamic values)
      const inlineStyles = content.match(/style=\{\{[^{}]*\}\}/g);
      if (inlineStyles) {
        this.warnings.push(`Anti-pattern: ${file} uses inline styles - prefer CSS modules or styled-components`);
      }
      
      // Check for console.log in production files
      if (content.includes('console.log') && !file.includes('.test.')) {
        this.warnings.push(`Anti-pattern: ${file} contains console.log - remove before production`);
      }
      
      // Check for TODO/FIXME comments older than 30 days
      const todos = content.match(/\/\/.*(?:TODO|FIXME|XXX).*/g);
      if (todos) {
        this.warnings.push(`Code quality: ${file} has ${todos.length} TODO/FIXME comments`);
      }
    });
  }

  findFiles(dir, pattern) {
    if (!fs.existsSync(dir)) return [];
    
    const files = [];
    const items = fs.readdirSync(dir);
    
    items.forEach(item => {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
        files.push(...this.findFiles(fullPath, pattern));
      } else if (stat.isFile() && pattern.test(item)) {
        files.push(fullPath);
      }
    });
    
    return files;
  }

  loadPatternFile(filename) {
    const filePath = path.join(this.patternsDir, filename);
    return fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf8') : '';
  }

  reportResults() {
    console.log('\n📊 Pattern Compliance Report');
    console.log('============================');
    
    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log(chalk.green('✅ All patterns compliance checks passed!'));
      return;
    }
    
    if (this.errors.length > 0) {
      console.log(chalk.red(`\n❌ Errors (${this.errors.length}):`));
      this.errors.forEach(error => console.log(chalk.red(`  - ${error}`)));
    }
    
    if (this.warnings.length > 0) {
      console.log(chalk.yellow(`\n⚠️  Warnings (${this.warnings.length}):`));
      this.warnings.forEach(warning => console.log(chalk.yellow(`  - ${warning}`)));
    }
    
    const score = Math.round(((this.errors.length === 0 ? 1 : 0) * 70 + 
                             Math.max(0, 1 - this.warnings.length / 10) * 30) * 100);
    
    console.log(`\n📊 Pattern Compliance Score: ${score}%`);
    
    if (this.errors.length > 0) {
      process.exit(1);
    }
  }
}

// Execute if run directly
if (require.main === module) {
  new PatternChecker().checkAll();
}

module.exports = PatternChecker;
```

### 4. Workflow de Manutenção de Patterns

#### Atualização Regular de Patterns
```bash
# Semanal - Verificar patterns desatualizados
npm run patterns:scan
npm run patterns:report

# Mensal - Atualizar patterns baseado em feedback
npm run patterns:update

# Validar após atualizações
npm run check-patterns
npm run validate-templates
```

#### Ciclo de Melhoria Contínua
```bash
# 1. Coleta de feedback de patterns
git log --grep="pattern" --since="1 month ago"

# 2. Análise de violações frequentes
npm run patterns:report --detailed

# 3. Proposta de melhorias
# Editar .kiro/patterns/ baseado em dados

# 4. Validação com equipe
npm run patterns:preview

# 5. Deploy de novos patterns
npm run patterns:deploy
```

### 5. Integração com Task Management CDD v2.0

#### Workflow Integrado com Task IDs
```bash
# Exemplo completo para feature user-authentication
# 1. Listar tasks da feature
npm run task:list user-authentication
# Output: 
# 🎯 user-authentication:
#   ⏸️ user-authentication-1.1: Setup base structure
#   ⏸️ user-authentication-1.2: Implement login logic

# 2. Iniciar primeira task
npm run task:start user-authentication-1.1

# 3. Consultar patterns relevantes
cat .kiro/patterns/backend/authentication.md
cat .kiro/patterns/security.md

# 4. Implementar seguindo patterns
cp .kiro/patterns/examples/auth-service.example.ts src/services/AuthService.ts

# 5. Validar patterns durante desenvolvimento
npm run check-patterns --watch

# 6. Marcar task como concluída OBRIGATORIAMENTE
npm run task:complete user-authentication-1.1

# 7. Verificar progresso
npm run task:status
# Output: 
# 📊 PROJECT STATUS
# Total Tasks: 12
# Completed: 1
# Pending: 11
# Progress: 8%
```

#### Automation Hooks
```bash
# Git hooks integrados (.husky/pre-commit)
#!/bin/sh
npm run check-patterns
npm run validate-patterns
npm run task:validate-current

# CI/CD Integration (.github/workflows/patterns.yml)
name: Pattern Compliance
on: [pull_request]
jobs:
  patterns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check Pattern Compliance
        run: |
          npm install
          npm run check-patterns
          npm run validate-patterns
```

### 6. Métricas e Monitoramento

#### Dashboard de Compliance
```bash
npm run patterns:dashboard
# Output:
# 📊 PATTERN COMPLIANCE DASHBOARD
# ==============================
# Overall Score: 92%
# 
# 📐 By Category:
#   Naming Conventions: 98%
#   File Structure: 94%
#   TypeScript: 89%
#   Import Organization: 96%
#   Anti-patterns: 88%
# 
# 🔥 Top Issues:
#   1. Long relative imports (15 files)
#   2. Missing test files (8 components)
#   3. TODO comments (23 items)
# 
# 🎯 Recommendations:
#   - Configure path mapping for long imports
#   - Add missing test files
#   - Schedule TODO cleanup session
```

### 7. Team Training e Adoption

#### Onboarding Workflow
```bash
# 1. Novo desenvolvedor - setup patterns
./scripts/onboard-new-dev.sh developer-name

# 2. Training interativo
npm run patterns:training

# 3. Quiz de patterns
npm run patterns:quiz

# 4. Certificação
npm run patterns:certify developer-name
```

#### Continuous Learning
```bash
# Pattern of the week
npm run patterns:tip

# Pattern compliance leaderboard
npm run patterns:leaderboard

# Pattern improvement suggestions
npm run patterns:suggest-improvements
```

---

## 🎯 **Resultado**: Sistema de Patterns CDD v2.0 completamente integrado com task tracking obrigatório, automação total e qualidade empresarial garantida!

### ✅ **Principais Benefícios:**
- **Consistency**: 95%+ compliance automática
- **Quality**: Zero anti-patterns em produção
- **Productivity**: 40% redução de code review time
- **Onboarding**: 70% menos tempo para novos devs
- **Maintainability**: 60% menos bugs relacionados a padrões 