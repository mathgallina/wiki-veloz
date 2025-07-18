#!/bin/bash

# new-feature.sh - Script para criar nova funcionalidade baseada no template
# Uso: ./new-feature.sh <nome-da-feature>

set -e  # Exit on any error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar se nome da feature foi fornecido
if [ -z "$1" ]; then
    print_error "Nome da feature é obrigatório!"
    echo "Uso: $0 <nome-da-feature>"
    echo ""
    echo "Exemplos:"
    echo "  $0 user-authentication"
    echo "  $0 payment-gateway"
    echo "  $0 notification-system"
    exit 1
fi

FEATURE_NAME="$1"

# Validar nome da feature (apenas letras, números e hífens)
if [[ ! "$FEATURE_NAME" =~ ^[a-z0-9-]+$ ]]; then
    print_error "Nome da feature deve conter apenas letras minúsculas, números e hífens"
    echo "Exemplo válido: user-authentication"
    exit 1
fi

# Verificar se estamos no diretório raiz do projeto
if [ ! -d ".kiro" ]; then
    print_error "Este script deve ser executado no diretório raiz do projeto (onde existe .kiro/)"
    exit 1
fi

# Verificar se template existe
if [ ! -d ".kiro/specs/_template" ]; then
    print_error "Template não encontrado em .kiro/specs/_template/"
    print_info "Execute primeiro: mkdir -p .kiro/specs/_template"
    exit 1
fi

# Verificar se feature já existe
if [ -d ".kiro/specs/$FEATURE_NAME" ]; then
    print_error "Feature '$FEATURE_NAME' já existe!"
    echo "Arquivos existentes em .kiro/specs/$FEATURE_NAME:"
    ls -la ".kiro/specs/$FEATURE_NAME"
    exit 1
fi

print_info "Criando nova feature: $FEATURE_NAME"

# Criar diretório da nova feature
mkdir -p ".kiro/specs/$FEATURE_NAME"
print_success "Diretório .kiro/specs/$FEATURE_NAME criado"

# Copiar arquivos do template
if [ -f ".kiro/specs/_template/requirements.md" ]; then
    cp ".kiro/specs/_template/requirements.md" ".kiro/specs/$FEATURE_NAME/"
    print_success "requirements.md copiado do template"
fi

if [ -f ".kiro/specs/_template/design.md" ]; then
    cp ".kiro/specs/_template/design.md" ".kiro/specs/$FEATURE_NAME/"
    print_success "design.md copiado do template"
fi

if [ -f ".kiro/specs/_template/tasks.md" ]; then
    cp ".kiro/specs/_template/tasks.md" ".kiro/specs/$FEATURE_NAME/"
    print_success "tasks.md copiado do template"
fi

# Converter nome da feature para diferentes formatos
FEATURE_TITLE=$(echo "$FEATURE_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++){ $i=toupper(substr($i,1,1)) substr($i,2) }}1')
FEATURE_CAMEL=$(echo "$FEATURE_NAME" | sed -r 's/(^|-)([a-z])/\U\2/g')
FEATURE_SNAKE=$(echo "$FEATURE_NAME" | sed 's/-/_/g')

print_info "Formatos detectados:"
echo "  - Kebab case: $FEATURE_NAME"
echo "  - Title case: $FEATURE_TITLE"
echo "  - CamelCase: $FEATURE_CAMEL"
echo "  - snake_case: $FEATURE_SNAKE"

# Substituir placeholders nos arquivos
for file in ".kiro/specs/$FEATURE_NAME"/*.md; do
    if [ -f "$file" ]; then
        # Substituições básicas
        sed -i.bak "s/\[Nome da Funcionalidade\]/$FEATURE_TITLE/g" "$file"
        sed -i.bak "s/\[nome-da-funcionalidade\]/$FEATURE_NAME/g" "$file"
        sed -i.bak "s/\[nomeDaFuncionalidade\]/$FEATURE_CAMEL/g" "$file"
        sed -i.bak "s/\[nome_da_funcionalidade\]/$FEATURE_SNAKE/g" "$file"
        
        # Adicionar data atual
        current_date=$(date "+%Y-%m-%d")
        sed -i.bak "s/\[Data de Criação\]/$current_date/g" "$file"
        sed -i.bak "s/\[data-criacao\]/$current_date/g" "$file"
        
        # Adicionar autor se disponível no git
        if git config user.name > /dev/null 2>&1; then
            author=$(git config user.name)
            sed -i.bak "s/\[Autor\]/$author/g" "$file"
            sed -i.bak "s/\[autor\]/$author/g" "$file"
        fi
        
        # Remover arquivos de backup
        rm -f "$file.bak"
        
        print_success "Placeholders substituídos em $(basename "$file")"
    fi
done

# Inicializar tracking se scripts estão disponíveis
if [ -f ".kiro/scripts/task-manager.js" ]; then
    print_info "Inicializando tracking de tarefas..."
    cd ".kiro/scripts"
    
    # Executar scan para detectar novas tarefas
    if npm run scan > /dev/null 2>&1; then
        print_success "Tracking inicializado"
    else
        print_warning "Falha ao inicializar tracking (mas feature foi criada com sucesso)"
    fi
    
    cd - > /dev/null
fi

# Mostrar resumo
echo ""
print_success "Feature '$FEATURE_NAME' criada com sucesso!"
echo ""
echo "📁 Arquivos criados em .kiro/specs/$FEATURE_NAME/:"
ls -la ".kiro/specs/$FEATURE_NAME/"

echo ""
print_info "Próximos passos:"
echo "1. Edite os arquivos em .kiro/specs/$FEATURE_NAME/"
echo "2. Customize requirements.md com os requisitos específicos"
echo "3. Detalhe design.md com a arquitetura técnica"
echo "4. Planeje tasks.md com as tarefas de implementação"
echo "5. Execute 'npm run status' para ver o progresso"

echo ""
print_warning "⚠️  Lembre-se de personalizar os templates!"
print_info "Os placeholders foram substituídos automaticamente, mas você ainda precisa:"
echo "  - Definir requisitos funcionais específicos"
echo "  - Detalhar a arquitetura técnica"
echo "  - Quebrar em tarefas menores"
echo "  - Estimar tempo e complexidade"

# Verificar se patterns existem para referência
if [ -d ".kiro/patterns" ]; then
    echo ""
    print_info "📐 Consulte os padrões de código em .kiro/patterns/ durante a implementação"
fi

print_success "🎉 Feature '$FEATURE_NAME' está pronta para ser desenvolvida!" 