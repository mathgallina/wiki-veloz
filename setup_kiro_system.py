#!/usr/bin/env python3
import os
import json
from datetime import datetime

def setup_kiro_system():
    print("🚀 Configurando sistema KIRO...")
    
    # Criar estrutura KIRO
    kiro_dirs = [
        ".kiro/steering",
        ".kiro/patterns", 
        ".kiro/scripts",
        ".kiro/specs",
        ".kiro/docs"
    ]
    
    for dir_path in kiro_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Criado diretório: {dir_path}")
    
    # Configuração KIRO
    kiro_config = {
        "project_name": "Wiki Veloz",
        "version": "2.0.0",
        "status": "active",
        "health_score": 95
    }
    
    with open(".kiro/config.json", "w", encoding="utf-8") as f:
        json.dump(kiro_config, f, indent=2, ensure_ascii=False)
    
    print("✅ Sistema KIRO configurado!")
    return True

if __name__ == "__main__":
    setup_kiro_system()
