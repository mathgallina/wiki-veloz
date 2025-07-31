# Padrões de Componentes - CDD v2.0

## Estrutura de Arquivos

### Estrutura Obrigatória

```
components/ComponentName/
├── index.ts                 # Barrel export
├── ComponentName.tsx        # Main component
├── ComponentName.test.tsx   # Tests
├── ComponentName.stories.tsx # Storybook
├── ComponentName.types.ts   # Type definitions
└── ComponentName.styles.ts  # Styled components
```

## Tipos de Componentes

### 1. Componentes de UI (Básicos)

```typescript
// components/ui/Button/Button.tsx
import React from 'react';
import type { ButtonProps } from './Button.types';

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  ...props
}) => {
  const baseClasses = 'button';
  const variantClasses = `button--${variant}`;
  const sizeClasses = `button--${size}`;
  const disabledClasses = disabled ? 'button--disabled' : '';

  return (
    <button
      className={`${baseClasses} ${variantClasses} ${sizeClasses} ${disabledClasses}`}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};
```

### 2. Componentes de Layout

```typescript
// components/layout/Container/Container.tsx
import React from 'react';
import type { ContainerProps } from './Container.types';

export const Container: React.FC<ContainerProps> = ({
  children,
  maxWidth = 'lg',
  padding = 'medium',
  ...props
}) => {
  return (
    <div
      className={`container container--${maxWidth} container--${padding}`}
      {...props}
    >
      {children}
    </div>
  );
};
```

### 3. Componentes de Formulário

```typescript
// components/forms/Input/Input.tsx
import React, { forwardRef } from 'react';
import type { InputProps } from './Input.types';

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, ...props }, ref) => {
    return (
      <div className='input-wrapper'>
        {label && <label className='input-label'>{label}</label>}
        <input
          ref={ref}
          className={`input ${error ? 'input--error' : ''}`}
          {...props}
        />
        {error && <span className='input-error'>{error}</span>}
        {helperText && !error && <span className='input-helper'>{helperText}</span>}
      </div>
    );
  }
);
```

## Padrões de Props

### Props Interface

```typescript
// components/ComponentName/ComponentName.types.ts
export interface ComponentNameProps {
  // Required props
  title: string;

  // Optional props with defaults
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;

  // Event handlers
  onClick?: () => void;
  onMouseEnter?: () => void;

  // Children
  children?: React.ReactNode;

  // HTML attributes
  className?: string;
  id?: string;

  // Spread operator for additional props
  [key: string]: any;
}
```

### Props com Validação

```typescript
// components/ComponentName/ComponentName.tsx
import React from 'react';
import type { ComponentNameProps } from './ComponentName.types';

export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  children,
  className = '',
  ...props
}) => {
  // Validação de props
  if (!title) {
    console.warn('ComponentName: title prop is required');
  }

  // Classes dinâmicas
  const classes = [
    'component-name',
    `component-name--${variant}`,
    `component-name--${size}`,
    disabled && 'component-name--disabled',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={classes} {...props}>
      <h3>{title}</h3>
      {children}
      {onClick && (
        <button onClick={onClick} disabled={disabled}>
          Action
        </button>
      )}
    </div>
  );
};
```

## Padrões de Estilização

### CSS Modules

```typescript
// components/ComponentName/ComponentName.module.css
.componentName {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  background: var(--color-background);
}

.componentName--primary {
  background: var(--color-primary);
  color: var(--color-white);
}

.componentName--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Styled Components

```typescript
// components/ComponentName/ComponentName.styles.ts
import styled from 'styled-components';

export const ComponentWrapper = styled.div<{
  variant: 'primary' | 'secondary';
  disabled: boolean;
}>`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  background: ${({ variant }) =>
    variant === 'primary' ? 'var(--color-primary)' : 'var(--color-secondary)'};
  opacity: ${({ disabled }) => (disabled ? 0.5 : 1)};
  cursor: ${({ disabled }) => (disabled ? 'not-allowed' : 'pointer')};
`;
```

## Padrões de Teste

### Teste de Renderização

```typescript
// components/ComponentName/ComponentName.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('should render with title', () => {
    render(<ComponentName title='Test Title' />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('should apply variant class', () => {
    render(<ComponentName title='Test' variant='secondary' />);
    const element = screen.getByText('Test').closest('div');
    expect(element).toHaveClass('component-name--secondary');
  });

  it('should be disabled when disabled prop is true', () => {
    render(<ComponentName title='Test' disabled={true} />);
    const element = screen.getByText('Test').closest('div');
    expect(element).toHaveClass('component-name--disabled');
  });
});
```

### Teste de Interações

```typescript
// components/ComponentName/ComponentName.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName Interactions', () => {
  it('should call onClick when button is clicked', () => {
    const mockOnClick = jest.fn();
    render(<ComponentName title='Test' onClick={mockOnClick} />);

    fireEvent.click(screen.getByText('Action'));
    expect(mockOnClick).toHaveBeenCalledTimes(1);
  });

  it('should not call onClick when disabled', () => {
    const mockOnClick = jest.fn();
    render(<ComponentName title='Test' onClick={mockOnClick} disabled={true} />);

    fireEvent.click(screen.getByText('Action'));
    expect(mockOnClick).not.toHaveBeenCalled();
  });
});
```

## Padrões de Performance

### Memoização

```typescript
// components/ComponentName/ComponentName.tsx
import React, { memo } from 'react';
import type { ComponentNameProps } from './ComponentName.types';

export const ComponentName = memo<ComponentNameProps>(
  ({
    title,
    variant = 'primary',
    size = 'medium',
    disabled = false,
    onClick,
    children,
    className = '',
    ...props
  }) => {
    // Component logic
    return (
      <div
        className={`component-name component-name--${variant} component-name--${size} ${className}`}
      >
        <h3>{title}</h3>
        {children}
        {onClick && (
          <button onClick={onClick} disabled={disabled}>
            Action
          </button>
        )}
      </div>
    );
  }
);

ComponentName.displayName = 'ComponentName';
```

### Lazy Loading

```typescript
// components/HeavyComponent/HeavyComponent.tsx
import React, { Suspense } from 'react';

const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

export const LazyHeavyComponent: React.FC = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
};
```

## Anti-Patterns (Proibidos)

### ❌ NÃO FAÇA

- **Componentes monolíticos**: Mais de 200 linhas
- **Props drilling**: Passar props através de 3+ níveis
- **Inline styles**: Exceto valores dinâmicos
- **Componentes sem TypeScript**: Sempre use types
- **Lógica de negócio em componentes**: Use custom hooks
- **Event handlers inline**: Extraia para funções

### ✅ SEMPRE FAÇA

- **Componentes pequenos e focados**: Uma responsabilidade
- **Props com defaults**: Sempre defina valores padrão
- **TypeScript interfaces**: Para type safety
- **CSS modules ou styled-components**: Para estilização
- **Testes unitários**: Para cada componente
- **Error boundaries**: Para tratamento de erros
