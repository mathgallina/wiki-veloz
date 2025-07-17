#!/usr/bin/env python3
"""
Script de teste para Google Drive com porta fixa
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopo necessário para Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def test_google_drive_fixed():
    """Testa a configuração do Google Drive com porta fixa"""

    print("🔍 Testando configuração do Google Drive (porta fixa)...")

    # Verificar se o arquivo de credenciais existe
    if not os.path.exists('credentials.json'):
        print("❌ Arquivo credentials.json não encontrado!")
        return False

    print("✅ Arquivo credentials.json encontrado")

    creds = None

    # Verificar se já temos um token válido
    if os.path.exists('token.json'):
        print("✅ Token encontrado, verificando validade...")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se não há credenciais válidas, fazer o fluxo de autorização
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token...")
            creds.refresh(Request())
        else:
            print("🔐 Iniciando fluxo de autorização (porta 8080)...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Usar porta fixa 8080
            creds = flow.run_local_server(port=8080)

        # Salvar as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("✅ Token salvo com sucesso")

    try:
        # Construir o serviço do Google Drive
        service = build('drive', 'v3', credentials=creds)
        print("✅ Serviço Google Drive construído com sucesso")

        # Testar listagem de arquivos
        results = service.files().list(pageSize=10).execute()
        files = results.get('files', [])

        print(f"✅ Conexão com Google Drive estabelecida!")
        print(f"📁 Encontrados {len(files)} arquivos na raiz")

        # Criar pasta de teste
        folder_metadata = {
            'name': 'Wiki-Veloz-Backups-Teste',
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f"✅ Pasta de teste criada com ID: {folder_id}")

        # Limpar pasta de teste
        service.files().delete(fileId=folder_id).execute()
        print("✅ Pasta de teste removida")

        return True

    except HttpError as error:
        print(f"❌ Erro na API do Google Drive: {error}")
        return False
    except Exception as error:
        print(f"❌ Erro inesperado: {error}")
        return False

if __name__ == '__main__':
    success = test_google_drive_fixed()
    if success:
        print("\n🎉 Google Drive configurado com sucesso!")
    else:
        print("\n❌ Falha na configuração do Google Drive")
