# Wiki Veloz - Estrutura Refatorada

## 📁 Nova Estrutura do Projeto

```
wiki-veloz/
├── app.py                          # Entry point limpo
├── app/                            # Aplicação principal
│   ├── __init__.py                # Factory pattern
│   ├── core/                      # Configurações centrais
│   │   ├── __init__.py
│   │   ├── config.py              # Configurações da aplicação
│   │   └── database.py            # Configurações de banco
│   ├── modules/                   # Módulos da aplicação
│   │   ├── __init__.py
│   │   ├── main/                  # Rotas principais
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── auth/                  # Autenticação
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── services/
│   │   │   └── validators/
│   │   ├── users/                 # Gerenciamento de usuários
│   │   ├── pages/                 # Gerenciamento de páginas
│   │   ├── documents/             # Gerenciamento de documentos
│   │   ├── pdfs/                  # Gerenciamento de PDFs
│   │   ├── notifications/         # Sistema de notificações
│   │   ├── analytics/             # Analytics e relatórios
│   │   └── backup/                # Sistema de backup
│   ├── shared/                    # Componentes compartilhados
│   │   ├── __init__.py
│   │   ├── decorators.py          # Decoradores customizados
│   │   ├── exceptions.py          # Exceções personalizadas
│   │   └── utils.py               # Utilitários
│   ├── static/                    # Arquivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   ├── templates/                 # Templates HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   └── admin/
│   └── data/                      # Dados JSON
│       ├── users.json
│       ├── pages.json
│       ├── notifications.json
│       └── activity_log.json
├── tests/                         # Testes automatizados
├── requirements.txt                # Dependências Python
├── Procfile                       # Configuração Heroku
└── README.md                      # Documentação
```

## 🎯 Principais Melhorias

### 1. **Estrutura Modular**
- Cada funcionalidade em seu próprio módulo
- Separação clara entre rotas, serviços e repositórios
- Padrão Repository para acesso a dados

### 2. **Factory Pattern**
- `app.py` limpo e focado apenas na inicialização
- `app/__init__.py` com factory pattern
- Registro automático de blueprints

### 3. **Componentes Compartilhados**
- Decoradores reutilizáveis
- Exceções personalizadas
- Utilitários centralizados

### 4. **Configuração Centralizada**
- Configurações em `app/core/config.py`
- Diferentes ambientes (dev, prod, test)
- Variáveis de ambiente organizadas

## 🚀 Como Executar

### Desenvolvimento
```bash
python app.py
```

### Produção
```bash
export FLASK_ENV=production
python app.py
```

## 📋 Módulos Implementados

### ✅ Módulos Completos
- **auth**: Autenticação e login
- **main**: Rotas principais
- **shared**: Componentes compartilhados
- **core**: Configurações

### 🔄 Módulos em Desenvolvimento
- **users**: Gerenciamento de usuários
- **pages**: Gerenciamento de páginas
- **documents**: Gerenciamento de documentos
- **pdfs**: Gerenciamento de PDFs
- **notifications**: Sistema de notificações
- **analytics**: Analytics e relatórios
- **backup**: Sistema de backup

## 🛠️ Próximos Passos

1. **Migrar lógica de negócio** dos módulos existentes
2. **Implementar testes** para cada módulo
3. **Adicionar validação** de dados
4. **Implementar logging** estruturado
5. **Configurar CI/CD** com a nova estrutura

## 📊 Métricas de Limpeza

- ✅ **Arquivos removidos**: 15+ arquivos desnecessários
- ✅ **Estrutura organizada**: Padrão profissional
- ✅ **Código modular**: Separação de responsabilidades
- ✅ **Configuração centralizada**: Fácil manutenção
- ✅ **Componentes reutilizáveis**: Decoradores e utilitários

## 🔧 Comandos Úteis

```bash
# Executar aplicação
python app.py

# Executar testes
python -m pytest tests/

# Verificar estrutura
tree app/ -I "__pycache__"

# Limpar cache
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

**Status**: ✅ Estrutura refatorada e organizada
**Próximo**: Migrar lógica de negócio dos módulos existentes
