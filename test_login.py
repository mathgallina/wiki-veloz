#!/usr/bin/env python3

import requests
from werkzeug.security import check_password_hash

# Dados do usuário
username = "matheus.gallina"
password = "Veloz2024!"
password_hash = "pbkdf2:sha256:600000$2kqDbe4zWU5vTEsR$0d3c5f0ce8995da5138a2793b8ca05ef5d03a0d92a64c1e7f5ff4681e889ba02"

print("🔍 Testando sistema de login...")
print(f"Usuário: {username}")
print(f"Senha: {password}")
print(f"Hash da senha: {password_hash}")

# Testar verificação de senha
is_valid = check_password_hash(password_hash, password)
print(f"✅ Senha válida: {is_valid}")

# Testar login via HTTP
session = requests.Session()
login_data = {
    'username': username,
    'password': password
}

try:
    response = session.post('http://127.0.0.1:8000/login', data=login_data)
    print(f"📡 Status da resposta: {response.status_code}")
    print(f"📄 URL final: {response.url}")

    if response.status_code == 200:
        print("✅ Login realizado com sucesso!")
    else:
        print("❌ Erro no login")
        print(f"Conteúdo da resposta: {response.text[:200]}...")

except Exception as e:
    print(f"❌ Erro na requisição: {e}")
