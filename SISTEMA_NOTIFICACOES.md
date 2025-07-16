# 🔔 Sistema de Notificações - Wiki Veloz Fibra

## 📋 Visão Geral

O sistema de notificações da Wiki Veloz Fibra permite que administradores criem e gerenciem notificações para todos os usuários da plataforma. As notificações aparecem no header da interface e podem ser marcadas como lidas, deletadas ou ter ações associadas.

## 🚀 Funcionalidades

### ✅ **Para Usuários**

- **Visualização**: Notificações aparecem no ícone de sino no header
- **Contador**: Badge vermelho mostra número de notificações não lidas
- **Marcar como lida**: Clique na notificação para marcá-la como lida
- **Marcar todas como lidas**: Botão para marcar todas de uma vez
- **Deletar**: Botão para remover notificações individuais
- **Ações**: Links para páginas ou ações específicas

### ✅ **Para Administradores**

- **Criar notificações**: Formulário completo para criar novas notificações
- **Selecionar destinatário**: Escolher usuário específico
- **Tipos de notificação**: Info, Sucesso, Aviso, Erro
- **Prioridades**: Baixa, Normal, Alta, Urgente
- **Data de expiração**: Definir quando a notificação deve expirar
- **Ações**: URLs e textos de botão para ações
- **Gerenciar**: Ver todas as notificações e deletar

## 🎯 Tipos de Notificação

### 📘 **Info** (Azul)

- Informações gerais
- Atualizações de sistema
- Anúncios não críticos

### ✅ **Success** (Verde)

- Confirmações de ações
- Tarefas concluídas
- Mensagens positivas

### ⚠️ **Warning** (Amarelo)

- Avisos importantes
- Lembretes
- Atenções necessárias

### ❌ **Error** (Vermelho)

- Erros críticos
- Problemas urgentes
- Falhas de sistema

## 🏷️ Prioridades

### 🔵 **Baixa**

- Informações não urgentes
- Lembretes opcionais

### 🔵 **Normal**

- Notificações padrão
- Informações importantes

### 🟡 **Alta**

- Avisos importantes
- Requer atenção

### 🔴 **Urgente**

- Crítico
- Requer ação imediata

## 📊 Estrutura de Dados

```json
{
  "id": "notif-20250116142023-admin-001",
  "user_id": "admin-001",
  "title": "Bem-vindo à Wiki Veloz Fibra!",
  "message": "Olá Matheus Gallina! Bem-vindo à nossa central de conhecimento.",
  "type": "success",
  "priority": "normal",
  "is_read": false,
  "created_at": "2025-01-16T14:20:23",
  "expires_at": null,
  "action_url": "/onboarding",
  "action_text": "Ver onboarding"
}
```

## 🔧 API Endpoints

### 📥 **Obter Notificações**

```
GET /api/notifications?include_read=false&limit=50
```

### ✅ **Marcar como Lida**

```
POST /api/notifications/{id}/read
```

### ✅ **Marcar Todas como Lidas**

```
POST /api/notifications/read-all
```

### 🗑️ **Deletar Notificação**

```
DELETE /api/notifications/{id}
```

### 📊 **Contador de Não Lidas**

```
GET /api/notifications/unread-count
```

### ➕ **Criar Notificação** (Admin)

```
POST /api/notifications
{
  "user_id": "user-id",
  "title": "Título",
  "message": "Mensagem",
  "type": "info",
  "priority": "normal",
  "expires_at": "2025-01-17T00:00:00",
  "action_url": "/url",
  "action_text": "Ver mais"
}
```

## 🎨 Interface

### 📱 **Header**

- Ícone de sino com badge de contagem
- Dropdown com lista de notificações
- Botões para marcar como lida/deletar

### ⚙️ **Painel Admin**

- Formulário completo para criar notificações
- Tabela com todas as notificações
- Filtros por usuário, tipo, prioridade

## 🔄 Notificações Automáticas

### 👋 **Boas-vindas**

- Criada automaticamente para novos usuários
- Aparece nas primeiras 24h após criação da conta

### 📅 **Agendadas**

- Sistema suporta notificações com data de expiração
- Notificações expiradas não aparecem na lista

## 🛠️ Como Usar

### 👤 **Para Usuários Comuns**

1. **Ver notificações**: Clique no ícone de sino no header
2. **Marcar como lida**: Clique na notificação
3. **Marcar todas**: Use o botão "Marcar todas como lidas"
4. **Deletar**: Clique no ícone de lixeira
5. **Ação**: Clique no link de ação se disponível

### 👨‍💼 **Para Administradores**

1. **Acessar painel**: Vá em "Administração" > "Gerenciar Notificações"
2. **Criar notificação**: Preencha o formulário
3. **Selecionar usuário**: Escolha o destinatário
4. **Definir tipo/prioridade**: Configure conforme necessário
5. **Adicionar ação**: URL e texto do botão (opcional)
6. **Salvar**: Clique em "Criar Notificação"

## 📝 Exemplos de Uso

### 🎉 **Notificação de Boas-vindas**

```json
{
  "title": "Bem-vindo à Wiki Veloz Fibra!",
  "message": "Olá [Nome]! Explore nossa central de conhecimento.",
  "type": "success",
  "priority": "normal",
  "action_url": "/onboarding",
  "action_text": "Ver onboarding"
}
```

### ⚠️ **Aviso de Manutenção**

```json
{
  "title": "Manutenção Programada",
  "message": "Sistema ficará indisponível das 02h às 04h.",
  "type": "warning",
  "priority": "high",
  "expires_at": "2025-01-17T04:00:00"
}
```

### 🚨 **Alerta Crítico**

```json
{
  "title": "Problema na Rede",
  "message": "Detectamos instabilidade na rede. Técnicos acionados.",
  "type": "error",
  "priority": "urgent",
  "action_url": "/status-rede",
  "action_text": "Ver status"
}
```

## 🔒 Segurança

- **Apenas admins** podem criar notificações
- **Validação** de dados de entrada
- **Sanitização** de conteúdo
- **Controle de acesso** por usuário

## 🚀 Próximas Melhorias

- [ ] **Notificações em tempo real** (WebSocket)
- [ ] **Notificações por email**
- [ ] **Templates de notificação**
- [ ] **Notificações em massa**
- [ ] **Agendamento de notificações**
- [ ] **Histórico de notificações**
- [ ] **Preferências de notificação**

## 📞 Suporte

Para dúvidas sobre o sistema de notificações:

1. Consulte esta documentação
2. Verifique os logs do sistema
3. Entre em contato com o administrador

---

**Última atualização**: 16/01/2025
**Versão**: 1.0.0
