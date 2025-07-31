# 📄 Sistema de PDFs - Wiki Veloz Fibra

## 🚀 Visão Geral

O sistema de PDFs permite fazer upload, visualizar e gerenciar documentos (PDFs, DOCs, imagens) diretamente na wiki. Os arquivos podem ser associados a páginas específicas ou ficarem disponíveis globalmente.

## ✨ Funcionalidades

### 📤 **Upload de Arquivos**

- **Drag & Drop**: Arraste arquivos diretamente para a área de upload
- **Seleção múltipla**: Faça upload de vários arquivos simultaneamente
- **Tipos suportados**: PDF, DOC, DOCX, TXT, JPG, PNG, GIF
- **Tamanho máximo**: 50MB por arquivo
- **Associação opcional**: Vincule arquivos a páginas específicas

### 👁️ **Visualização**

- **Visualizador integrado**: Visualize PDFs diretamente no navegador
- **Download**: Baixe arquivos com contador de downloads
- **Preview**: Visualização rápida de documentos

### 🔍 **Gerenciamento**

- **Busca**: Encontre arquivos por nome ou descrição
- **Filtros**: Filtre por página associada
- **Ordenação**: Ordene por data, nome, tamanho ou downloads
- **Estatísticas**: Veja contadores de download e tamanho dos arquivos

### 🛡️ **Segurança**

- **Autenticação**: Apenas usuários logados podem acessar
- **Controle de acesso**: Apenas admins podem excluir arquivos
- **Validação**: Verificação de tipos de arquivo permitidos
- **Nomes únicos**: Evita conflitos de nomes de arquivo

## 🎯 Como Usar

### 1. **Acessar o Sistema de PDFs**

1. Faça login na wiki
2. Clique no ícone de engrenagem (⚙️) no canto superior direito
3. Selecione "Gerenciar PDFs" no menu de administração
4. Ou acesse diretamente: `/admin/pdfs`

### 2. **Fazer Upload de Arquivos**

#### Método 1: Drag & Drop

1. Arraste arquivos para a área de upload
2. Os arquivos serão enviados automaticamente
3. Veja o progresso na barra de progresso

#### Método 2: Seleção Manual

1. Clique em "Selecionar Arquivos"
2. Escolha os arquivos desejados
3. Os uploads serão processados automaticamente

### 3. **Associar a Páginas (Opcional)**

1. Selecione uma página no filtro "Filtrar por Página"
2. Faça upload dos arquivos
3. Os arquivos ficarão associados à página selecionada

### 4. **Visualizar e Gerenciar**

- **Visualizar**: Clique no ícone de olho (👁️)
- **Download**: Clique no ícone de download (⬇️)
- **Excluir**: Clique no ícone de lixeira (🗑️) - apenas para admins

## 📁 Estrutura de Arquivos

```
wiki-veloz/
├── static/
│   └── uploads/          # Arquivos enviados
│       └── .gitkeep      # Mantém pasta no repositório
├── data/
│   └── pdfs.json         # Metadados dos PDFs
└── templates/
    └── admin_pdfs.html   # Interface de gerenciamento
```

## 🔧 Configuração

### Tipos de Arquivo Permitidos

```python
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "txt",
    "jpg", "jpeg", "png", "gif"
}
```

### Tamanho Máximo

```python
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB
```

### Pasta de Upload

```python
app.config["UPLOAD_FOLDER"] = "static/uploads"
```

## 📊 Estrutura de Dados

### Arquivo `data/pdfs.json`

```json
[
  {
    "id": "uuid-unico",
    "filename": "nome-unico-do-arquivo.pdf",
    "original_filename": "documento-original.pdf",
    "page_id": "id-da-pagina-opcional",
    "description": "Descrição opcional",
    "uploaded_by": "user-id",
    "uploaded_at": "2024-01-15T10:00:00",
    "file_size": 1024000,
    "download_count": 5
  }
]
```

## 🔌 APIs Disponíveis

### GET `/api/pdfs`

**Retorna lista de PDFs**

```bash
curl -H "Authorization: Bearer token" \
     "http://localhost:8000/api/pdfs?page_id=opcional"
```

### POST `/api/pdfs`

**Faz upload de arquivo**

```bash
curl -X POST \
     -F "file=@documento.pdf" \
     -F "page_id=id-da-pagina" \
     -F "description=Descrição" \
     "http://localhost:8000/api/pdfs"
```

### DELETE `/api/pdfs/<pdf_id>`

**Remove um PDF**

```bash
curl -X DELETE \
     "http://localhost:8000/api/pdfs/pdf-id"
```

### GET `/uploads/<filename>`

**Download de arquivo**

```bash
curl -O "http://localhost:8000/uploads/nome-do-arquivo"
```

### GET `/api/pdfs/<pdf_id>/view`

**Visualiza PDF no navegador**

```bash
curl "http://localhost:8000/api/pdfs/pdf-id/view"
```

## 🎨 Interface do Usuário

### Características da Interface

- **Design responsivo**: Funciona em desktop e mobile
- **Tema escuro/claro**: Suporte a ambos os temas
- **Upload drag & drop**: Interface intuitiva
- **Filtros avançados**: Busca e ordenação
- **Visualizador modal**: PDFs em popup
- **Progresso em tempo real**: Feedback visual

### Componentes Principais

1. **Área de Upload**: Drag & drop com progresso
2. **Filtros**: Busca, página, ordenação
3. **Lista de Arquivos**: Cards com informações
4. **Visualizador**: Modal para PDFs
5. **Ações**: Visualizar, download, excluir

## 🔒 Segurança e Permissões

### Controle de Acesso

- **Upload**: Todos os usuários logados
- **Visualização**: Todos os usuários logados
- **Download**: Todos os usuários logados
- **Exclusão**: Apenas administradores

### Validações

- **Tipo de arquivo**: Apenas extensões permitidas
- **Tamanho**: Máximo 50MB
- **Autenticação**: Login obrigatório
- **Autorização**: Verificação de permissões

## 📈 Estatísticas e Analytics

### Métricas Coletadas

- **Downloads**: Contador por arquivo
- **Uploads**: Data e usuário
- **Tamanho**: Tamanho dos arquivos
- **Associações**: Páginas vinculadas

### Logs de Atividade

```json
{
  "user_id": "user-001",
  "action": "pdf_uploaded",
  "details": "PDF enviado: documento.pdf",
  "timestamp": "2024-01-15T10:00:00",
  "ip_address": "127.0.0.1"
}
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. **Arquivo não enviado**

- Verifique o tamanho (máx. 50MB)
- Confirme o tipo de arquivo
- Verifique a conexão com a internet

#### 2. **Erro de permissão**

- Faça login novamente
- Verifique se tem permissão de admin para exclusão

#### 3. **PDF não visualiza**

- Verifique se o navegador suporta PDF
- Tente fazer download e abrir localmente

#### 4. **Pasta uploads não existe**

```bash
mkdir -p static/uploads
chmod 755 static/uploads
```

### Logs de Erro

Verifique os logs do Flask para erros:

```bash
tail -f app.log
```

## 🔄 Integração com Backup

O sistema de PDFs está integrado ao sistema de backup:

### Backup Automático

- **Inclusão**: PDFs são incluídos nos backups
- **Configuração**: `"include_uploads": true`
- **Estrutura**: `uploads/` no arquivo de backup

### Restauração

- **Arquivos**: Restaurados automaticamente
- **Metadados**: Preservados no `pdfs.json`
- **Associações**: Mantidas com páginas

## 🎯 Próximas Melhorias

### Funcionalidades Planejadas

1. **Comentários**: Comentários em PDFs
2. **Versões**: Controle de versão de arquivos
3. **Tags**: Sistema de tags para organização
4. **Compartilhamento**: Links públicos para PDFs
5. **OCR**: Extração de texto de imagens
6. **Preview**: Thumbnails de imagens

### Melhorias Técnicas

1. **Compressão**: Compressão automática de imagens
2. **CDN**: Distribuição de conteúdo
3. **Cache**: Cache de visualização
4. **Streaming**: Streaming de vídeos
5. **API**: API REST completa

## 📚 Recursos Úteis

### Documentação Relacionada

- [Sistema de Backup](./SISTEMA_BACKUP.md)
- [Gerenciamento de Usuários](./GERENCIAMENTO_USUARIOS.md)
- [Analytics](./ANALYTICS_GUIDE.md)

### Comandos Úteis

```bash
# Verificar espaço em disco
df -h static/uploads/

# Listar arquivos maiores
find static/uploads/ -type f -size +10M

# Limpar arquivos antigos (cuidado!)
find static/uploads/ -type f -mtime +30 -delete
```

---

**💡 Dica**: Use o sistema de PDFs para centralizar documentos importantes da empresa, como manuais, procedimentos e relatórios.

**Última atualização**: 16/07/2025
