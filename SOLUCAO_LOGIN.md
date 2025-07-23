# 🔐 Guia de Solução de Problemas - Login Wiki Veloz

## ✅ Status Atual: SISTEMA FUNCIONANDO

O sistema de login da Wiki Veloz está **funcionando corretamente**. As credenciais padrão são:

- **Usuário**: `admin`
- **Senha**: `B@rcelona1998`

## 🌐 Como Acessar

1. **Abra seu navegador**
2. **Acesse**: `http://localhost:8000`
3. **Use as credenciais acima**
4. **Clique em "Entrar"**

## 🔧 Se Você Está Tendo Problemas

### 1. Verificar se o Servidor Está Rodando

```bash
# No terminal, execute:
python3 app.py
```

Você deve ver:

```
 * Running on http://0.0.0.0:8000
 * Debug mode: on
```

### 2. Testar o Sistema de Login

Execute o script de teste:

```bash
python3 test_login.py
```

### 3. Testar Login via HTTP

Execute o script de teste HTTP:

```bash
python3 test_http_login.py
```

## 🚨 Problemas Comuns e Soluções

### Problema: "Usuário ou senha incorretos"

**Solução:**

1. Verifique se está digitando exatamente:

   - Usuário: `admin` (minúsculo)
   - Senha: `B@rcelona1998` (com @ e maiúsculas)

2. Se ainda não funcionar, execute:

```bash
python3 test_login.py
```

### Problema: "Página não carrega"

**Solução:**

1. Verifique se o servidor está rodando:

```bash
curl http://localhost:8000
```

2. Se não estiver rodando, inicie:

```bash
python3 app.py
```

### Problema: "Erro de conexão"

**Solução:**

1. Verifique se a porta 8000 está livre:

```bash
lsof -i :8000
```

2. Se estiver ocupada, mate o processo:

```bash
pkill -f "python3 app.py"
```

3. Reinicie o servidor:

```bash
python3 app.py
```

## 📋 Checklist de Verificação

- [ ] Servidor Flask está rodando
- [ ] Arquivo `data/users.json` existe
- [ ] Usuário admin está criado
- [ ] Credenciais estão corretas
- [ ] Navegador consegue acessar `http://localhost:8000`

## 🔍 Diagnóstico Automático

Execute este comando para verificar tudo:

```bash
python3 test_login.py && python3 test_http_login.py
```

## 📞 Suporte

Se ainda estiver com problemas:

1. **Verifique os logs do servidor** - procure por erros no terminal onde `app.py` está rodando

2. **Teste em navegador diferente** - às vezes cache pode causar problemas

3. **Limpe cache do navegador** - Ctrl+F5 (Windows) ou Cmd+Shift+R (Mac)

4. **Verifique firewall** - certifique-se que a porta 8000 não está bloqueada

## 🎯 Credenciais de Teste

Para facilitar, aqui estão as credenciais novamente:

```
Usuário: admin
Senha: B@rcelona1998
```

## 🔄 Reset do Sistema (Se Necessário)

Se tudo falhar, você pode resetar o sistema:

1. **Pare o servidor**: Ctrl+C no terminal
2. **Delete o arquivo de usuários**: `rm data/users.json`
3. **Reinicie o servidor**: `python3 app.py`
4. **O usuário admin será recriado automaticamente**

## ✅ Confirmação de Funcionamento

O sistema foi testado e está funcionando. Se você ainda não consegue acessar, verifique:

1. **URL correta**: `http://localhost:8000` (não `https`)
2. **Servidor rodando**: Terminal deve mostrar "Running on http://0.0.0.0:8000"
3. **Credenciais exatas**: `admin` e `B@rcelona1998`

---

**Última atualização**: 23/07/2025  
**Status**: ✅ Funcionando  
**Testado por**: Sistema automatizado
