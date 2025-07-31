# 📦 Instalação Manual de Extensões - Wiki Veloz Fibra

## 🚀 Como Instalar as Extensões

Como o comando `code` não está disponível no terminal, você pode instalar as extensões manualmente através da interface do VS Code/Cursor.

## 📋 Extensões Essenciais para Instalar

### 📦 **Python Development**

1. Abra o VS Code/Cursor
2. Vá em **Extensions** (Ctrl+Shift+X)
3. Procure e instale:
   - **Python** (Microsoft)
   - **Pylance** (Microsoft)
   - **Black Formatter** (Microsoft)
   - **Flake8** (Microsoft)
   - **isort** (Microsoft)

### 🎨 **Frontend Development**

- **Tailwind CSS IntelliSense** (Brad Cornes)
- **Auto Rename Tag** (Jun Han)
- **Auto Close Tag** (Jun Han)
- **TypeScript** (Microsoft)

### 🔍 **Code Quality**

- **ESLint** (Microsoft)
- **Prettier** (Prettier)
- **Code Spell Checker** (Street Side Software)
- **Code Spell Checker Portuguese (Brazil)** (Street Side Software)
- **SonarLint** (SonarSource)

### 📚 **Git & Version Control**

- **GitLens** (Eric Amodio)
- **Git Graph** (mhutchie)

### 🌐 **API Testing**

- **Thunder Client** (Ranga Vadhineni)
- **REST Client** (Huachao Mao)

### ⚡ **Productivity**

- **Live Server** (Ritwick Dey)
- **JSON Tools** (Microsoft)
- **YAML** (Red Hat)
- **Markdown All in One** (Yu Zhang)

### 🎨 **Themes & Icons**

- **Material Icon Theme** (Philipp Kief)
- **Material Theme** (Equim)

## 🎯 Instalação Rápida via Marketplace

### Método 1: Links Diretos

Clique nos links abaixo para instalar diretamente:

#### Python Development

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.pylance)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)

#### Frontend Development

- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [Auto Rename Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag)
- [Auto Close Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag)

#### Code Quality

- [ESLint](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- [Code Spell Checker Portuguese](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker-portuguese-brazilian)
- [SonarLint](https://marketplace.visualstudio.com/items?itemName=sonarsource.sonarlint-vscode)

#### Git & Productivity

- [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
- [Thunder Client](https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client)
- [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

### Método 2: Busca no VS Code

1. Abra o VS Code/Cursor
2. Pressione **Ctrl+Shift+X** (ou Cmd+Shift+X no Mac)
3. Digite o nome da extensão na barra de pesquisa
4. Clique em **Install**

## ⚙️ Configurações Recomendadas

Após instalar as extensões, configure:

### 🎨 **Tema e Ícones**

1. **Ctrl+Shift+P** → "Preferences: Color Theme"
2. Selecione **Material Theme**
3. **Ctrl+Shift+P** → "Preferences: File Icon Theme"
4. Selecione **Material Icon Theme**

### 🔧 **Python Settings**

1. **Ctrl+Shift+P** → "Preferences: Open Settings (JSON)"
2. Adicione:

```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true
}
```

### 📝 **Prettier Settings**

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "prettier.singleQuote": true,
  "prettier.tabWidth": 2
}
```

## 🎯 Verificação da Instalação

### ✅ **Como Verificar se Funcionou**

1. **Python**: Digite `import` e veja autocomplete
2. **Tailwind**: Digite `bg-` e veja sugestões
3. **GitLens**: Veja informações do Git no editor
4. **Prettier**: Salve um arquivo e veja formatação automática

### 🔍 **Testes Rápidos**

1. **Abra um arquivo Python**: Deve ter syntax highlighting
2. **Digite HTML**: Tags devem fechar automaticamente
3. **Use Tailwind**: Classes devem ter autocomplete
4. **Salve arquivo**: Deve formatar automaticamente

## 🚀 Próximos Passos

Após instalar as extensões:

1. **Reinicie o VS Code/Cursor**
2. **Configure o tema Material Icon Theme**
3. **Teste as funcionalidades**
4. **Comece a desenvolver!**

## 📚 Recursos Úteis

- [VS Code Marketplace](https://marketplace.visualstudio.com/)
- [Python Extensions](https://marketplace.visualstudio.com/search?term=python)
- [Frontend Extensions](https://marketplace.visualstudio.com/search?term=frontend)
- [Productivity Extensions](https://marketplace.visualstudio.com/search?term=productivity)

---

**💡 Dica**: Se alguma extensão não funcionar, tente desinstalar e reinstalar, ou reinicie o VS Code/Cursor.

**Última atualização**: 16/07/2025
