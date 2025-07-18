# Exemplo: Estrutura Patterns CDD v2.0 Completa

Este é um exemplo de como ficaria a pasta `.kiro/patterns/` gerada para um projeto React + Next.js + TypeScript + Node.js + PostgreSQL usando CDD v2.0.

## Estrutura Completa Robusta

```
.kiro/patterns/
├── README.md                    # Índice navegável e overview completo
├── conventions.md               # Convenções rigorosas de nomenclatura
├── architecture.md              # SOLID principles e design patterns
├── typescript.md                # TypeScript strict mode patterns
├── security.md                  # OWASP guidelines e security headers
├── performance.md               # Core Web Vitals e optimization patterns
├── testing.md                   # Testing strategies e coverage requirements
├── error-handling.md            # Error handling patterns e logging
├── accessibility.md             # WCAG 2.1 AA compliance patterns
├── frontend/                    # Padrões específicos do frontend
│   ├── README.md               # Índice de padrões frontend
│   ├── react.md                # React best practices
│   ├── nextjs.md               # Next.js optimization patterns
│   ├── components.md           # Component design patterns
│   ├── state-management.md     # Zustand/Context patterns
│   ├── styling.md              # Tailwind CSS patterns
│   └── forms.md                # Form validation e handling
├── backend/                     # Padrões específicos do backend
│   ├── README.md               # Índice de padrões backend
│   ├── nodejs.md               # Node.js patterns
│   ├── express.md              # Express.js patterns
│   ├── api-design.md           # REST API design patterns
│   ├── middleware.md           # Middleware patterns
│   ├── authentication.md       # JWT e Auth patterns
│   └── caching.md              # Redis caching strategies
├── database/                    # Padrões específicos de banco
│   ├── README.md               # Índice de padrões database
│   ├── postgresql.md           # PostgreSQL optimization patterns
│   ├── prisma.md               # Prisma ORM patterns
│   ├── migrations.md           # Migration patterns e versioning
│   ├── indexing.md             # Index optimization patterns
│   └── transactions.md         # Transaction patterns
├── examples/                    # Templates práticos copy-paste ready
│   ├── README.md               # Índice de templates
│   ├── components/             # Component templates
│   │   ├── Button.example.tsx
│   │   ├── Modal.example.tsx
│   │   ├── Form.example.tsx
│   │   └── DataTable.example.tsx
│   ├── hooks/                  # Custom hooks templates
│   │   ├── useApi.example.ts
│   │   ├── useAuth.example.ts
│   │   └── useLocalStorage.example.ts
│   ├── services/               # Service layer templates
│   │   ├── UserService.example.ts
│   │   ├── ApiClient.example.ts
│   │   └── AuthService.example.ts
│   ├── controllers/            # Controller templates
│   │   ├── UserController.example.ts
│   │   ├── AuthController.example.ts
│   │   └── BaseController.example.ts
│   ├── models/                 # Model/Schema templates
│   │   ├── User.model.ts
│   │   ├── ApiResponse.types.ts
│   │   └── Database.schema.ts
│   ├── tests/                  # Test templates
│   │   ├── component.test.example.tsx
│   │   ├── service.test.example.ts
│   │   ├── api.test.example.ts
│   │   └── e2e.test.example.ts
│   └── configs/                # Configuration templates
│       ├── eslint.config.example.js
│       ├── tailwind.config.example.js
│       └── next.config.example.js
├── linting/                     # Configurações de linting automatizadas
│   ├── README.md               # Setup e uso das configs
│   ├── .eslintrc.custom.js     # ESLint config rigorosa
│   ├── .prettierrc.custom.js   # Prettier config customizada
│   ├── tsconfig.patterns.json  # TypeScript config strict
│   ├── .husky/                 # Git hooks configuration
│   │   ├── pre-commit
│   │   ├── pre-push
│   │   └── commit-msg
│   ├── lint-staged.config.js   # Staged files linting
│   └── quality-gates.js        # Quality validation rules
├── ci-cd/                       # Patterns para CI/CD
│   ├── README.md               # CI/CD setup guide
│   ├── github-actions.yml      # GitHub Actions workflows
│   ├── quality-pipeline.yml    # Quality validation pipeline
│   ├── deploy-pipeline.yml     # Deployment pipeline
│   └── monitoring.yml          # Monitoring setup
└── CHANGELOG.md                 # Versionamento dos patterns
```

## Exemplos de Conteúdo CDD v2.0

### README.md Principal
```markdown
# Code Patterns CDD v2.0 - HealthTracker Pro

## 🎯 Visão Geral
Este diretório contém todos os padrões de código obrigatórios para o projeto HealthTracker Pro.
Baseado na análise de steering, aplicamos rigorosamente os princípios CDD v2.0.

### Stack Identificado
- **Frontend**: React 18, Next.js 14, TypeScript 5.0, Tailwind CSS 3.3
- **Backend**: Node.js 20, Express 4.18, TypeScript 5.0
- **Database**: PostgreSQL 15, Prisma 5.0 ORM
- **Testing**: Jest 29, Vitest, Cypress 13, Testing Library
- **DevOps**: Docker, GitHub Actions, Vercel
- **Monitoring**: Sentry, Vercel Analytics

### Princípios Fundamentais CDD v2.0
1. **Consistency Over Flexibility**: Patterns rigorosos garantem código uniforme
2. **Automation Over Manual**: Linting automático força compliance (95%+ target)
3. **Security By Default**: OWASP patterns aplicados automaticamente
4. **Performance First**: Core Web Vitals como prioridade máxima
5. **Accessibility Always**: WCAG 2.1 AA compliance obrigatória
6. **Task Tracking Integrated**: Coordenação com system de task IDs

## 📚 Índice de Patterns

### 🏗️ Arquitetura e Fundamentos
- [conventions.md](./conventions.md) - Convenções rigorosas PascalCase/camelCase/kebab-case
- [architecture.md](./architecture.md) - SOLID principles, DI, design patterns
- [typescript.md](./typescript.md) - Strict mode, zero any policy, type safety

### 🔒 Qualidade e Segurança Obrigatória
- [security.md](./security.md) - OWASP Top 10, security headers, JWT
- [performance.md](./performance.md) - Core Web Vitals <2.5s LCP, bundle <250KB
- [testing.md](./testing.md) - 90%+ coverage, unit/integration/e2e
- [error-handling.md](./error-handling.md) - Try/catch patterns, logging
- [accessibility.md](./accessibility.md) - WCAG 2.1 AA, screen readers

### 🎨 Frontend Patterns (React/Next.js)
- [frontend/README.md](./frontend/README.md) - Índice frontend completo
- [frontend/react.md](./frontend/react.md) - Hooks, memoization, performance
- [frontend/nextjs.md](./frontend/nextjs.md) - App Router, SSR, optimization
- [frontend/components.md](./frontend/components.md) - Design patterns, props
- [frontend/state-management.md](./frontend/state-management.md) - Zustand patterns
- [frontend/styling.md](./frontend/styling.md) - Tailwind CSS conventions
- [frontend/forms.md](./frontend/forms.md) - React Hook Form + Zod validation

### ⚙️ Backend Patterns (Node.js/Express)
- [backend/README.md](./backend/README.md) - Índice backend completo
- [backend/nodejs.md](./backend/nodejs.md) - Async patterns, error handling
- [backend/express.md](./backend/express.md) - Middleware, routing, security
- [backend/api-design.md](./backend/api-design.md) - REST patterns, validation
- [backend/authentication.md](./backend/authentication.md) - JWT, refresh tokens
- [backend/caching.md](./backend/caching.md) - Redis strategies, invalidation

### 🗄️ Database Patterns (PostgreSQL/Prisma)
- [database/README.md](./database/README.md) - Índice database completo
- [database/postgresql.md](./database/postgresql.md) - Query optimization, indexes
- [database/prisma.md](./database/prisma.md) - Schema design, relations
- [database/migrations.md](./database/migrations.md) - Versioning, rollbacks
- [database/transactions.md](./database/transactions.md) - ACID compliance

### 📝 Templates e Exemplos Funcionais
- [examples/README.md](./examples/README.md) - Templates copy-paste ready
- [examples/components/](./examples/components/) - React components templates
- [examples/services/](./examples/services/) - Service layer templates
- [examples/tests/](./examples/tests/) - Testing templates
- [examples/configs/](./examples/configs/) - Configuration templates

### 🔧 Automação Total
- [linting/README.md](./linting/README.md) - Linting automation setup
- [ci-cd/](./ci-cd/) - GitHub Actions, quality gates, deployment

## 🚀 Quick Start Workflow

### 1. Setup Inicial (OBRIGATÓRIO)
```bash
# Aplicar configurações de patterns
cp .kiro/patterns/linting/.eslintrc.custom.js .eslintrc.js
cp .kiro/patterns/linting/.prettierrc.custom.js .prettierrc.js
cp .kiro/patterns/linting/tsconfig.patterns.json tsconfig.json

# Instalar Git hooks para compliance automático
cp -r .kiro/patterns/linting/.husky/ .husky/
npx husky install

# Instalar dependências de qualidade
npm install -D eslint prettier @typescript-eslint/parser

# Validar setup inicial
npm run check-patterns
npm run type-check
echo "✅ Patterns CDD v2.0 configurados!"
```

### 2. Desenvolvimento Diário (Workflow Obrigatório)
```bash
# ANTES de implementar - consultar patterns relevantes
cat .kiro/patterns/README.md                    # Índice geral
cat .kiro/patterns/frontend/react.md            # Para React
cat .kiro/patterns/backend/nodejs.md            # Para Node.js
cat .kiro/patterns/database/postgresql.md       # Para DB queries

# DURANTE implementação - validação contínua
npm run lint-patterns --watch                   # Linting em tempo real
npm run type-check --watch                      # TypeScript validation
npm run test --watch                            # Testing contínuo

# ANTES de commit - validação automática (via Git hooks)
git add . && git commit -m "feat: implement X following patterns"
# Hooks executam: lint + type-check + tests + pattern compliance
```

### 3. Validação de Compliance
```bash
# Relatório de compliance detalhado
npm run patterns:report
# Output esperado: 95%+ compliance score

# Fix automático de patterns menores
npm run patterns:fix

# Audit de qualidade completo
npm run patterns:audit
npm run security:scan
npm run performance:audit
```

## 📊 Métricas de Qualidade Obrigatórias

### Targets Empresariais
```markdown
🎯 COMPLIANCE TARGETS (NON-NEGOTIABLE):
- Pattern Compliance: 95%+ (automatically enforced)
- TypeScript Strict: 100% (zero any usage)
- Test Coverage: 90%+ para código crítico
- Performance Budget: <250KB bundle gzipped
- Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1
- Security Score: A+ (zero known vulnerabilities)
- Accessibility: WCAG 2.1 AA (100% compliance)
- Task Tracking: 100% completed tasks marked

🔍 CONTINUOUS MONITORING:
- ESLint rules: 200+ rules automatically enforced
- Prettier formatting: Automatic code formatting
- TypeScript strict mode: noImplicitAny, strictNullChecks
- Git pre-commit hooks: Block non-compliant commits
- CI/CD quality gates: Prevent deployment of poor quality code
```

### Validation Automática
```markdown
✅ AUTOMATED VALIDATION LAYERS:
1. **Editor Level**: ESLint + Prettier real-time feedback
2. **Pre-commit**: Git hooks block bad code
3. **CI/CD**: Quality gates prevent deployment
4. **Monitoring**: Runtime error tracking via Sentry
5. **Performance**: Core Web Vitals monitoring
6. **Security**: Automated vulnerability scanning
```

## 🔄 Manutenção e Evolução

### Atualização de Patterns
```bash
# Gerar relatório de padrões desatualizados
npm run patterns:outdated

# Análise de violações frequentes
npm run patterns:violations --detailed

# Propor melhorias baseadas em dados
npm run patterns:suggest-improvements

# Versionar mudanças significativas
npm run patterns:version-bump
git commit -m "patterns: update to v2.1 with new security rules"
```

### Contribuição para Patterns
```markdown
📝 CONTRIBUTION WORKFLOW:
1. Identifique pattern recorrente no código
2. Documente em arquivo apropriado seguindo template
3. Adicione exemplos práticos funcionais
4. Configure ESLint rules para enforcement
5. Adicione testes para pattern validation
6. Update CHANGELOG.md com changes
7. Submeta PR com justificativa e impact analysis
```

---

## 🎯 INTEGRAÇÃO COM TASK TRACKING CDD v2.0

### Workflow com Task IDs
```bash
# Patterns são consultados durante desenvolvimento de tasks
npm run list user-authentication          # Ver tasks disponíveis
npm run start user-authentication-1.1     # Iniciar task específica

# Durante implementação - patterns são aplicados automaticamente
cp .kiro/patterns/examples/components/AuthForm.example.tsx src/components/AuthForm.tsx
# Edit following patterns automatically

# Validation durante desenvolvimento
npm run check-patterns                    # Compliance automático
npm run complete user-authentication-1.1  # Marcar task como concluída

# Task completion triggers validation
npm run validate-task-compliance user-authentication-1.1
```

### Automação Integrada
```markdown
🤖 AUTOMATED TASK WORKFLOWS:
- Task start: Auto-copy relevant pattern templates
- Development: Real-time pattern compliance checking
- Task completion: Automatic code quality validation
- Progress tracking: Pattern compliance metrics included
- Reporting: Task velocity + code quality correlation
```

---

**Versão**: 2.0.0  
**Última atualização**: 2025-01-14T10:45:00.000Z  
**Compliance Score**: 97% (Target: 95%+)  
**Status**: ✅ Production Ready with Full Automation
```

### conventions.md Rigoroso
```markdown
# Convenções de Código CDD v2.0

## 🎯 Nomenclatura Rigorosa (100% Enforcement)

### Arquivos e Diretórios (OBRIGATÓRIO)
```bash
✅ CORRETO:
components/user-profile/UserProfile.tsx      # PascalCase para componentes
pages/user-dashboard.tsx                     # kebab-case para pages
services/user-service.ts                     # kebab-case para services
utils/string-helpers.ts                      # kebab-case para utilities
types/api-responses.types.ts                 # kebab-case + .types
constants/api-endpoints.ts                   # kebab-case
hooks/use-local-storage.ts                   # kebab-case com use prefix
lib/database-connection.ts                   # kebab-case

❌ PROIBIDO (ESLint blocks):
components/userProfile.tsx                   # camelCase em arquivos
services/UserService.ts                      # PascalCase em services
utils/stringHelpers.ts                       # camelCase em utilities
types/apiResponses.ts                        # sem .types suffix
hooks/userHook.ts                            # sem use prefix
```

### Código TypeScript (Strict Enforcement)
```typescript
✅ OBRIGATÓRIO:
// Functions: camelCase
function calculateTotalPrice(basePrice: number): number {}
const validateUserInput = (input: string): boolean => {}

// Classes: PascalCase
class UserRepository {}
class ApiResponseHandler {}

// Constants: UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.healthtracker.com' as const;
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_PAGINATION_SIZE = 20;

// Interfaces: PascalCase (no I prefix required)
interface User {
  readonly id: string;
  name: string;
  email: string;
}

interface UserRepositoryContract {
  findById(id: string): Promise<User | null>;
}

// Types: PascalCase
type UserStatus = 'active' | 'inactive' | 'pending';
type ApiResponse<T> = {
  data: T;
  success: boolean;
  message?: string;
};

❌ PROIBIDO (Zero tolerance):
function CalculateTotalPrice() {}              # PascalCase para função
const validate_user_input = () => {}          # snake_case
class userRepository {}                        # camelCase para classe
const api_base_url = 'https://api.com';       # constante não UPPER_SNAKE
interface IUser {}                             # I prefix desnecessário
type userStatus = string;                      # camelCase + genérico demais
```

### React Components (Strict Patterns)
```typescript
✅ PADRÃO OBRIGATÓRIO:
// Component: PascalCase com props interface
interface UserProfileProps {
  userId: string;
  onUserUpdate?: (user: User) => void;
  showEmail?: boolean;
}

export function UserProfile({ 
  userId, 
  onUserUpdate, 
  showEmail = true 
}: UserProfileProps): JSX.Element {
  // Component implementation
}

// Custom hooks: use prefix + camelCase + explicit return type
export function useUserProfile(userId: string): {
  user: User | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
} {
  // Hook implementation
}

// File structure obrigatória:
UserProfile.tsx          # Component
UserProfile.test.tsx     # Tests
UserProfile.stories.tsx  # Storybook (opcional)
index.ts                 # Barrel export

❌ PROIBIDO:
export function userProfile() {}               # camelCase component
interface UserProfileProperties {}             # verbose naming
export function userProfileHook() {}           # sem use prefix
class UserProfile extends Component {}         # class components
```

## 📁 Estrutura de Arquivos Empresarial

### Organização por Feature (OBRIGATÓRIO)
```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Route groups
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable UI components
│   ├── ui/               # Basic UI components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts  # export { Button } from './Button'
│   │   └── index.ts      # export * from './Button'
│   └── index.ts          # export * from './ui'
├── features/             # Feature-specific code
│   ├── user-management/
│   │   ├── components/   # Feature components
│   │   ├── hooks/        # Feature hooks
│   │   ├── services/     # Business logic
│   │   ├── types/        # Feature types
│   │   ├── utils/        # Feature utilities
│   │   └── index.ts      # Public API
│   └── health-tracking/
├── lib/                  # Shared libraries
│   ├── utils.ts         # General utilities
│   ├── validations.ts   # Zod schemas
│   └── constants.ts     # Shared constants
├── hooks/               # Global custom hooks
├── types/               # Global TypeScript types
├── services/            # Global services (API, auth, etc.)
└── config/              # Configuration files
```

### Barrel Exports (OBRIGATÓRIO para Public APIs)
```typescript
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Modal } from './Modal';
export { DataTable } from './DataTable';

// features/user-management/index.ts - SOMENTE APIs públicas
export { UserProfile } from './components/UserProfile';
export { useUserProfile } from './hooks/useUserProfile';
export { UserService } from './services/UserService';

// Export types explicitly
export type { 
  User, 
  UserCreate, 
  UserUpdate 
} from './types/user.types';

// NÃO re-export internal utilities
// ❌ export * from './utils'; // internal only
```

## 📦 Imports e Dependencies (Automated Order)

### Ordem de Imports (ESLint Enforced)
```typescript
✅ ORDEM AUTOMÁTICA OBRIGATÓRIA:
// 1. React primeiro (sempre)
import React from 'react';
import { useState, useEffect, useCallback } from 'react';

// 2. External libraries (alfabético)
import { z } from 'zod';
import axios from 'axios';
import clsx from 'clsx';

// 3. Internal absolute imports (@/ path mapping)
import { Button, Input } from '@/components/ui';
import { UserService } from '@/services/user-service';
import { useAuth } from '@/hooks/use-auth';

// 4. Relative imports (próximo para distante)
import { validateUserInput } from '../utils/validation';
import { UserCard } from './UserCard';

// 5. Type imports (sempre por último)
import type { User, UserCreate } from '@/types/user.types';
import type { ComponentProps } from 'react';

❌ PROIBIDO (ESLint error):
import { validateUserInput } from '../utils';  # relative antes absolute
import type { User } from '@/types';          # types no meio
import React from 'react';                    # React não primeiro
```

### Path Mapping (TypeScript Config)
```typescript
// tsconfig.json paths - OBRIGATÓRIO
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/features/*": ["./src/features/*"],
      "@/services/*": ["./src/services/*"],
      "@/utils/*": ["./src/lib/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/types/*": ["./src/types/*"],
      "@/config/*": ["./src/config/*"]
    }
  }
}

✅ SEMPRE USAR:
import { UserService } from '@/services/user-service';
import { Button } from '@/components/ui';
import { User } from '@/types/user.types';

❌ NUNCA USAR:
import { UserService } from '../../../services/user-service';
import { Button } from '../../components/ui/Button';
import { User } from '../../../types/user';
```

## 💬 Comentários e Documentação (Quality Standards)

### JSDoc para APIs Públicas (OBRIGATÓRIO)
```typescript
✅ DOCUMENTAÇÃO COMPLETA:
/**
 * Calculates the total price including taxes, discounts, and shipping
 * 
 * @param basePrice - Base price before any calculations (must be positive)
 * @param taxRate - Tax rate as decimal (0.1 for 10%)
 * @param discountPercent - Discount percentage (10 for 10% discount)
 * @param shippingCost - Additional shipping cost (default: 0)
 * @returns Final price after all calculations
 * @throws {ValidationError} When basePrice is negative or taxRate invalid
 * 
 * @example
 * ```typescript
 * const finalPrice = calculateTotalPrice(100, 0.1, 5, 10);
 * // Returns: 105 + 10.5 (tax) + 10 (shipping) = 125.5
 * ```
 */
export function calculateTotalPrice(
  basePrice: number,
  taxRate: number,
  discountPercent: number = 0,
  shippingCost: number = 0
): number {
  if (basePrice < 0) {
    throw new ValidationError('Base price cannot be negative', 'basePrice');
  }
  
  if (taxRate < 0 || taxRate > 1) {
    throw new ValidationError('Tax rate must be between 0 and 1', 'taxRate');
  }
  
  const discountAmount = (basePrice * discountPercent) / 100;
  const discountedPrice = basePrice - discountAmount;
  const taxAmount = discountedPrice * taxRate;
  
  return discountedPrice + taxAmount + shippingCost;
}

❌ DOCUMENTAÇÃO INADEQUADA:
// Calculate price (óbvio)
function calc(p: number, t: number, d?: number): number { ... }

// Missing params documentation
/**
 * Calculates price
 */
function calculatePrice(basePrice, taxRate) { ... }
```

### Comentários Inline (Quando Necessário)
```typescript
✅ COMENTÁRIOS ÚTEIS:
// Using setTimeout instead of setInterval to prevent memory leaks
// if component unmounts before cleanup (React 18 Strict Mode issue)
const timeoutId = setTimeout(() => {
  fetchUserData();
}, DEBOUNCE_DELAY);

// Workaround for Safari Date.parse() bug with ISO strings
// See: https://bugs.webkit.org/show_bug.cgi?id=123456
// TODO: Remove when Safari 17+ has >90% market share
const normalizedDate = date.replace(/-/g, '/');

// Performance optimization: batch DOM updates
// Reduces layout thrashing from ~100ms to ~5ms
const fragment = document.createDocumentFragment();
items.forEach(item => fragment.appendChild(createItemElement(item)));
container.appendChild(fragment);

❌ COMENTÁRIOS INÚTEIS:
const total = price * 1.1; // Add tax (óbvio)
if (user) { ... }          // Check if user exists (óbvio)
i++;                       // Increment i (óbvio)
return true;               // Return true (óbvio)
```

---

## 🧪 Testing Conventions (90%+ Coverage Target)

### Nomenclatura de Testes (Jest/Vitest)
```typescript
✅ ESTRUTURA OBRIGATÓRIA:
// Describe: Component/function/service name
describe('UserProfile Component', () => {
  // Context blocks para scenarios
  describe('quando user data está carregando', () => {
    it('deve mostrar loading spinner', () => {});
    it('deve desabilitar form inputs', () => {});
  });
  
  describe('quando user data carrega com sucesso', () => {
    it('deve exibir user name no header', () => {});
    it('deve permitir edição de profile data', () => {});
    it('deve salvar mudanças quando form é submetido', () => {});
  });
  
  describe('quando ocorre erro no carregamento', () => {
    it('deve exibir error message apropriada', () => {});
    it('deve mostrar retry button', () => {});
    it('deve permitir retry da operação', () => {});
  });
});

// Para services/utilities
describe('UserService', () => {
  describe('createUser', () => {
    it('deve criar user com dados válidos', () => {});
    it('deve rejeitar quando email já existe', () => {});
    it('deve validar required fields', () => {});
  });
});

❌ NOMENCLATURA RUIM:
describe('user profile', () => {          # lowercase, vago
  it('test user name', () => {});         # vago, sem contexto
  it('loading', () => {});               # incompleto
  it('should work', () => {});           # inútil
});
```

### Test Structure Pattern
```typescript
✅ PADRÃO AAA (Arrange-Act-Assert):
describe('calculateTotalPrice', () => {
  it('deve calcular preço total com tax e discount corretamente', () => {
    // Arrange
    const basePrice = 100;
    const taxRate = 0.1; // 10%
    const discountPercent = 5; // 5%
    const expected = 100 - 5 + 9.5; // 104.5
    
    // Act
    const result = calculateTotalPrice(basePrice, taxRate, discountPercent);
    
    // Assert
    expect(result).toBe(expected);
    expect(result).toBeCloseTo(104.5, 2);
  });
  
  it('deve throw ValidationError para basePrice negativo', () => {
    // Arrange
    const invalidBasePrice = -10;
    
    // Act & Assert
    expect(() => {
      calculateTotalPrice(invalidBasePrice, 0.1);
    }).toThrow(ValidationError);
  });
});
```

---

## 🔧 Automação de Compliance (95%+ Target)

### ESLint Rules (200+ Rules Enforced)
```javascript
// .kiro/patterns/linting/.eslintrc.custom.js
module.exports = {
  rules: {
    // Naming conventions - ENFORCED
    '@typescript-eslint/naming-convention': [
      'error',
      {
        selector: 'variableLike',
        format: ['camelCase'],
        leadingUnderscore: 'forbid',
      },
      {
        selector: 'typeLike',
        format: ['PascalCase'],
      },
      {
        selector: 'enumMember',
        format: ['UPPER_CASE'],
      },
    ],
    
    // Import organization - ENFORCED
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external', 
          'internal',
          'parent',
          'sibling',
          'index',
          'type',
        ],
        'newlines-between': 'always',
        alphabetize: { order: 'asc' },
      },
    ],
    
    // TypeScript strict - ENFORCED
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'error',
    '@typescript-eslint/prefer-nullish-coalescing': 'error',
    '@typescript-eslint/prefer-optional-chain': 'error',
  },
};
```

### Git Hooks (Pre-commit Quality Gates)
```bash
#!/bin/sh
# .kiro/patterns/linting/.husky/pre-commit

echo "🔍 Running pre-commit quality checks..."

# 1. Lint and auto-fix
npm run lint-patterns --fix
if [ $? -ne 0 ]; then
  echo "❌ Linting failed"
  exit 1
fi

# 2. Type checking
npm run type-check
if [ $? -ne 0 ]; then
  echo "❌ Type checking failed" 
  exit 1
fi

# 3. Pattern compliance
npm run check-patterns
if [ $? -ne 0 ]; then
  echo "❌ Pattern compliance failed"
  exit 1
fi

# 4. Tests for changed files
npm run test:changed
if [ $? -ne 0 ]; then
  echo "❌ Tests failed"
  exit 1
fi

echo "✅ All quality checks passed!"
```

**Compliance Score**: 97% (Target: 95%+)  
**Enforcement**: Automatic via ESLint + Git hooks + CI/CD  
**Violations**: Zero tolerance in main branch 