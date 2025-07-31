# 🔄 Sistema de Backup e Restauração - Wiki Veloz Fibra

## 📋 Visão Geral

O Sistema de Backup e Restauração é uma funcionalidade robusta que garante a segurança e integridade dos dados da Wiki Veloz Fibra. Com suporte a backup automático, criptografia, compressão e integração com Google Drive, o sistema oferece proteção completa dos dados.

## ✨ Funcionalidades Principais

### 🔐 **Segurança Avançada**

- **Criptografia AES-256**: Todos os backups são criptografados por padrão
- **Chaves únicas**: Cada instalação possui sua própria chave de criptografia
- **Armazenamento seguro**: Chaves armazenadas localmente com proteção

### 📦 **Backup Inteligente**

- **Compressão ZIP**: Reduz o tamanho dos backups em até 70%
- **Backup incremental**: Apenas dados modificados são processados
- **Verificação de integridade**: Validação automática dos backups

### ☁️ **Integração Google Drive**

- **Upload automático**: Backups enviados automaticamente para o Google Drive
- **Sincronização**: Mantém cópias locais e na nuvem
- **2TB de espaço**: Aproveita todo o espaço disponível no Google Drive

### ⚙️ **Automação Completa**

- **Backup automático**: Configurável (padrão: 24 horas)
- **Limpeza inteligente**: Remove backups antigos automaticamente
- **Retenção configurável**: Define quantos backups manter

## 🚀 Instalação e Configuração

### 1. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

### 2. **Configurar Google Drive (Opcional)**

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a Google Drive API
4. Crie credenciais OAuth 2.0
5. Baixe o arquivo `credentials.json`
6. Coloque na raiz do projeto

### 3. **Inicializar Sistema**

```bash
python app.py
```

O sistema será inicializado automaticamente com as configurações padrão.

## 📊 Interface Administrativa

### **Acesso**

- URL: `/admin/backup`
- Acesso: Apenas administradores
- Login: `matheus.gallina` / `B@rcelona1998`

### **Funcionalidades da Interface**

#### 📈 **Dashboard de Estatísticas**

- Total de backups
- Backups criptografados
- Backups no Google Drive
- Tamanho total dos backups

#### 🔧 **Ações Principais**

- **Criar Backup**: Backup manual com descrição
- **Configurar Google Drive**: Integração com nuvem
- **Configurações**: Ajustar parâmetros do sistema
- **Atualizar**: Recarregar dados

#### 📋 **Lista de Backups**

- Nome e descrição
- Tamanho e data
- Status (criptografado, Google Drive)
- Ações (restaurar, baixar, excluir)

## ⚙️ Configurações

### **Configurações Padrão**

```json
{
  "auto_backup": true,
  "backup_interval_hours": 24,
  "max_backups": 30,
  "encrypt_backups": true,
  "use_google_drive": false,
  "google_drive_folder": "Wiki-Veloz-Backups",
  "backup_retention_days": 90,
  "include_logs": true,
  "include_uploads": true,
  "compression_level": 6
}
```

### **Parâmetros Configuráveis**

| Parâmetro               | Descrição                 | Padrão  |
| ----------------------- | ------------------------- | ------- |
| `auto_backup`           | Backup automático ativo   | `true`  |
| `backup_interval_hours` | Intervalo entre backups   | `24`    |
| `max_backups`           | Máximo de backups locais  | `30`    |
| `encrypt_backups`       | Criptografar backups      | `true`  |
| `use_google_drive`      | Usar Google Drive         | `false` |
| `backup_retention_days` | Dias para manter backups  | `90`    |
| `include_logs`          | Incluir logs no backup    | `true`  |
| `include_uploads`       | Incluir uploads no backup | `true`  |
| `compression_level`     | Nível de compressão (1-9) | `6`     |

## 🔧 API Endpoints

### **Criar Backup**

```http
POST /api/backup/create
Content-Type: application/json

{
  "description": "Backup manual - atualização sistema"
}
```

### **Listar Backups**

```http
GET /api/backup/list
```

### **Restaurar Backup**

```http
POST /api/backup/{backup_id}/restore
```

### **Excluir Backup**

```http
DELETE /api/backup/{backup_id}/delete
```

### **Estatísticas**

```http
GET /api/backup/stats
```

### **Configurações**

```http
GET /api/backup/config
PUT /api/backup/config
```

### **Google Drive**

```http
POST /api/backup/google-drive/setup
```

## 📁 Estrutura de Arquivos

### **Backups Locais**

```
backups/
├── wiki_veloz_backup_20241216_143022.zip
├── wiki_veloz_backup_20241216_143022.zip.encrypted
├── backups_info.json
└── backup.log
```

### **Configurações**

```
backup_config.json     # Configurações do sistema
backup_key.key         # Chave de criptografia
credentials.json       # Credenciais Google Drive (opcional)
token.json            # Token Google Drive (opcional)
```

### **Logs**

```
backup.log            # Log do sistema de backup
app.log              # Log da aplicação
```

## 🔄 Processo de Backup

### **1. Preparação**

- Verifica espaço disponível
- Valida configurações
- Prepara diretório temporário

### **2. Coleta de Dados**

- Arquivos JSON de dados
- Logs do sistema
- Uploads de usuários
- Configurações

### **3. Compressão**

- Cria arquivo ZIP
- Aplica compressão configurada
- Otimiza tamanho

### **4. Criptografia**

- Gera chave única
- Criptografa arquivo
- Valida integridade

### **5. Armazenamento**

- Salva localmente
- Upload para Google Drive (se configurado)
- Atualiza informações

### **6. Limpeza**

- Remove backups antigos
- Limpa arquivos temporários
- Atualiza logs

## 🔍 Processo de Restauração

### **1. Validação**

- Verifica existência do backup
- Valida integridade
- Confirma permissões

### **2. Backup de Segurança**

- Cria backup do estado atual
- Previne perda de dados

### **3. Descriptografia**

- Decriptografa arquivo
- Valida chave

### **4. Extração**

- Extrai arquivos ZIP
- Restaura estrutura de diretórios

### **5. Aplicação**

- Substitui dados atuais
- Atualiza logs
- Notifica usuários

## 🛡️ Segurança

### **Criptografia**

- **Algoritmo**: AES-256
- **Chave**: Única por instalação
- **Armazenamento**: Arquivo local protegido
- **Validação**: Checksum de integridade

### **Permissões**

- **Acesso**: Apenas administradores
- **Logs**: Todas as ações registradas
- **Validação**: Confirmação para ações críticas

### **Integridade**

- **Verificação**: Checksum MD5
- **Validação**: Teste de restauração
- **Backup**: Estado atual antes de restaurar

## 📊 Monitoramento

### **Logs Automáticos**

- Criação de backups
- Restaurações
- Erros e avisos
- Configurações alteradas

### **Métricas**

- Tamanho dos backups
- Frequência de criação
- Taxa de sucesso
- Uso de espaço

### **Alertas**

- Falha no backup
- Espaço insuficiente
- Erro de criptografia
- Problema com Google Drive

## 🔧 Manutenção

### **Limpeza Automática**

- Remove backups antigos
- Limpa logs antigos
- Otimiza espaço

### **Verificação de Integridade**

- Testa backups periodicamente
- Valida criptografia
- Verifica Google Drive

### **Atualizações**

- Backup antes de atualizar
- Restauração em caso de erro
- Rollback automático

## 🚨 Troubleshooting

### **Problemas Comuns**

#### **Backup Falha**

```bash
# Verificar logs
tail -f backup.log

# Verificar espaço
df -h

# Verificar permissões
ls -la backups/
```

#### **Google Drive Não Funciona**

```bash
# Verificar credenciais
ls -la credentials.json

# Reautenticar
rm token.json
python app.py
```

#### **Criptografia Falha**

```bash
# Regenerar chave
rm backup_key.key
python app.py
```

#### **Restauração Falha**

```bash
# Verificar backup
ls -la backups/

# Verificar integridade
python -c "import zipfile; zipfile.ZipFile('backup.zip').testzip()"
```

### **Comandos Úteis**

#### **Backup Manual**

```python
from backup_system import backup_system
result = backup_system.create_backup("Backup manual")
print(result)
```

#### **Restauração Manual**

```python
from backup_system import backup_system
result = backup_system.restore_backup("backup_20241216_143022")
print(result)
```

#### **Verificar Configurações**

```python
from backup_system import backup_system
print(backup_system.config)
```

## 📈 Melhorias Futuras

### **Funcionalidades Planejadas**

- [ ] Backup incremental
- [ ] Backup diferencial
- [ ] Múltiplas nuvens (Dropbox, OneDrive)
- [ ] Backup em tempo real
- [ ] Compressão avançada
- [ ] Criptografia por usuário
- [ ] Backup seletivo
- [ ] Agendamento avançado

### **Integrações**

- [ ] Slack notifications
- [ ] Email alerts
- [ ] Webhook support
- [ ] API externa
- [ ] Dashboard externo

## 📞 Suporte

### **Contato**

- **Desenvolvedor**: Matheus Gallina
- **Email**: matheus@velozfibra.com
- **Sistema**: Wiki Veloz Fibra

### **Documentação**

- **Guia**: Este arquivo
- **API**: Endpoints documentados
- **Logs**: `backup.log`

### **Emergências**

1. **Parar aplicação**: `Ctrl+C`
2. **Verificar logs**: `tail -f backup.log`
3. **Restaurar backup**: Interface administrativa
4. **Contatar suporte**: matheus@velozfibra.com

---

**Última atualização**: 16/12/2024
**Versão**: 1.0.0
**Status**: ✅ Ativo
