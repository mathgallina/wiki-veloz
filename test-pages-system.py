#!/usr/bin/env python3
"""
Test script for Pages System
CDD v2.0 - Pages system testing
"""

import json

import requests

from app import create_app
from app.core.config import config
from app.core.database import DatabaseManager
from app.modules.pages.services.page_service import PageService


def test_pages_system():
    """Test the pages system"""
    print("🧪 TESTANDO SISTEMA DE PÁGINAS CDD v2.0")
    print("=" * 50)
    
    # Initialize services
    db_manager = DatabaseManager(config['default']())
    page_service = PageService(db_manager)
    
    # Test 1: Create sample pages
    print("\n1️⃣ Criando páginas de exemplo...")
    success = page_service.create_sample_pages()
    if success:
        print("✅ Páginas de exemplo criadas com sucesso")
    else:
        print("❌ Erro ao criar páginas de exemplo")
    
    # Test 2: Get all pages
    print("\n2️⃣ Obtendo todas as páginas...")
    pages = page_service.get_all_pages()
    print(f"✅ {len(pages)} páginas encontradas")
    
    for page in pages:
        print(f"   📄 {page.get('title', 'Sem título')} (ID: {page.get('id', 'N/A')})")
    
    # Test 3: Search pages
    print("\n3️⃣ Testando busca de páginas...")
    search_results = page_service.search_pages("bem-vindo")
    print(f"✅ {len(search_results)} resultados para 'bem-vindo'")
    
    # Test 4: Get pages by category
    print("\n4️⃣ Testando filtro por categoria...")
    geral_pages = page_service.get_pages_by_category("Geral")
    print(f"✅ {len(geral_pages)} páginas na categoria 'Geral'")
    
    # Test 5: Get recent pages
    print("\n5️⃣ Testando páginas recentes...")
    recent_pages = page_service.get_recent_pages(5)
    print(f"✅ {len(recent_pages)} páginas recentes")
    
    # Test 6: Get popular pages
    print("\n6️⃣ Testando páginas populares...")
    popular_pages = page_service.get_popular_pages(5)
    print(f"✅ {len(popular_pages)} páginas populares")
    
    # Test 7: Test page analytics
    if pages:
        print("\n7️⃣ Testando analytics de página...")
        first_page = pages[0]
        analytics = page_service.get_page_analytics(first_page['id'])
        print(f"✅ Analytics da página '{first_page.get('title', 'N/A')}':")
        print(f"   👁️ Visualizações: {analytics.get('views', 0)}")
        print(f"   📝 Versão: {analytics.get('version', 1)}")
        print(f"   🏷️ Tags: {', '.join(analytics.get('tags', []))}")
    
    # Test 8: Test page versions
    if pages:
        print("\n8️⃣ Testando sistema de versões...")
        first_page = pages[0]
        versions = page_service.get_page_versions(first_page['id'])
        print(f"✅ {len(versions)} versões encontradas para a página")
    
    print("\n🎉 TESTE DO SISTEMA DE PÁGINAS CONCLUÍDO!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_pages_system() 