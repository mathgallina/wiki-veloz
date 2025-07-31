#!/usr/bin/env python3

import requests
from werkzeug.security import generate_password_hash, check_password_hash

# Dados do usuário
username = "matheus.gallina"
password = "B@rcelona1998"

print("🔍 Testando sistema de login...")
print(f"Usuário: {username}")
print(f"Senha: {password}")

# Gerar novo hash para teste
new_hash = generate_password_hash(password)
print(f"Novo hash da senha: {new_hash}")

# Testar verificação de senha
is_valid = check_password_hash(new_hash, password)
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
