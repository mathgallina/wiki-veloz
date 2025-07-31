# Prompt Direto: Geração da Pasta Patterns

Analise os arquivos `.kiro/steering/` (product.md, structure.md, tech.md) e crie uma pasta `.kiro/patterns/` completa com padrões de código específicos para as tecnologias do projeto.

## Estrutura a criar:

```
.kiro/patterns/
├── README.md                 # Índice e visão geral
├── conventions.md            # Nomenclatura e convenções gerais  
├── architecture.md           # Padrões arquiteturais
├── security.md              # Diretrizes de segurança
├── performance.md           # Otimizações e performance
├── testing.md               # Padrões de teste
├── frontend/                # Padrões frontend específicos
├── backend/                 # Padrões backend específicos  
├── database/                # Padrões de banco de dados
├── examples/                # Exemplos práticos de código
└── linting/                 # Configurações customizadas
```

## Para cada tecnologia identificada no tech.md, crie:

**TypeScript**: patterns/typescript.md com regras ✅ permitido / ❌ proibido
**React**: patterns/frontend/react.md com padrões de componentes, hooks, estado
**Node.js**: patterns/backend/nodejs.md com controllers, middleware, error handling
**Database**: patterns/database/[tipo].md com queries, models, migrations
**Testing**: patterns/testing.md com estrutura, nomenclatura, coverage

## Inclua em cada arquivo:

1. **Regras claras**: O que pode e não pode ser feito
2. **Exemplos práticos**: Código funcional demonstrando padrões
3. **Justificativas**: Por que seguir cada padrão
4. **Configurações**: ESLint, Prettier, TSConfig customizados
5. **Integração**: Como aplicar no workflow diário

## Exemplos de conteúdo:

```markdown
# Padrões TypeScript

## ✅ PERMITIDO
- Strict mode sempre ativo
- Types explícitos para APIs públicas
- Interfaces para objetos complexos

## ❌ PROIBIDO
- Uso de `any` sem justificativa
- @ts-ignore sem comentário explicativo
- Tipos implícitos em funções exportadas

## Exemplo Correto
[código TypeScript seguindo padrões]
```

Gere TODOS os arquivos preenchidos com conteúdo específico baseado nas tecnologias reais do projeto, criando uma fonte única da verdade para padrões de código. 