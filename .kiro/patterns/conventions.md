# Convenções de Código

## Nomenclatura (Obrigatório)

### Arquivos

- **Components**: `PascalCase.tsx` (ex: `UserProfile.tsx`)
- **Pages**: `kebab-case.tsx` (ex: `user-settings.tsx`)
- **Utils**: `camelCase.ts` (ex: `formatDate.ts`)
- **Types**: `camelCase.types.ts` (ex: `user.types.ts`)
- **Constants**: `UPPER_SNAKE_CASE.ts` (ex: `API_ENDPOINTS.ts`)

### Variáveis

- **JavaScript/TypeScript**: `camelCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **CSS Classes**: `kebab-case`
- **Environment**: `UPPER_SNAKE_CASE`

## Estrutura de Arquivos

### Componentes

```
components/ComponentName/
├── index.ts                 # Barrel export
├── ComponentName.tsx        # Main component
├── ComponentName.test.tsx   # Tests
├── ComponentName.stories.tsx # Storybook
└── ComponentName.styles.ts  # Styled components
```

### Services

```
services/ServiceName/
├── index.ts                 # Barrel export
├── ServiceName.ts           # Main service
├── ServiceName.test.ts      # Tests
└── ServiceName.types.ts     # Type definitions
```

## Import/Export Rules

### Import Order (Obrigatório)

```typescript
// 1. External libraries (alfabética)
import React from 'react';
import axios from 'axios';

// 2. Internal modules (alfabética)
import { Button } from '@/components/ui/Button';
import { UserService } from '@/services/UserService';

// 3. Relative imports
import './Component.css';

// 4. Type-only imports
import type { User } from '@/types/user.types';
```

### Export Rules

- **Default exports**: Apenas para componentes principais
- **Named exports**: Para utilities, types, constants
- **Barrel exports**: Obrigatório via index.ts

## Anti-Patterns (Proibido)

### ❌ Nunca Fazer

- Nomes genéricos: `Component1`, `utils`, `helper`
- Imports relativos longos: `../../../components`
- Arquivos > 300 linhas sem modularização
- Misturar types com implementação
- CSS inline exceto valores dinâmicos

### ✅ Sempre Fazer

- Nomes descritivos e específicos
- Absolute paths com path mapping
- Arquivos modulares < 200 linhas
- Separar types em arquivos .types.ts
- CSS componentizado ou modules
