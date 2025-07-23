# Organização & Estrutura - CDD v2.0

## Filosofia de Organização

O Wiki Veloz segue uma arquitetura **feature-based** com separação clara de responsabilidades, priorizando:

### Separation of Concerns

- **Feature-based**: Organização por funcionalidades de negócio
- **Layer-based**: Separação por responsabilidades técnicas
- **Shared**: Componentes e utilitários compartilhados
- **Domain-driven**: Estrutura alinhada com domínios de negócio

### Princípios de Organização

1. **Simplicidade**: Estrutura intuitiva e fácil de navegar
2. **Escalabilidade**: Suporte a crescimento sem refatoração
3. **Manutenibilidade**: Fácil localização e modificação de código
4. **Testabilidade**: Estrutura que facilita testes automatizados
5. **Performance**: Organização que otimiza carregamento

## Estrutura de Diretórios Detalhada

```
wiki-veloz/
├── app.py                    # Entry point da aplicação
├── requirements.txt          # Dependências Python
├── package.json             # Dependências Node.js
├── tailwind.config.js       # Configuração Tailwind
├── docker-compose.yml       # Configuração Docker
├── Dockerfile               # Container da aplicação
├── Procfile                 # Configuração Heroku
├── runtime.txt              # Versão Python
├── .env.example             # Variáveis de ambiente
├── .gitignore               # Arquivos ignorados
├── README.md                # Documentação principal
├── Makefile                 # Comandos de automação
├── pyproject.toml           # Configuração Python
├── bandit-report.json       # Relatório de segurança
├── cookies.txt              # Cookies de sessão
├── CREDENCIAIS_GOOGLE_DRIVE.md # Configuração Google Drive
├── EXTENSOES_GUIDE.md       # Guia de extensões
├── GERENCIAMENTO_USUARIOS.md # Gestão de usuários
├── GUIA_BACKUP_RAPIDO.md    # Backup rápido
├── INSTRUCOES.md            # Instruções gerais
├── KIRO_INTEGRATION.md      # Integração KIRO
├── RESUMO_PDFS.md           # Resumo de PDFs
├── SISTEMA_BACKUP.md        # Sistema de backup
├── SISTEMA_NOTIFICACOES.md  # Sistema de notificações
├── SISTEMA_PDFS.md          # Sistema de PDFs
├── ANALYTICS_GUIDE.md       # Guia de analytics
├── deploy-github.md         # Deploy GitHub
├── install-extensions.sh    # Script de instalação
├── install-extensions-manual.md # Instalação manual
├── setup-dev.sh             # Setup de desenvolvimento
├── setup_google_drive_simple.py # Setup Google Drive
├── backup_system.py         # Sistema de backup
├── backup_system_simple.py  # Backup simplificado
├── backup_config.json       # Configuração de backup
├── debug_upload.py          # Debug de upload
├── test_editor_upload.py    # Teste de upload
├── test_editor_upload_simple.py # Teste simplificado
├── test_pdfs_setores.py     # Teste de PDFs
├── test_download_test_document.txt # Teste de download
├── data/                    # Dados da aplicação
│   ├── users.json           # Usuários
│   ├── pages.json           # Páginas
│   ├── pdfs.json            # PDFs
│   ├── notifications.json   # Notificações
│   └── activity_log.json    # Log de atividades
├── static/                  # Arquivos estáticos
│   └── uploads/             # Uploads de usuários
├── templates/               # Templates HTML
│   ├── index.html           # Página principal
│   ├── login.html           # Página de login
│   ├── admin_users.html     # Admin usuários
│   ├── admin_pdfs.html      # Admin PDFs
│   ├── admin_notifications.html # Admin notificações
│   ├── admin_backup.html    # Admin backup
│   ├── admin_analytics.html # Admin analytics
│   └── admin_activity.html  # Admin atividades
├── tests/                   # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py          # Configuração pytest
│   ├── test_users.py        # Testes de usuários
│   ├── test_pdfs.py         # Testes de PDFs
│   ├── test_login.py        # Testes de login
│   ├── test_google_drive.py # Testes Google Drive
│   └── test_google_drive_fixed.py # Testes corrigidos
├── backups/                 # Backups automáticos
└── .kiro/                   # CDD v2.0 structure
    ├── steering/            # Direcionamento estratégico
    │   ├── product.md       # Visão de produto
    │   ├── structure.md     # Este arquivo
    │   └── tech.md          # Decisões técnicas
    ├── patterns/            # Padrões de código
    │   ├── README.md        # Índice de padrões
    │   ├── conventions.md   # Convenções gerais
    │   ├── architecture.md  # Padrões arquiteturais
    │   ├── typescript.md    # Padrões TypeScript
    │   ├── frontend/        # Padrões frontend
    │   │   ├── react.md     # Padrões React
    │   │   └── components.md # Padrões de componentes
    │   ├── backend/         # Padrões backend
    │   │   └── nodejs.md    # Padrões Node.js
    │   ├── database/        # Padrões database
    │   │   └── postgresql.md # Padrões PostgreSQL
    │   ├── examples/        # Exemplos práticos
    │   │   └── react-component-example.tsx
    │   └── linting/         # Configurações de linting
    ├── scripts/             # Scripts de automação
    │   ├── package.json     # Dependências Node.js
    │   ├── task-manager.js  # Gerenciador de tasks
    │   ├── validate-task-format.sh # Validação de formato
    │   ├── backup-tasks.sh  # Backup de tasks
    │   ├── health-dashboard.sh # Dashboard de saúde
    │   ├── weekly-cleanup.sh # Limpeza semanal
    │   └── new-feature.sh   # Criação de features
    └── specs/               # Especificações
        ├── _template/       # Templates
        │   ├── requirements.md # Template requirements
        │   ├── design.md    # Template design
        │   └── tasks.md     # Template tasks
        ├── user-authentication/ # Feature exemplo
        │   ├── requirements.md
        │   ├── design.md
        │   └── tasks.md
        └── payment-gateway/ # Feature exemplo
            ├── requirements.md
            ├── design.md
            └── tasks.md
```

## Convenções de Nomenclatura (Rígidas)

### Arquivos Python

- **Módulos**: `snake_case.py` (ex: `user_service.py`)
- **Classes**: `PascalCase` (ex: `UserService`)
- **Funções**: `snake_case` (ex: `create_user`)
- **Variáveis**: `snake_case` (ex: `user_data`)
- **Constantes**: `UPPER_SNAKE_CASE` (ex: `MAX_RETRY_COUNT`)

### Arquivos JavaScript/TypeScript

- **Componentes React**: `PascalCase.tsx` (ex: `UserProfile.tsx`)
- **Hooks**: `camelCase.ts` (ex: `useUser.ts`)
- **Utilitários**: `camelCase.ts` (ex: `formatDate.ts`)
- **Types**: `camelCase.types.ts` (ex: `user.types.ts`)
- **Constants**: `UPPER_SNAKE_CASE.ts` (ex: `API_ENDPOINTS.ts`)

### Diretórios

- **Geral**: `kebab-case` (ex: `user-management`)
- **Componentes**: `PascalCase` (ex: `UserProfile`)
- **Features**: `kebab-case` (ex: `payment-gateway`)
- **Scripts**: `kebab-case` (ex: `backup-tasks`)

### Padrões de Import (Obrigatórios)

#### Python

```python
# 1. Standard library imports (alfabética)
import os
import sys
from datetime import datetime
from typing import List, Optional

# 2. Third-party imports (alfabética)
import flask
import requests
from google.oauth2 import service_account

# 3. Local imports (alfabética)
from models.user import User
from services.auth_service import AuthService
from utils.validators import validate_email
```

#### TypeScript/JavaScript

```typescript
// 1. External libraries (alfabética)
import React from 'react';
import axios from 'axios';

// 2. Internal modules (absolute paths - alfabética)
import { Button } from '@/components/ui/Button';
import { UserService } from '@/services/UserService';

// 3. Relative imports (alfabética)
import { validateForm } from '../utils/validation';
import './Component.css';

// 4. Type-only imports (separados)
import type { User } from '@/types/user.types';
```

## Estrutura de Features

### Template de Feature

```
features/feature-name/
├── components/              # Componentes específicos
│   ├── FeatureComponent.tsx
│   └── FeatureComponent.test.tsx
├── hooks/                   # Hooks customizados
│   └── useFeature.ts
├── services/                # Serviços da feature
│   └── featureService.ts
├── types/                   # Tipos TypeScript
│   └── feature.types.ts
├── utils/                   # Utilitários
│   └── featureUtils.ts
└── index.ts                 # Barrel export
```

### Estrutura de Componentes

```
components/ComponentName/
├── index.ts                 # Barrel export
├── ComponentName.tsx        # Main component
├── ComponentName.test.tsx   # Tests
├── ComponentName.stories.tsx # Storybook
├── ComponentName.types.ts   # Type definitions
└── ComponentName.styles.ts  # Styled components
```

## Padrões de Organização

### Separação por Responsabilidade

- **Presentation**: Templates, componentes UI, estilos
- **Business Logic**: Services, validators, business rules
- **Data Access**: Models, repositories, database queries
- **Infrastructure**: Config, utilities, external integrations

### Organização por Domínio

- **User Management**: Usuários, autenticação, permissões
- **Content Management**: Páginas, documentos, versionamento
- **File Management**: Uploads, PDFs, integração Google Drive
- **Notification System**: Alertas, notificações, emails
- **Analytics**: Métricas, relatórios, insights

## Anti-Patterns (Proibidos)

### ❌ NÃO FAÇA

- **Nomes genéricos**: `utils.py`, `helper.ts`, `Component1.tsx`
- **Imports relativos longos**: `../../../components/Button`
- **Arquivos monolíticos**: Mais de 300 linhas sem modularização
- **Misturar responsabilidades**: Lógica de negócio em componentes
- **Estrutura plana**: Todos os arquivos na raiz
- **Nomes não descritivos**: `data.json`, `config.py`

### ✅ SEMPRE FAÇA

- **Nomes descritivos e específicos**: `UserAuthenticationService.ts`
- **Absolute paths**: `@/components/Button`
- **Arquivos modulares**: Máximo 200-250 linhas
- **Separação clara**: Uma responsabilidade por arquivo
- **Estrutura hierárquica**: Organização lógica em diretórios
- **Documentação**: README.md em cada diretório principal

## Padrões de Configuração

### Arquivos de Configuração

- **Environment**: `.env` para variáveis de ambiente
- **Application**: `config.py` para configurações da app
- **Build**: `package.json`, `requirements.txt`
- **Deployment**: `Dockerfile`, `docker-compose.yml`
- **Development**: `.eslintrc.js`, `tailwind.config.js`

### Convenções de Configuração

- **Desenvolvimento**: Configurações locais em `.env.local`
- **Teste**: Configurações de teste em `.env.test`
- **Produção**: Configurações de produção em variáveis de ambiente
- **Sensível**: Nunca commitar secrets, usar `.env.example`

## Padrões de Documentação

### README.md Obrigatório

Cada diretório principal deve ter um README.md com:

- **Propósito**: O que o diretório contém
- **Estrutura**: Lista de arquivos importantes
- **Como usar**: Exemplos de uso
- **Dependências**: O que é necessário para usar

### Documentação de Código

- **Docstrings**: Para todas as funções e classes
- **Type hints**: Para Python e TypeScript
- **Comments**: Para lógica complexa
- **Examples**: Exemplos de uso em docstrings

## Padrões de Versionamento

### Estrutura de Commits

```
feat: adiciona sistema de notificações
fix: corrige bug no upload de PDFs
docs: atualiza documentação de API
style: formata código conforme padrões
refactor: refatora serviço de autenticação
test: adiciona testes para UserService
chore: atualiza dependências
```

### Branching Strategy

- **main**: Código de produção
- **develop**: Código em desenvolvimento
- **feature/**: Novas funcionalidades
- **hotfix/**: Correções urgentes
- **release/**: Preparação para release
