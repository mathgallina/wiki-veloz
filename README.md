# Wiki Veloz Fibra

Sistema de wiki interna para centralizar informações, processos e documentação da empresa Veloz Fibra.

## 🚀 Características

- **Design Moderno**: Interface limpa e responsiva
- **Navegação Intuitiva**: Menu lateral organizado por categorias
- **Edição Simples**: Suporte a Markdown para formatação
- **Pesquisa Rápida**: Busca por palavras-chave
- **Dados Locais**: Armazenamento em JSON (sem banco de dados complexo)
- **Fácil Manutenção**: Código simples e personalizável

## 📋 Categorias Disponíveis

- **Visão da Empresa**: Missão, valores e objetivos
- **Processos Internos**: Fluxos de trabalho e procedimentos
- **Ferramentas Utilizadas**: Sistemas e ferramentas da empresa
- **Onboarding**: Processo de integração de novos colaboradores
- **Histórico de Mudanças**: Decisões e mudanças importantes
- **Geral**: Outros assuntos

## 🛠️ Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se estiver usando git
   git clone <url-do-repositorio>
   cd wiki-veloz
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o aplicativo**
   ```bash
   python app.py
   ```

4. **Acesse no navegador**
   ```
   http://localhost:8000
   ```

## 📁 Estrutura do Projeto

```
wiki-veloz/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── data/                 # Dados das páginas (criado automaticamente)
│   └── pages.json       # Arquivo JSON com o conteúdo
├── static/               # Arquivos estáticos
│   └── uploads/         # Uploads de arquivos
└── templates/            # Templates HTML
    └── index.html       # Template principal
```

## 🎯 Como Usar

### Visualizando Páginas
1. Acesse a wiki no navegador
2. Use o menu lateral para navegar por categorias
3. Clique em uma página para visualizar o conteúdo

### Criando Nova Página
1. Clique no botão "Nova Página" no menu lateral
2. Preencha o título, categoria e conteúdo
3. O conteúdo pode ser formatado usando Markdown
4. Clique em "Criar Página"

### Editando Páginas
1. Abra uma página existente
2. Clique no botão "Editar"
3. Modifique o conteúdo usando Markdown
4. Clique em "Salvar"

### Pesquisando
1. Use a barra de pesquisa no topo da página
2. Digite palavras-chave para encontrar páginas
3. Os resultados aparecem automaticamente

## 📝 Formatação Markdown

O sistema suporta formatação Markdown para criar conteúdo rico:

```markdown
# Título Principal
## Subtítulo
### Sub-subtítulo

**Texto em negrito**
*Texto em itálico*

- Lista com marcadores
- Outro item

1. Lista numerada
2. Segundo item

[Link](https://exemplo.com)

![Imagem](url-da-imagem)

> Citação ou destaque
```

## 🔧 Personalização

### Adicionando Novas Categorias
1. Edite o arquivo `templates/index.html`
2. Adicione a nova categoria na função `getCategoryName()`
3. Adicione a descrição na função `getCategoryDescription()`

### Modificando o Design
1. O design usa Tailwind CSS via CDN
2. Edite as classes CSS no template HTML
3. Personalize cores, fontes e layout conforme necessário

### Configurações do Backend
1. Edite `app.py` para modificar rotas e lógica
2. Adicione novas funcionalidades conforme necessário
3. Configure autenticação real se necessário

## 🚀 Deploy

### Opção 1: Local (Desenvolvimento)
```bash
python app.py
```

### Opção 2: Streamlit Cloud
1. Crie uma conta no Streamlit Cloud
2. Conecte seu repositório GitHub
3. Configure o arquivo `requirements.txt`
4. Deploy automático

### Opção 3: VPS/Server
1. Configure um servidor Linux
2. Instale Python e dependências
3. Use gunicorn para produção:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## 📊 Dados de Exemplo

O sistema vem com páginas de exemplo incluídas:
- Visão da Empresa
- Ferramentas Utilizadas
- Processos Internos
- Onboarding de Novos Colaboradores
- Histórico de Mudanças

## 🔒 Segurança

- Sistema de login simulado (pode ser expandido)
- Validação de entrada no backend
- Sanitização de conteúdo Markdown

## 🛠️ Manutenção

### Backup dos Dados
- O arquivo `data/pages.json` contém todo o conteúdo
- Faça backup regular deste arquivo
- Considere versionamento com Git

### Atualizações
1. Mantenha as dependências atualizadas
2. Teste em ambiente de desenvolvimento
3. Faça backup antes de atualizações

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do console
2. Consulte a documentação do Flask
3. Teste em diferentes navegadores

## 🎨 Tecnologias Utilizadas

- **Backend**: Python + Flask
- **Frontend**: HTML + Tailwind CSS + Alpine.js
- **Formatação**: Markdown
- **Armazenamento**: JSON
- **Deploy**: Local/Streamlit Cloud/VPS

---

**Desenvolvido para Veloz Fibra** 🚀
*Centralizando conhecimento, conectando pessoas* 