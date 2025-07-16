# 🚀 Guia Rápido - Sistema de Backup Wiki Veloz Fibra

## ⚡ Início Rápido

### 1. **Acessar Sistema**

- URL: `http://localhost:8000`
- Login: `matheus.gallina` / `B@rcelona1998`
- Navegar para: **Administração > Backup**

### 2. **Criar Primeiro Backup**

1. Clique em **"Criar Backup"**
2. Digite uma descrição (opcional)
3. Aguarde a confirmação
4. ✅ Backup criado com sucesso!

### 3. **Verificar Backups**

- Dashboard mostra estatísticas
- Lista todos os backups disponíveis
- Status: criptografado, Google Drive, tamanho

## 🔧 Configurações Básicas

### **Backup Automático**

- ✅ **Ativo por padrão**
- ⏰ **Intervalo**: 24 horas
- 📦 **Máximo**: 30 backups
- 🗑️ **Retenção**: 90 dias

### **Segurança**

- 🔐 **Criptografia**: AES-256 ativa
- 🔑 **Chave**: Gerada automaticamente
- 📁 **Localização**: `backup_key.key`

## 📊 Interface Administrativa

### **Dashboard**

```
┌─────────────────────────────────────────────────────────┐
│ 📊 Estatísticas                                        │
├─────────────────────────────────────────────────────────┤
│ 📦 Total: 2 backups    🔐 Criptografados: 2           │
│ ☁️ Google Drive: 0     💾 Tamanho: 9.5 KB            │
└─────────────────────────────────────────────────────────┘
```

### **Ações Disponíveis**

- ➕ **Criar Backup**: Manual com descrição
- 🔄 **Restaurar**: Volta para estado anterior
- 📥 **Baixar**: Download do arquivo
- 🗑️ **Excluir**: Remove backup
- ⚙️ **Configurar**: Ajusta parâmetros

## 🔄 Operações Principais

### **Criar Backup Manual**

```bash
# Via API
curl -X POST http://localhost:8000/api/backup/create \
  -H "Content-Type: application/json" \
  -d '{"description": "Backup antes da atualização"}'
```

### **Listar Backups**

```bash
# Via API
curl http://localhost:8000/api/backup/list
```

### **Restaurar Backup**

```bash
# Via API
curl -X POST http://localhost:8000/api/backup/backup_20250716_151152/restore
```

## 📁 Estrutura de Arquivos

### **Backups Criados**

```
backups/
├── wiki_veloz_backup_20250716_151152.zip.encrypted  # Backup criptografado
├── wiki_veloz_backup_20250716_150843.zip           # Backup anterior
├── backups_info.json                               # Informações dos backups
└── backup.log                                     # Log do sistema
```

### **Configurações**

```
backup_config.json    # Configurações do sistema
backup_key.key        # Chave de criptografia
```

## 🔐 Segurança

### **Criptografia Automática**

- ✅ Todos os backups são criptografados
- 🔑 Chave única por instalação
- 🛡️ Proteção contra acesso não autorizado

### **Validação de Integridade**

- ✅ Checksum MD5 em cada backup
- 🔍 Verificação automática
- ⚠️ Alertas em caso de corrupção

## ☁️ Google Drive (Opcional)

### **Configurar Google Drive**

1. Baixar `credentials.json` do Google Cloud Console
2. Colocar na raiz do projeto
3. Clicar em **"Configurar Google Drive"**
4. Autorizar acesso
5. ✅ Backups enviados automaticamente

### **Benefícios**

- 📱 Acesso de qualquer lugar
- 💾 2TB de espaço disponível
- 🔄 Sincronização automática
- 🛡️ Backup adicional na nuvem

## 🚨 Emergências

### **Sistema Não Inicia**

```bash
# Verificar logs
tail -f backup.log

# Verificar permissões
ls -la backups/

# Reiniciar sistema
python app.py
```

### **Backup Corrompido**

```bash
# Verificar integridade
python -c "import zipfile; zipfile.ZipFile('backup.zip').testzip()"

# Restaurar backup anterior
# Via interface administrativa
```

### **Perda de Chave**

```bash
# Regenerar chave (perde backups antigos)
rm backup_key.key
python app.py
```

## 📈 Monitoramento

### **Logs Automáticos**

- 📝 Todas as operações registradas
- ⏰ Timestamp em cada ação
- 🔍 Detalhes de erros e sucessos

### **Métricas Disponíveis**

- 📊 Total de backups
- 💾 Tamanho total
- 🔐 Backups criptografados
- ☁️ Backups na nuvem

## ⚡ Comandos Úteis

### **Backup Manual via Python**

```python
from backup_system import backup_system
result = backup_system.create_backup("Backup manual")
print(f"Backup criado: {result['name']}")
```

### **Verificar Configurações**

```python
from backup_system import backup_system
print(backup_system.config)
```

### **Listar Backups**

```python
from backup_system import backup_system
backups = backup_system.get_backups_list()
for backup in backups:
    print(f"{backup['name']} - {backup['size']} bytes")
```

## 🎯 Próximos Passos

### **Configurações Recomendadas**

1. **Ajustar intervalo**: 12 horas para dados críticos
2. **Aumentar retenção**: 180 dias para histórico
3. **Configurar Google Drive**: Backup na nuvem
4. **Monitorar logs**: Verificar regularmente

### **Melhorias Planejadas**

- 📱 Notificações por email
- 🔄 Backup incremental
- 📊 Dashboard avançado
- 🔗 Integração com Slack

## 📞 Suporte

### **Contato**

- **Desenvolvedor**: Matheus Gallina
- **Email**: matheus@velozfibra.com
- **Sistema**: Wiki Veloz Fibra

### **Documentação Completa**

- 📖 `SISTEMA_BACKUP.md`: Documentação técnica
- 🔧 `backup_system.py`: Código fonte
- 📊 Interface web: `/admin/backup`

---

**✅ Sistema Ativo e Funcionando**
**🔄 Backup Automático Configurado**
**🔐 Criptografia Ativa**
**📊 Monitoramento Ativo**

**Última atualização**: 16/12/2024
