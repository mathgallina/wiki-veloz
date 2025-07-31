#!/bin/bash

# Script de Instalação - Task Manager .kiro
# Configura permissões e executa primeira configuração

echo "🚀 Configurando Task Manager .kiro..."

# Verifica se está na pasta correta
if [ ! -f "task-manager.js" ]; then
    echo "❌ Execute este script dentro da pasta .kiro/scripts/"
    exit 1
fi

# Dar permissões de execução
echo "🔧 Configurando permissões..."
chmod +x task-manager.js
chmod +x generate-report.js
chmod +x install.sh

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale Node.js v14+ primeiro."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'.' -f1 | sed 's/v//')
if [ "$NODE_VERSION" -lt 14 ]; then
    echo "❌ Node.js v14+ é necessário. Versão atual: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) encontrado"

# Verificar se há specs para escanear
SPECS_DIR="../specs"
if [ ! -d "$SPECS_DIR" ]; then
    echo "⚠️  Diretório .kiro/specs não encontrado"
    echo "📝 Certifique-se de ter features criadas antes de escanear"
else
    # Contar features (excluindo _template)
    FEATURE_COUNT=$(find "$SPECS_DIR" -maxdepth 1 -type d ! -name "_template" ! -name "specs" | wc -l)
    FEATURE_COUNT=$((FEATURE_COUNT - 1)) # Remove o próprio diretório specs da contagem
    
    if [ "$FEATURE_COUNT" -gt 0 ]; then
        echo "📁 $FEATURE_COUNT feature(s) encontrada(s)"
        
        # Perguntar se quer escanear agora
        echo ""
        read -p "🔍 Deseja escanear as tarefas agora? (y/n): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🔍 Escaneando tarefas..."
            node task-manager.js scan
            
                    echo ""
        echo "📊 Status atual:"
        node task-manager.js status
        
        echo ""
        echo "📐 Status dos padrões:"
        node task-manager.js patterns
    fi
else
    echo "📝 Nenhuma feature encontrada em .kiro/specs/"
    echo "💡 Crie algumas features primeiro e depois execute: npm run scan"
fi
fi

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📖 Comandos disponíveis:"
echo "  npm run scan     - Escanear todas as tarefas"
echo "  npm run status   - Ver status geral"
echo "  npm run list     - Listar tarefas"
echo "  npm run patterns - Ver status dos padrões de código"
echo "  npm run check-patterns - Validar conformidade com padrões"
echo "  npm run watch    - Monitorar mudanças automaticamente"
echo "  npm run report   - Gerar relatório"
echo "  npm run help     - Ajuda completa"
echo ""
echo "📄 Documentação completa: README.md" 