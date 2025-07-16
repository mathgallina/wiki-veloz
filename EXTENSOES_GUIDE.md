# 🚀 Guia de Extensões - Wiki Veloz Fibra

## 📋 Visão Geral

Este guia lista as extensões essenciais para desenvolver a wiki da Veloz Fibra com máxima produtividade e qualidade de código.

## 🎯 Extensões Essenciais

### 📦 **Python Development**

| Extensão            | Descrição                  | Benefício                        |
| ------------------- | -------------------------- | -------------------------------- |
| **Python**          | Suporte completo ao Python | IntelliSense, debugging, linting |
| **Pylance**         | IntelliSense avançado      | Autocomplete inteligente         |
| **Black Formatter** | Formatação automática      | Código consistente               |
| **Flake8**          | Análise estática           | Detecção de erros                |
| **isort**           | Organização de imports     | Imports organizados              |

### 🎨 **Frontend Development**

| Extensão                      | Descrição                  | Benefício                   |
| ----------------------------- | -------------------------- | --------------------------- |
| **Tailwind CSS IntelliSense** | Autocomplete Tailwind      | Desenvolvimento mais rápido |
| **Auto Rename Tag**           | Renomeia tags HTML         | Produtividade               |
| **Auto Close Tag**            | Fecha tags automaticamente | Menos digitação             |
| **TypeScript**                | Suporte a TypeScript       | Melhor desenvolvimento JS   |

### 🔍 **Code Quality**

| Extensão                | Descrição                | Benefício           |
| ----------------------- | ------------------------ | ------------------- |
| **ESLint**              | Análise estática JS      | Detecção de erros   |
| **Prettier**            | Formatação automática    | Código consistente  |
| **Code Spell Checker**  | Verificação ortográfica  | Textos sem erros    |
| **SonarLint**           | Detecção de bugs         | Qualidade de código |
| **Portuguese (Brazil)** | Verificação em português | Textos em português |

### 📚 **Git & Version Control**

| Extensão      | Descrição           | Benefício                 |
| ------------- | ------------------- | ------------------------- |
| **GitLens**   | Histórico detalhado | Rastreamento de mudanças  |
| **Git Graph** | Visualização do Git | Entendimento do histórico |

### 🌐 **API Testing**

| Extensão           | Descrição     | Benefício           |
| ------------------ | ------------- | ------------------- |
| **Thunder Client** | Teste de APIs | Testes rápidos      |
| **REST Client**    | Cliente REST  | Testes de endpoints |

### ⚡ **Productivity**

| Extensão        | Descrição          | Benefício             |
| --------------- | ------------------ | --------------------- |
| **Live Server** | Servidor local     | Preview em tempo real |
| **JSON Tools**  | Ferramentas JSON   | Manipulação de dados  |
| **YAML**        | Suporte a YAML     | Configurações         |
| **Markdown**    | Suporte a Markdown | Documentação          |

## 🚀 Instalação Rápida

### Método 1: Script Automático

```bash
# Execute o script de instalação
./install-extensions.sh
```

### Método 2: Instalação Manual

```bash
# Python Development
code --install-extension ms-python.python
code --install-extension ms-python.pylance
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
code --install-extension ms-python.isort

# Frontend Development
code --install-extension bradlc.vscode-tailwindcss
code --install-extension formulahendry.auto-rename-tag
code --install-extension formulahendry.auto-close-tag

# Code Quality
code --install-extension ms-vscode.vscode-eslint
code --install-extension ms-vscode.vscode-prettier
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension streetsidesoftware.code-spell-checker-portuguese-brazilian

# Git & Productivity
code --install-extension eamodio.gitlens
code --install-extension rangav.vscode-thunder-client
code --install-extension ms-vscode.live-server
```

## ⚙️ Configurações Recomendadas

### 🎨 **Tema e Ícones**

```json
{
  "workbench.iconTheme": "material-icon-theme",
  "workbench.colorTheme": "Material Theme",
  "editor.fontSize": 14,
  "editor.fontFamily": "'Fira Code', 'Consolas', 'Courier New', monospace"
}
```

### 🔧 **Python Settings**

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.sortImports.args": ["--profile", "black"]
}
```

### 🎨 **Tailwind CSS Settings**

```json
{
  "tailwindCSS.includeLanguages": {
    "html": "html",
    "javascript": "javascript"
  },
  "tailwindCSS.experimental.classRegex": [
    ["classList.add\\(([^)]*)\\)", "([^)]*)"],
    ["className\\s*=\\s*['\"`]([^'\"`]*)['\"`]", "([^'\"`]*)"]
  ]
}
```

### 📝 **Prettier Settings**

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "prettier.singleQuote": true,
  "prettier.tabWidth": 2,
  "prettier.semi": true
}
```

## 🎯 Como Usar

### 📊 **Para Desenvolvimento Python**

1. **Debugging**: Use F5 para debugar
2. **Linting**: Erros aparecem automaticamente
3. **Formatting**: Ctrl+Shift+P → "Format Document"
4. **Import Sorting**: Ctrl+Shift+P → "Sort Imports"

### 🎨 **Para Desenvolvimento Frontend**

1. **Tailwind Autocomplete**: Digite classes e veja sugestões
2. **Live Preview**: Use Live Server para preview
3. **API Testing**: Use Thunder Client para testar APIs
4. **Git History**: Use GitLens para ver histórico

### 🔍 **Para Qualidade de Código**

1. **Spell Check**: Erros ortográficos aparecem sublinhados
2. **ESLint**: Problemas de JavaScript são destacados
3. **SonarLint**: Bugs e vulnerabilidades são detectados
4. **Prettier**: Formatação automática ao salvar

## 📚 Extensões Específicas para o Projeto

### 🌐 **Para APIs Flask**

- **Thunder Client**: Testa endpoints `/api/*`
- **REST Client**: Cria arquivos `.http` para testes
- **JSON Tools**: Manipula respostas JSON

### 🎨 **Para Tailwind CSS**

- **Tailwind CSS IntelliSense**: Autocomplete de classes
- **Auto Rename Tag**: Edita tags HTML facilmente
- **Bracket Pair Colorizer**: Visualiza estrutura do código

### 📊 **Para Analytics**

- **JSON Tools**: Analisa dados exportados
- **Markdown**: Visualiza documentação
- **GitLens**: Rastreia mudanças no código

## 🚀 Dicas de Produtividade

### ⌨️ **Atalhos Úteis**

- `Ctrl+Shift+P`: Command Palette
- `F5`: Debug
- `Ctrl+Space`: Autocomplete
- `Ctrl+Shift+F`: Buscar em arquivos
- `Ctrl+D`: Selecionar próxima ocorrência

### 🔧 **Configurações Avançadas**

1. **Auto Save**: Salva automaticamente
2. **Format on Save**: Formata ao salvar
3. **Minimap**: Mostra visão geral do arquivo
4. **Word Wrap**: Quebra linhas longas

### 📊 **Debugging**

1. **Python**: Configure breakpoints com F9
2. **JavaScript**: Use console.log() e debugger
3. **Network**: Use DevTools para APIs
4. **Performance**: Use Profiler para otimização

## 🎯 Próximos Passos

### 📦 **Extensões Futuras**

- [ ] **Docker**: Para containerização
- [ ] **Database**: Para conexão com banco
- [ ] **Testing**: Para testes automatizados
- [ ] **Deployment**: Para deploy automático

### 🔧 **Configurações Avançadas**

- [ ] **Workspace Settings**: Configurações específicas do projeto
- [ ] **Task Runner**: Automação de tarefas
- [ ] **Snippets**: Templates de código
- [ ] **Themes**: Temas customizados

---

**💡 Dica**: Após instalar as extensões, reinicie o VS Code/Cursor para garantir que todas funcionem corretamente.

**📚 Recursos**:

- [VS Code Marketplace](https://marketplace.visualstudio.com/)
- [Python Extensions](https://marketplace.visualstudio.com/search?term=python)
- [Frontend Extensions](https://marketplace.visualstudio.com/search?term=frontend)

**Última atualização**: 16/07/2025
