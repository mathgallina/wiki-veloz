# Sistema de Gerenciamento de Usuários - Wiki Veloz Fibra

## Visão Geral

O sistema de gerenciamento de usuários permite que administradores criem, editem e gerenciem usuários da wiki de forma segura e intuitiva.

## Acesso ao Sistema

### Como Acessar

1. Faça login na wiki como administrador
2. Clique no ícone de engrenagem (⚙️) no canto superior direito
3. Selecione "Gerenciar Usuários" no menu dropdown

### Permissões

- **Apenas administradores** podem acessar o sistema de gerenciamento
- Usuários comuns não veem o menu de administração

## Funcionalidades

### 1. Visualizar Usuários

- Lista completa de todos os usuários do sistema
- Informações exibidas:
  - Nome completo
  - Nome de usuário
  - Email
  - Função (Administrador/Usuário)
  - Status (Ativo/Inativo)
  - Último login

### 2. Criar Novo Usuário

1. Clique no botão "Adicionar Usuário"
2. Preencha os campos obrigatórios:
   - **Nome Completo**: Nome real do colaborador
   - **Nome de Usuário**: Login único (ex: joao.silva)
   - **Email**: Email corporativo
   - **Senha**: Senha inicial (o usuário pode alterar depois)
   - **Função**: Usuário ou Administrador
   - **Status**: Ativo ou Inativo

### 3. Editar Usuário

1. Clique no ícone de editar (✏️) ao lado do usuário
2. Modifique os campos desejados
3. Para alterar a senha, preencha o campo "Senha" (deixe em branco para manter a atual)
4. Clique em "Atualizar"

### 4. Deletar Usuário

1. Clique no ícone de lixeira (🗑️) ao lado do usuário
2. Confirme a ação
3. **Observações importantes**:
   - Não é possível deletar o próprio usuário
   - Não é possível deletar o último administrador
   - O usuário admin padrão (Matheus Gallina) não pode ser deletado

## Tipos de Usuário

### Administrador

- Acesso completo à wiki
- Pode criar, editar e deletar páginas
- Pode gerenciar outros usuários
- Pode visualizar logs de atividade
- Pode acessar todas as funcionalidades

### Usuário

- Pode visualizar e editar páginas da wiki
- Não pode gerenciar usuários
- Não pode acessar logs de atividade
- Acesso limitado às funcionalidades básicas

## Segurança

### Validações Implementadas

- **Usuários únicos**: Não é possível criar dois usuários com o mesmo nome de usuário
- **Emails únicos**: Não é possível usar o mesmo email em múltiplos usuários
- **Senhas criptografadas**: Todas as senhas são armazenadas de forma segura
- **Proteção de administradores**: Não é possível deletar o último administrador
- **Logs de atividade**: Todas as ações são registradas para auditoria

### Boas Práticas

1. **Senhas fortes**: Use senhas com pelo menos 8 caracteres, incluindo letras, números e símbolos
2. **Usuários inativos**: Desative usuários que não estão mais ativos na empresa
3. **Revisão regular**: Verifique periodicamente a lista de usuários
4. **Logs**: Monitore os logs de atividade para detectar atividades suspeitas

## Logs de Atividade

Todas as ações de gerenciamento de usuários são registradas:

- Criação de usuários
- Edição de usuários
- Exclusão de usuários
- Tentativas de login
- Logouts

Para visualizar os logs:

1. Clique no ícone de engrenagem (⚙️)
2. Selecione "Logs de Atividade"

## Exemplos de Uso

### Adicionando um Novo Colaborador

```
Nome: João Silva
Usuário: joao.silva
Email: joao.silva@velozfibra.com
Senha: Veloz2024!
Função: Usuário
Status: Ativo
```

### Adicionando um Administrador

```
Nome: Maria Santos
Usuário: maria.santos
Email: maria.santos@velozfibra.com
Senha: Admin2024!
Função: Administrador
Status: Ativo
```

### Desativando um Usuário

1. Clique em editar o usuário
2. Desmarque a opção "Usuário ativo"
3. Clique em "Atualizar"

## Suporte

Em caso de problemas:

1. Verifique se você está logado como administrador
2. Confirme se o usuário não está sendo usado em outro lugar
3. Verifique os logs de atividade para identificar possíveis erros
4. Entre em contato com o administrador principal (Matheus Gallina)

---

**Última atualização**: 16/07/2025
**Versão**: 1.0
