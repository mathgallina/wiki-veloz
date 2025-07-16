#!/usr/bin/env python3
"""
Script simples para configurar Google Drive sem autorização interativa
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def setup_google_drive_simple():
    """Configura Google Drive usando credenciais de serviço"""

    print("🔧 Configurando Google Drive (modo simples)...")

    # Criar credenciais de serviço básicas
    service_account_info = {
        "type": "service_account",
        "project_id": "bkp-opa-velozfibra",
        "private_key_id": "simple_key",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
        "client_email": "wiki-veloz@bkp-opa-velozfibra.iam.gserviceaccount.com",
        "client_id": "635432419724-vte2et3gs849ao3o813is6vsdjgddqag.apps.googleusercontent.com",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/wiki-veloz%40bkp-opa-velozfibra.iam.gserviceaccount.com"
    }

    # Salvar credenciais de serviço
    with open('service-account.json', 'w') as f:
        json.dump(service_account_info, f, indent=2)

    print("✅ Credenciais de serviço criadas")

    try:
        # Criar credenciais
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )

        # Construir serviço
        service = build('drive', 'v3', credentials=credentials)
        print("✅ Serviço Google Drive construído")

        # Testar conexão
        results = service.files().list(pageSize=1).execute()
        print("✅ Conexão com Google Drive estabelecida")

        return True

    except HttpError as error:
        print(f"❌ Erro na API: {error}")
        return False
    except Exception as error:
        print(f"❌ Erro: {error}")
        return False

if __name__ == '__main__':
    success = setup_google_drive_simple()
    if success:
        print("\n🎉 Google Drive configurado com sucesso!")
    else:
        print("\n❌ Falha na configuração")
