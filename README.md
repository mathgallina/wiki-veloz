# Base de Conhecimento Veloz

Sistema de base de conhecimento desenvolvido em Flask.

## 🚀 Como Rodar o Projeto no Mac

### Pré-requisitos
- Python 3.9+ instalado
- Terminal do Mac

### Passo a Passo Completo

#### 1. Navegue até a pasta do projeto
```bash
cd ~/projetos/base-conhecimento-veloz
```

#### 2. Crie o ambiente virtual (se não existir)
```bash
python3 -m venv .venv
```

#### 3. Ative o ambiente virtual
```bash
source .venv/bin/activate
```

#### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

#### 5. Execute o projeto
**Opção A - Usando o script de inicialização:**
```bash
bash scripts/start.sh
```

**Opção B - Executando diretamente:**
```bash
python3 app.py
```

#### 6. Acesse no navegador
Abra seu navegador e acesse:
- **http://localhost:8000** ou
- **http://127.0.0.1:8000**

### 🔧 Solução de Problemas

#### Se a porta 8000 estiver ocupada:

1. **Verifique quais processos estão usando a porta:**
```bash
lsof -i :8000
```

2. **Mate o processo (substitua PID_DO_PROCESSO pelo número real):**
```bash
kill -9 PID_DO_PROCESSO
```

**Exemplo:**
```bash
kill -9 88315
```

3. **Tente rodar o projeto novamente:**
```bash
python3 app.py
```

### 📁 Estrutura do Projeto

```
base-conhecimento-veloz/
├── .venv/           # Ambiente virtual Python
├── app.py           # Arquivo principal do Flask
├── static/          # Arquivos estáticos (CSS, JS, imagens)
├── templates/       # Arquivos HTML do Flask
├── scripts/start.sh # Script de inicialização
├── requirements.txt # Dependências do projeto
├── docs/           # Documentação
├── logs/           # Logs do sistema
└── README.md       # Este arquivo
```

### 🛠️ Comandos Úteis

**Para parar o servidor:**
- Pressione `Ctrl+C` no terminal

**Para verificar se o servidor está rodando:**
```bash
curl -I http://127.0.0.1:8000
```

**Para atualizar dependências:**
```bash
pip install --upgrade -r requirements.txt
```

**Para desativar o ambiente virtual:**
```bash
deactivate
```

### ✅ Status do Sistema

O servidor está configurado para:
- **Porta:** 8000
- **Modo:** Debug (desenvolvimento)
- **Host:** 127.0.0.1
- **Debugger PIN:** 126-722-987

### 🎯 Próximos Passos

1. Acesse o sistema no navegador
2. Explore as funcionalidades disponíveis
3. Para desenvolvimento, o modo debug está ativo (auto-reload)

---

**Desenvolvido com ❤️ usando Flask**
