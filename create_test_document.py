#!/usr/bin/env python3
"""
Create a test document with file attachment
"""

import os

import requests


def create_test_document():
    """Create a test document with file attachment"""
    
    session = requests.Session()
    
    # Login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    print("🔐 Logging in...")
    response = session.post("http://localhost:8000/auth/login", data=login_data)
    
    if response.status_code != 200:
        print("❌ Login failed")
        return
    
    print("✅ Login successful")
    
    # Create a simple text file for testing
    test_file_path = "test_document.txt"
    with open(test_file_path, "w") as f:
        f.write("Este é um documento de teste para verificar a visualização.\n")
        f.write("Conteúdo do documento:\n")
        f.write("- Item 1: Teste de visualização\n")
        f.write("- Item 2: Verificação de anexos\n")
        f.write("- Item 3: Teste de modal\n")
    
    print(f"📝 Created test file: {test_file_path}")
    
    # Create document with file upload
    with open(test_file_path, "rb") as f:
        files = {"file": ("test_document.txt", f, "text/plain")}
        data = {
            "title": "Documento de Teste - Visualização",
            "description": "Este é um documento de teste para verificar a funcionalidade de visualização de documentos no sistema Wiki-Veloz.",
            "category": "Técnico",
            "content": "Conteúdo do documento de teste",
            "type": "documento",
            "priority": "alta",
            "author": "admin",
            "tags": "teste,visualização,documento"
        }
        
        print("📤 Uploading document with file...")
        upload_response = session.post(
            "http://localhost:8000/documents/create",
            files=files,
            data=data
        )
    
    print(f"Upload status: {upload_response.status_code}")
    
    if upload_response.status_code == 201:
        result = upload_response.json()
        if result.get('success'):
            print("✅ Document created successfully!")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"❌ Document creation failed: {result.get('message')}")
    else:
        print(f"❌ Upload failed with status: {upload_response.status_code}")
        print(f"Response: {upload_response.text}")
    
    # Clean up test file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
        print(f"🧹 Cleaned up test file: {test_file_path}")

if __name__ == "__main__":
    create_test_document() 