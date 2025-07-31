# Padrões React - CDD v2.0

## Estrutura de Componentes

### Componente Funcional (Obrigatório)

```typescript
import React from 'react';
import type { ComponentProps } from './Component.types';

interface ComponentProps {
  title: string;
  onAction?: () => void;
  disabled?: boolean;
}

export const Component: React.FC<ComponentProps> = ({
  title,
  onAction,
  disabled = false,
}) => {
  const handleClick = () => {
    if (!disabled && onAction) {
      onAction();
    }
  };

  return (
    <div className='component'>
      <h2>{title}</h2>
      <button onClick={handleClick} disabled={disabled}>
        Action
      </button>
    </div>
  );
};
```

### Hooks Customizados

```typescript
// hooks/useCustomHook.ts
import { useState, useEffect } from 'react';

interface UseCustomHookOptions {
  initialValue?: string;
  autoSave?: boolean;
}

export const useCustomHook = (options: UseCustomHookOptions = {}) => {
  const [value, setValue] = useState(options.initialValue || '');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (options.autoSave && value) {
      // Auto-save logic
    }
  }, [value, options.autoSave]);

  return {
    value,
    setValue,
    isLoading,
  };
};
```

## Padrões de Estado

### Context API (Para estado global)

```typescript
// contexts/AppContext.tsx
import React, { createContext, useContext, useReducer } from 'react';

interface AppState {
  user: User | null;
  theme: 'light' | 'dark';
}

type AppAction =
  | { type: 'SET_USER'; payload: User }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' };

const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>{children}</AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
```

## Padrões de Formulários

### Form com Validação

```typescript
// components/forms/ValidatedForm.tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const formSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(8, 'Senha deve ter pelo menos 8 caracteres'),
});

type FormData = z.infer<typeof formSchema>;

export const ValidatedForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = async (data: FormData) => {
    try {
      // Submit logic
      console.log(data);
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input {...register('email')} placeholder='Email' />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <input type='password' {...register('password')} placeholder='Senha' />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <button type='submit' disabled={isSubmitting}>
        {isSubmitting ? 'Enviando...' : 'Enviar'}
      </button>
    </form>
  );
};
```

## Padrões de Performance

### Memoização de Componentes

```typescript
// components/ExpensiveComponent.tsx
import React, { memo, useMemo } from 'react';

interface ExpensiveComponentProps {
  data: Array<{ id: string; value: number }>;
  filter: string;
}

export const ExpensiveComponent = memo<ExpensiveComponentProps>(({ data, filter }) => {
  const filteredData = useMemo(() => {
    return data.filter(item => item.value.toString().includes(filter));
  }, [data, filter]);

  return (
    <div>
      {filteredData.map(item => (
        <div key={item.id}>{item.value}</div>
      ))}
    </div>
  );
});
```

### Lazy Loading

```typescript
// pages/LazyPage.tsx
import React, { Suspense } from 'react';

const LazyComponent = React.lazy(() => import('../components/HeavyComponent'));

export const LazyPage: React.FC = () => {
  return (
    <div>
      <h1>Página com Lazy Loading</h1>
      <Suspense fallback={<div>Carregando...</div>}>
        <LazyComponent />
      </Suspense>
    </div>
  );
};
```

## Padrões de Teste

### Teste de Componente

```typescript
// components/Component.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Component } from './Component';

describe('Component', () => {
  it('should render with title', () => {
    render(<Component title='Test Title' />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('should call onAction when button is clicked', () => {
    const mockAction = jest.fn();
    render(<Component title='Test' onAction={mockAction} />);

    fireEvent.click(screen.getByText('Action'));
    expect(mockAction).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Component title='Test' disabled={true} />);
    expect(screen.getByText('Action')).toBeDisabled();
  });
});
```

## Anti-Patterns (Proibidos)

### ❌ NÃO FAÇA

- **Componentes muito grandes**: Mais de 200 linhas
- **Props drilling**: Passar props através de muitos níveis
- **Side effects em render**: useEffect sem dependências
- **Inline styles**: Exceto valores dinâmicos
- **Componentes sem TypeScript**: Sempre use types

### ✅ SEMPRE FAÇA

- **Componentes pequenos e focados**: Uma responsabilidade
- **Custom hooks**: Para lógica reutilizável
- **TypeScript**: Para type safety
- **Error boundaries**: Para tratamento de erros
- **Loading states**: Para melhor UX
