# Prompt para Geração da Pasta Patterns CDD v2.0 (.kiro/patterns/)

## 🎯 Objetivo
Analise a estrutura de steering do projeto (.kiro/steering/) e gere uma pasta `patterns/` completa com padrões de código rigorosos, automação total, integração com task tracking e qualidade empresarial para CDD v2.0.

## 📋 Instruções Detalhadas para IA

### FASE 1: ANÁLISE PROFUNDA DO STEERING
Execute esta análise sistemática para extrair máximo contexto:

#### 1. **Análise de Produto e Negócio**
```bash
# Leia e entenda profundamente:
.kiro/steering/product.md
```
**Extraia:**
- **Domínio do negócio**: Qual área/setor? (fintech, e-commerce, healthcare, etc.)
- **Usuários alvo**: Quem usa o sistema? (desenvolvedores, end-users, empresas)
- **Objetivos críticos**: Quais métricas de sucesso são essenciais?
- **Constraints de negócio**: Regulamentações, compliance, performance requirements
- **Progressive strategy**: Como o produto evolui? Que patterns precisam ser escaláveis?

#### 2. **Análise de Stack Tecnológico**
```bash
# Analise tecnologias e decisões:
.kiro/steering/tech.md
```
**Identifique e catalogue:**
- **Frontend Stack**: React, Next.js, Vue, Angular, Svelte
- **Backend Stack**: Node.js, Express, Fastify, NestJS, Python, Go
- **Database**: PostgreSQL, MongoDB, Redis, Prisma, Drizzle
- **Testing**: Jest, Vitest, Cypress, Playwright, Testing Library
- **Build Tools**: Vite, Webpack, Turbo, esbuild, Rollup
- **DevOps**: Docker, Kubernetes, CI/CD, AWS, Vercel
- **Monitoring**: Sentry, DataDog, New Relic, logging strategies
- **Security**: Authentication, authorization, encryption requirements

#### 3. **Análise de Estrutura e Filosofia**
```bash
# Entenda organização e filosofia:
.kiro/steering/structure.md
```
**Extraia:**
- **Arquitetura**: Monolith, microservices, micro-frontends, modular monolith
- **Organização**: Feature-based, layer-based, domain-driven design
- **Convenções**: Nomenclatura, path mapping, import strategies
- **Performance**: Bundle splitting, lazy loading, optimization priorities
- **Filosofia**: LLM-first, automation-first, quality-first approach

### FASE 2: GERAÇÃO DA ESTRUTURA PATTERNS ROBUSTA

Crie a estrutura `.kiro/patterns/` completa e empresarial:

```
.kiro/patterns/
├── README.md                    # Índice navegável e overview completo
├── conventions.md               # Convenções rigorosas de nomenclatura
├── architecture.md              # Padrões arquiteturais e SOLID principles
├── typescript.md                # Padrões TypeScript strict mode
├── security.md                  # OWASP guidelines e security headers
├── performance.md               # Core Web Vitals e optimization patterns
├── testing.md                   # Testing patterns e coverage requirements
├── error-handling.md            # Error handling patterns e logging
├── accessibility.md             # WCAG 2.1 AA compliance patterns
├── frontend/                    # Padrões específicos do frontend
│   ├── README.md               # Índice de padrões frontend
│   ├── react.md                # React patterns (se aplicável)
│   ├── nextjs.md               # Next.js patterns (se aplicável)
│   ├── components.md           # Component design patterns
│   ├── state-management.md     # Redux, Zustand, Context patterns
│   ├── styling.md              # CSS-in-JS, CSS Modules, Tailwind
│   └── forms.md                # Form validation e handling
├── backend/                     # Padrões específicos do backend
│   ├── README.md               # Índice de padrões backend
│   ├── nodejs.md               # Node.js patterns (se aplicável)
│   ├── api-design.md           # REST/GraphQL API patterns
│   ├── middleware.md           # Middleware patterns
│   ├── authentication.md       # Auth patterns e JWT handling
│   ├── database.md             # Database query patterns
│   └── caching.md              # Cache strategies e invalidation
├── database/                    # Padrões específicos de banco
│   ├── README.md               # Índice de padrões database
│   ├── postgresql.md           # PostgreSQL patterns (se aplicável)
│   ├── migrations.md           # Migration patterns e versioning
│   ├── indexing.md             # Index optimization patterns
│   ├── transactions.md         # Transaction patterns
│   └── backup.md               # Backup e recovery patterns
├── examples/                    # Templates práticos copy-paste ready
│   ├── README.md               # Índice de templates
│   ├── components/             # Component templates
│   ├── services/               # Service layer templates
│   ├── controllers/            # Controller templates
│   ├── models/                 # Model/Schema templates
│   ├── tests/                  # Test templates
│   └── configs/                # Configuration templates
├── linting/                     # Configurações de linting automatizadas
│   ├── README.md               # Setup e uso das configs
│   ├── .eslintrc.custom.js     # ESLint config customizada
│   ├── .prettierrc.custom.js   # Prettier config customizada
│   ├── tsconfig.patterns.json  # TypeScript config rigorosa
│   ├── .husky/                 # Git hooks configuration
│   └── lint-staged.config.js   # Staged files linting
├── ci-cd/                       # Patterns para CI/CD
│   ├── github-actions.yml      # GitHub Actions workflows
│   ├── pre-commit.yml          # Pre-commit hooks
│   └── quality-gates.md        # Quality gate definitions
└── CHANGELOG.md                 # Versionamento dos patterns
```

### FASE 3: CONTEÚDO DETALHADO DOS ARQUIVOS

#### README.md Principal
```markdown
# Code Patterns CDD v2.0

## 🎯 Visão Geral
Este diretório contém todos os padrões de código obrigatórios para o projeto [NOME_PROJETO].
Baseado na análise de steering, aplicamos rigorosamente:

### Stack Identificado
- **Frontend**: [EXTRAIR DE tech.md]
- **Backend**: [EXTRAIR DE tech.md]
- **Database**: [EXTRAIR DE tech.md]
- **Testing**: [EXTRAIR DE tech.md]

### Princípios Fundamentais
1. **Consistency Over Flexibility**: Patterns rigorosos garantem código uniforme
2. **Automation Over Manual**: Linting automático força compliance
3. **Security By Default**: OWASP patterns aplicados por padrão
4. **Performance First**: Core Web Vitals como priority
5. **Accessibility Always**: WCAG 2.1 AA compliance obrigatória

## 📚 Índice de Patterns

### 🏗️ Arquitetura e Fundamentos
- [conventions.md](./conventions.md) - Nomenclatura e convenções rigorosas
- [architecture.md](./architecture.md) - SOLID principles e design patterns
- [typescript.md](./typescript.md) - TypeScript strict mode patterns

### 🔒 Qualidade e Segurança
- [security.md](./security.md) - OWASP guidelines e security headers
- [performance.md](./performance.md) - Optimization e Core Web Vitals
- [testing.md](./testing.md) - Testing strategies e coverage
- [error-handling.md](./error-handling.md) - Error handling e logging
- [accessibility.md](./accessibility.md) - WCAG compliance patterns

### 🎨 Frontend Patterns
- [frontend/README.md](./frontend/README.md) - Índice frontend
- [frontend/react.md](./frontend/react.md) - React best practices
- [frontend/components.md](./frontend/components.md) - Component patterns
- [frontend/state-management.md](./frontend/state-management.md) - State patterns

### ⚙️ Backend Patterns
- [backend/README.md](./backend/README.md) - Índice backend
- [backend/nodejs.md](./backend/nodejs.md) - Node.js patterns
- [backend/api-design.md](./backend/api-design.md) - API design patterns
- [backend/authentication.md](./backend/authentication.md) - Auth patterns

### 🗄️ Database Patterns
- [database/README.md](./database/README.md) - Índice database
- [database/postgresql.md](./database/postgresql.md) - PostgreSQL patterns
- [database/migrations.md](./database/migrations.md) - Migration patterns

### 📝 Templates e Exemplos
- [examples/README.md](./examples/README.md) - Templates práticos
- [examples/components/](./examples/components/) - Component templates
- [examples/services/](./examples/services/) - Service templates

### 🔧 Automação
- [linting/README.md](./linting/README.md) - Linting automation
- [ci-cd/](./ci-cd/) - CI/CD patterns

## 🚀 Quick Start

### 1. Setup Inicial
```bash
# Aplicar configurações de linting
cp .kiro/patterns/linting/.eslintrc.custom.js .eslintrc.js
cp .kiro/patterns/linting/.prettierrc.custom.js .prettierrc.js
cp .kiro/patterns/linting/tsconfig.patterns.json tsconfig.json

# Instalar Git hooks
cp -r .kiro/patterns/linting/.husky/ .husky/
npx husky install

# Validar setup
npm run check-patterns
```

### 2. Desenvolvimento Diário
```bash
# Antes de implementar - consultar patterns relevantes
cat .kiro/patterns/[technology].md

# Durante implementação - validação contínua
npm run lint-patterns --watch

# Antes de commit - validação automática (via Git hooks)
git add . && git commit -m "feature: implement X following patterns"
```

### 3. Validação de Compliance
```bash
# Relatório de compliance
npm run patterns:report

# Fix automático de patterns
npm run patterns:fix

# Audit de qualidade
npm run patterns:audit
```

## 📊 Métricas de Qualidade

### Targets Obrigatórios
- **Pattern Compliance**: >95%
- **TypeScript Strict**: 100% (zero any)
- **Test Coverage**: >90% para código crítico
- **Performance Budget**: <250KB bundle gzipped
- **Accessibility**: WCAG 2.1 AA compliance
- **Security**: Zero vulnerabilidades conhecidas

### Validação Automática
Todos os patterns são automaticamente validados via:
- ESLint rules customizadas
- Prettier formatting
- TypeScript strict mode
- Git pre-commit hooks
- CI/CD quality gates

## 🔄 Manutenção e Evolução

### Atualização de Patterns
```bash
# Gerar relatório de padrões desatualizados
npm run patterns:outdated

# Propor melhorias baseadas em dados
npm run patterns:suggest

# Versionar mudanças
npm run patterns:version
```

### Contribuição
1. Identifique pattern recorrente no código
2. Documente em arquivo apropriado
3. Adicione exemplos práticos
4. Configure linting rules
5. Submeta PR com justificativa

---
**Última atualização**: [DATA_ATUAL]
**Versão**: 2.0.0
**Status**: ✅ Production Ready
```

#### conventions.md
```markdown
# Convenções de Código CDD v2.0

## 🎯 Nomenclatura Rigorosa

### Arquivos e Diretórios
```bash
✅ CORRETO:
components/user-profile/UserProfile.tsx      # PascalCase para componentes
services/user-service.ts                     # kebab-case para services
utils/string-helpers.ts                      # kebab-case para utilities
types/api-responses.types.ts                 # kebab-case + .types
constants/api-endpoints.ts                   # kebab-case
hooks/use-local-storage.ts                   # kebab-case

❌ ERRADO:
components/userProfile.tsx                   # camelCase em arquivos
services/UserService.ts                      # PascalCase em services
utils/stringHelpers.ts                       # camelCase em utilities
types/apiResponses.ts                        # sem .types suffix
```

### Funções e Variáveis
```typescript
✅ CORRETO:
// Funções: camelCase
function calculateTotalPrice() {}
const validateUserInput = () => {}

// Classes: PascalCase
class UserRepository {}
class ApiResponseHandler {}

// Constantes: UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.example.com';
const MAX_RETRY_ATTEMPTS = 3;

// Interfaces: PascalCase com I prefix opcional
interface User {}
interface IUserRepository {}

// Types: PascalCase com T prefix opcional
type UserStatus = 'active' | 'inactive';
type TApiResponse<T> = { data: T; success: boolean };

❌ ERRADO:
function CalculateTotalPrice() {}              # PascalCase para função
const validate_user_input = () => {}          # snake_case
class userRepository {}                        # camelCase para classe
const api_base_url = 'https://api.com';       # não é constante
```

### Componentes React
```typescript
✅ CORRETO:
// Component: PascalCase
export function UserProfile({ userId }: UserProfileProps) {}

// Props interface: ComponentProps suffix
interface UserProfileProps {
  userId: string;
  onUserUpdate?: (user: User) => void;
}

// Custom hooks: use prefix + camelCase
export function useUserProfile(userId: string) {}

// Component files: ComponentName.tsx
UserProfile.tsx
UserProfile.test.tsx
UserProfile.stories.tsx

❌ ERRADO:
export function userProfile() {}               # camelCase component
interface UserProfileProperties {}             # verbose naming
export function userProfileHook() {}           # no use prefix
```

## 📁 Estrutura de Arquivos Obrigatória

### Organização por Feature
```
src/
├── components/              # Componentes reutilizáveis
│   ├── ui/                 # Components de UI básicos
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts    # Barrel export obrigatório
│   │   └── index.ts        # Barrel export do ui/
│   └── index.ts            # Barrel export geral
├── features/               # Features específicas
│   ├── user-management/
│   │   ├── components/     # Components específicos da feature
│   │   ├── hooks/          # Hooks específicos
│   │   ├── services/       # Business logic
│   │   ├── types/          # Types específicos
│   │   └── index.ts        # API pública da feature
├── services/               # Services compartilhados
├── utils/                  # Utilities puras
├── hooks/                  # Custom hooks globais
├── types/                  # Types globais
├── constants/              # Constantes globais
└── config/                 # Configurações
```

### Barrel Exports (Obrigatório)
```typescript
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Modal } from './Modal';

// features/user-management/index.ts
export * from './components';
export * from './hooks';
export * from './services';
export type { User, UserCreate, UserUpdate } from './types';
```

## 📦 Imports e Dependencies

### Ordem de Imports (Obrigatório)
```typescript
✅ CORRETO:
// 1. External libraries
import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';

// 2. Internal absolute imports (path mapping)
import { Button, Input } from '@/components/ui';
import { useAuth } from '@/hooks';
import { UserService } from '@/services';

// 3. Relative imports
import { validateUserInput } from '../utils';
import { UserProfile } from './UserProfile';

// 4. Type imports (last)
import type { User, UserCreate } from '@/types';
import type { ComponentProps } from 'react';

❌ ERRADO:
import { validateUserInput } from '../utils';  # relative primeiro
import React from 'react';                    # external depois
import type { User } from '@/types';          # types no meio
import { Button } from '@/components/ui';     # absolute depois
```

### Path Mapping (Obrigatório)
```typescript
// tsconfig.json paths configuration
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/features/*": ["./src/features/*"],
      "@/services/*": ["./src/services/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/types/*": ["./src/types/*"],
      "@/config/*": ["./src/config/*"]
    }
  }
}

✅ USAR:
import { UserService } from '@/services/user-service';
import { Button } from '@/components/ui';

❌ NÃO USAR:
import { UserService } from '../../../services/user-service';
import { Button } from '../../components/ui/Button';
```

## 💬 Comentários e Documentação

### JSDoc para APIs Públicas (Obrigatório)
```typescript
✅ CORRETO:
/**
 * Calculates the total price including taxes and discounts
 * @param basePrice - Base price before calculations
 * @param taxRate - Tax rate as decimal (0.1 for 10%)
 * @param discountPercent - Discount percentage (10 for 10%)
 * @returns Final price after taxes and discounts
 * @throws {Error} When basePrice is negative
 */
export function calculateTotalPrice(
  basePrice: number,
  taxRate: number,
  discountPercent: number = 0
): number {
  if (basePrice < 0) {
    throw new Error('Base price cannot be negative');
  }
  
  const discountAmount = (basePrice * discountPercent) / 100;
  const discountedPrice = basePrice - discountAmount;
  return discountedPrice * (1 + taxRate);
}

❌ EVITAR:
// Calculate price (comentário óbvio)
function calc(p, t, d) { ... }  // nomes não descritivos
```

### Comentários Inline (Quando Necessário)
```typescript
✅ CORRETO:
// Using setTimeout instead of setInterval to prevent memory leaks
// in case the component unmounts before cleanup
const timeoutId = setTimeout(() => {
  fetchUserData();
}, DEBOUNCE_DELAY);

// Workaround for Safari bug with Date.parse()
// https://bugs.webkit.org/show_bug.cgi?id=123456
const normalizedDate = date.replace(/-/g, '/');

❌ EVITAR:
const total = price * 1.1; // Add tax (óbvio)
if (user) { ... }          // Check if user exists (óbvio)
```

## 🧪 Testing Conventions

### Nomenclatura de Testes
```typescript
✅ CORRETO:
// Describe: component/function name
describe('UserProfile', () => {
  // Test: should + behavior + condition
  it('should display user name when user data is provided', () => {});
  it('should show loading state when user data is loading', () => {});
  it('should handle error when user data fails to load', () => {});
});

// Para hooks
describe('useUserProfile', () => {
  it('should return user data when userId is valid', () => {});
  it('should return loading state while fetching', () => {});
});

❌ EVITAR:
describe('user profile component', () => {  // lowercase
  it('test user name', () => {});           // vago
  it('loading', () => {});                  // incompleto
});
```

## 🎨 CSS e Styling

### CSS Modules (se aplicável)
```typescript
// UserProfile.module.css
.container {
  padding: 1rem;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
}

// UserProfile.tsx
import styles from './UserProfile.module.css';

export function UserProfile() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>User Profile</h1>
    </div>
  );
}
```

### Styled Components (se aplicável)
```typescript
import styled from 'styled-components';

// PascalCase para styled components
const Container = styled.div`
  padding: 1rem;
`;

const Title = styled.h1`
  font-size: 1.5rem;
  font-weight: bold;
`;
```

---

## 🔧 Automação de Compliance

### ESLint Rules
- `@typescript-eslint/naming-convention`: Força nomenclatura
- `import/order`: Força ordem de imports
- `prefer-const`: Força uso de const
- `no-var`: Proíbe var

### Prettier Configuration
- `semi: true`: Semicolons obrigatórios
- `singleQuote: true`: Single quotes
- `trailingComma: 'es5'`: Trailing commas

### Git Hooks
- Pre-commit: Linting e formatting
- Pre-push: Type checking e tests

**Compliance Target**: 100% - Zero tolerância para violações
```

#### typescript.md
```markdown
# TypeScript Patterns CDD v2.0

## 🎯 Strict Mode Configuration

### tsconfig.json Obrigatório
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    
    // STRICT MODE - OBRIGATÓRIO
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    
    // ADDITIONAL STRICTNESS
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    
    // PATH MAPPING
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/features/*": ["./src/features/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "build"]
}
```

## 🏗️ Type Definitions

### Interface Design
```typescript
✅ CORRETO:
// Use interface para object types
interface User {
  readonly id: string;        // readonly para IDs
  name: string;
  email: string;
  age?: number;               // optional com ?
  createdAt: Date;
  updatedAt: Date;
}

// Extend interfaces quando apropriado
interface UserCreate extends Omit<User, 'id' | 'createdAt' | 'updatedAt'> {
  password: string;
}

// Generic interfaces para reusabilidade
interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
}

❌ EVITAR:
// any type é PROIBIDO (exceto casos extremos justificados)
interface BadUser {
  data: any;                  // ❌ use specific types
  metadata: object;           // ❌ use Record<string, unknown>
}
```

### Union Types e Literals
```typescript
✅ CORRETO:
// Union types para valores específicos
type UserStatus = 'active' | 'inactive' | 'pending' | 'suspended';
type ThemeMode = 'light' | 'dark' | 'auto';

// Literal types com const assertions
const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  NOT_FOUND: 404,
  INTERNAL_ERROR: 500,
} as const;

type HttpStatusCode = typeof HTTP_STATUS[keyof typeof HTTP_STATUS];

// Discriminated unions para type safety
type LoadingState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: unknown }
  | { status: 'error'; error: string };

❌ EVITAR:
type BadStatus = string;      // muito genérico
type BadState = {             // falta discriminator
  loading?: boolean;
  data?: unknown;
  error?: string;
};
```

### Utility Types
```typescript
✅ USAR UTILITY TYPES:
// Partial para updates
function updateUser(id: string, updates: Partial<User>): Promise<User> {}

// Pick para selecionar props específicas
type UserSummary = Pick<User, 'id' | 'name' | 'email'>;

// Omit para excluir props
type UserCreate = Omit<User, 'id' | 'createdAt' | 'updatedAt'>;

// Record para object types
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;

// ReturnType para inferir tipos de retorno
const createUser = (data: UserCreate) => ({ ...data, id: generateId() });
type CreatedUser = ReturnType<typeof createUser>;
```

## 🎯 Function Signatures

### Function Declarations
```typescript
✅ CORRETO:
// Explicit return types para APIs públicas
export function calculateTotalPrice(
  basePrice: number,
  taxRate: number,
  discountPercent: number = 0
): number {
  return basePrice * (1 + taxRate) * (1 - discountPercent / 100);
}

// Async functions com Promise typing
export async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.statusText}`);
  }
  return response.json() as User;
}

// Generic functions
export function createApiClient<T>(
  baseUrl: string,
  defaultHeaders?: Record<string, string>
): ApiClient<T> {
  // implementation
}

❌ EVITAR:
// Implicit return types para APIs públicas
export function calculate(price, tax) {  // ❌ no types
  return price * tax;
}

// any no return type
export async function fetchData(): Promise<any> {  // ❌ use specific type
  // implementation
}
```

### React Component Types
```typescript
✅ CORRETO:
// Functional components com proper typing
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
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  
  // Component logic
  
  return (
    <div>
      {/* JSX */}
    </div>
  );
}

// Custom hooks com proper typing
export function useUserProfile(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // Hook logic
  
  return { user, loading, error, refetch };
}

// Hook return type should be inferred or explicitly typed for complex cases
export function useApiCall<T>(): {
  data: T | null;
  loading: boolean;
  error: string | null;
  call: (url: string) => Promise<void>;
} {
  // implementation
}
```

## 🔒 Type Safety Patterns

### Null/Undefined Handling
```typescript
✅ CORRETO:
// Use optional chaining e nullish coalescing
function getUserDisplayName(user: User | null): string {
  return user?.name ?? 'Anonymous';
}

// Type guards para runtime safety
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof (obj as User).id === 'string' &&
    typeof (obj as User).name === 'string'
  );
}

// Assertion functions
function assertIsUser(obj: unknown): asserts obj is User {
  if (!isUser(obj)) {
    throw new Error('Object is not a valid User');
  }
}

❌ EVITAR:
// Unsafe type assertions
const user = data as User;              // ❌ sem validação
const user = data!;                     // ❌ non-null assertion perigoso

// Manual null checks quando temos optional chaining
if (user && user.profile && user.profile.avatar) {  // ❌ use user?.profile?.avatar
  // ...
}
```

### Error Handling Types
```typescript
✅ CORRETO:
// Result pattern para error handling
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

export async function safeApiCall<T>(
  url: string
): Promise<Result<T, string>> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return { success: false, error: response.statusText };
    }
    const data = await response.json() as T;
    return { success: true, data };
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}

// Custom error types
class ValidationError extends Error {
  constructor(
    message: string,
    public field: string,
    public code: string
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

## 📦 Module Patterns

### Barrel Exports
```typescript
// types/index.ts
export type { User, UserCreate, UserUpdate } from './user.types';
export type { ApiResponse, ApiError } from './api.types';
export type { LoadingState, AsyncState } from './common.types';

// services/index.ts
export { UserService } from './user-service';
export { AuthService } from './auth-service';
export { ApiClient } from './api-client';

// Re-export with rename if needed
export { 
  PostgresUserRepository as UserRepository 
} from './user-repository';
```

### Declaration Merging (quando necessário)
```typescript
// Para estender bibliotecas externas
declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      primary: string;
      secondary: string;
      error: string;
    };
    breakpoints: {
      mobile: string;
      tablet: string;
      desktop: string;
    };
  }
}
```

## 🧪 Testing Types

### Test Utilities
```typescript
// test-utils.types.ts
export type MockedFunction<T extends (...args: any[]) => any> = 
  jest.MockedFunction<T>;

export type PartialUser = Partial<User>;

// Factory functions para testes
export function createMockUser(overrides: Partial<User> = {}): User {
  return {
    id: 'test-id',
    name: 'Test User',
    email: 'test@example.com',
    createdAt: new Date(),
    updatedAt: new Date(),
    ...overrides,
  };
}

// Type-safe mock creators
export function createMockApiResponse<T>(
  data: T,
  overrides: Partial<ApiResponse<T>> = {}
): ApiResponse<T> {
  return {
    data,
    success: true,
    message: 'Success',
    ...overrides,
  };
}
```

## 🔧 Advanced Patterns

### Template Literal Types
```typescript
// Para type-safe string manipulation
type EmailDomain = 'gmail.com' | 'company.com' | 'test.com';
type Email<T extends EmailDomain> = `${string}@${T}`;

type UserEmail = Email<'company.com'>;  // only accepts @company.com emails

// Event naming pattern
type EventType = 'user' | 'order' | 'payment';
type EventAction = 'created' | 'updated' | 'deleted';
type EventName<T extends EventType, A extends EventAction> = `${T}.${A}`;

type UserEvents = EventName<'user', 'created' | 'updated'>;  // 'user.created' | 'user.updated'
```

### Conditional Types
```typescript
// API response based on method
type ApiMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

type ApiResponse<T, M extends ApiMethod> = M extends 'DELETE'
  ? { success: boolean; message: string }
  : { success: boolean; data: T };

// Async or sync based on flag
type MaybeAsync<T, Async extends boolean> = Async extends true
  ? Promise<T>
  : T;

function processData<A extends boolean>(
  data: string,
  async: A
): MaybeAsync<string, A> {
  // implementation with proper return type
}
```

---

## 📊 Compliance Targets

### Métricas Obrigatórias
- **any usage**: 0% (zero tolerância)
- **Type coverage**: 100%
- **Strict mode compliance**: 100%
- **Explicit return types**: 100% para APIs públicas
- **Type imports**: Separados dos value imports

### Validação Automática
```bash
# TypeScript compiler check
npm run type-check

# Type coverage
npm run type-coverage

# ESLint TypeScript rules
npm run lint:typescript
```

**Target**: Zero TypeScript errors, zero any usage, 100% type safety
```

### FASE 4: CONFIGURAÇÕES DE AUTOMAÇÃO

#### linting/.eslintrc.custom.js
```javascript
module.exports = {
  root: true,
  extends: [
    '@eslint/js/recommended',
    '@typescript-eslint/recommended',
    '@typescript-eslint/recommended-requiring-type-checking',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: { jsx: true },
    tsconfigRootDir: __dirname,
    project: ['./tsconfig.json'],
  },
  plugins: [
    '@typescript-eslint',
    'react',
    'react-hooks',
    'jsx-a11y',
    'import',
  ],
  settings: {
    react: { version: 'detect' },
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json',
      },
    },
  },
  rules: {
    // TypeScript Rules - STRICT
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': [
      'error',
      { allowExpressions: true },
    ],
    '@typescript-eslint/prefer-nullish-coalescing': 'error',
    '@typescript-eslint/prefer-optional-chain': 'error',
    '@typescript-eslint/strict-boolean-expressions': 'error',
    
    // Naming Conventions - ENFORCED
    '@typescript-eslint/naming-convention': [
      'error',
      {
        selector: 'variableLike',
        format: ['camelCase'],
        leadingUnderscore: 'allow',
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
    
    // Import Organization - ENFORCED
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
    
    // React Rules - STRICT
    'react/jsx-uses-react': 'off',
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
    'react/jsx-no-bind': 'error',
    'react/no-array-index-key': 'error',
    
    // Accessibility - ENFORCED
    'jsx-a11y/alt-text': 'error',
    'jsx-a11y/aria-props': 'error',
    'jsx-a11y/aria-proptypes': 'error',
    'jsx-a11y/aria-unsupported-elements': 'error',
    
    // General Quality
    'prefer-const': 'error',
    'no-var': 'error',
    'no-console': 'warn',
    'eqeqeq': 'error',
  },
  overrides: [
    {
      files: ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}'],
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
        'no-console': 'off',
      },
    },
  ],
};
```

### FASE 5: VALIDAÇÃO E MÉTRICAS

#### Script de Validação de Patterns
```bash
#!/bin/bash
# scripts/validate-generated-patterns.sh

echo "🔍 Validating generated patterns..."

# Check required files
required_files=(
  ".kiro/patterns/README.md"
  ".kiro/patterns/conventions.md"
  ".kiro/patterns/typescript.md"
  ".kiro/patterns/linting/.eslintrc.custom.js"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing required file: $file"
    exit 1
  fi
done

# Validate content quality
if ! grep -q "CDD v2.0" .kiro/patterns/README.md; then
  echo "❌ README.md must reference CDD v2.0"
  exit 1
fi

if ! grep -q "OBRIGATÓRIO" .kiro/patterns/conventions.md; then
  echo "❌ conventions.md must have mandatory requirements"
  exit 1
fi

# Check automation setup
if [ ! -f ".kiro/patterns/linting/.eslintrc.custom.js" ]; then
  echo "❌ Missing ESLint configuration"
  exit 1
fi

echo "✅ All patterns validation passed!"
```

## 🎯 **Resultado**: Geração automática de patterns CDD v2.0 robustos, completos e prontos para produção!

### ✅ **Entregáveis do Prompt:**
1. **Análise completa** de steering documents para contexto
2. **Estrutura rigorosa** de patterns baseada em tecnologias identificadas
3. **Padrões específicos** para cada tecnologia na stack
4. **Automação total** com linting, formatting e validation
5. **Templates práticos** copy-paste ready
6. **Configurações de CI/CD** para quality gates
7. **Métricas de compliance** automatizadas
8. **Documentation completa** com exemplos práticos

### 🎯 **Características dos Patterns Gerados:**
- **Technology-Specific**: Patterns adaptados à stack real do projeto
- **Automation-First**: Linting rules que forçam compliance
- **Enterprise-Grade**: Qualidade empresarial com security e performance
- **Developer-Friendly**: Templates e exemplos práticos
- **Maintainable**: Versionamento e evolution guidelines
- **Measurable**: Métricas e dashboards de compliance

---

**Prompt Version**: 2.0.0  
**Target Compliance**: 95%+ automation, 100% type safety, zero any usage  
**Expected Output**: Production-ready patterns directory com automação completa 