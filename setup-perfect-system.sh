#!/bin/bash

# Wiki Veloz - Sistema Perfeito CDD v2.0
# Script de configuração e inicialização

set -e

echo "🚀 INICIANDO SISTEMA PERFEITO CDD v2.0"
echo "========================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Python está instalado
check_python() {
    log_info "Verificando Python..."
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        log_success "Python3 encontrado"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        log_success "Python encontrado"
    else
        log_error "Python não encontrado. Instale Python 3.8+"
        exit 1
    fi
}

# Verificar se pip está instalado
check_pip() {
    log_info "Verificando pip..."
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
        log_success "pip3 encontrado"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
        log_success "pip encontrado"
    else
        log_error "pip não encontrado. Instale pip"
        exit 1
    fi
}

# Criar ambiente virtual
setup_venv() {
    log_info "Configurando ambiente virtual..."
    if [ ! -d ".venv" ]; then
        $PYTHON_CMD -m venv .venv
        log_success "Ambiente virtual criado"
    else
        log_info "Ambiente virtual já existe"
    fi
    
    # Ativar ambiente virtual
    source .venv/bin/activate
    log_success "Ambiente virtual ativado"
}

# Instalar dependências
install_dependencies() {
    log_info "Instalando dependências..."
    $PIP_CMD install --upgrade pip
    $PIP_CMD install -r requirements.txt
    
    if [ -f "requirements-dev.txt" ]; then
        log_info "Instalando dependências de desenvolvimento..."
        $PIP_CMD install -r requirements-dev.txt
    fi
    
    log_success "Dependências instaladas"
}

# Configurar estrutura de dados
setup_data_structure() {
    log_info "Configurando estrutura de dados..."
    
    # Criar diretórios necessários
    mkdir -p app/data
    mkdir -p app/static/uploads
    mkdir -p backups
    mkdir -p logs
    
    # Copiar dados existentes se houver
    if [ -d "data" ] && [ ! -d "app/data" ]; then
        log_info "Migrando dados existentes..."
        cp -r data/* app/data/ 2>/dev/null || true
    fi
    
    log_success "Estrutura de dados configurada"
}

# Verificar configuração CDD
check_cdd_structure() {
    log_info "Verificando estrutura CDD v2.0..."
    
    if [ ! -d ".kiro" ]; then
        log_warning "Estrutura CDD não encontrada. Criando..."
        mkdir -p .kiro/{steering,patterns,scripts,specs,docs,backups}
        
        # Criar arquivo de configuração CDD
        cat > .kiro/config.json << EOF
{
    "project_name": "Wiki Veloz",
    "version": "2.0.0",
    "methodology": "CDD v2.0",
    "status": "active"
}
EOF
        log_success "Estrutura CDD criada"
    else
        log_success "Estrutura CDD encontrada"
    fi
}

# Executar testes básicos
run_basic_tests() {
    log_info "Executando testes básicos..."
    
    # Testar importação da aplicação
    if $PYTHON_CMD -c "from app import create_app; app = create_app(); print('✅ Aplicação criada com sucesso')" 2>/dev/null; then
        log_success "Teste de importação passou"
    else
        log_error "Teste de importação falhou"
        return 1
    fi
    
    # Testar configuração
    if $PYTHON_CMD -c "from app.core.config import config; print('✅ Configuração carregada')" 2>/dev/null; then
        log_success "Teste de configuração passou"
    else
        log_error "Teste de configuração falhou"
        return 1
    fi
    
    log_success "Todos os testes básicos passaram"
}

# Configurar variáveis de ambiente
setup_environment() {
    log_info "Configurando variáveis de ambiente..."
    
    # Criar arquivo .env se não existir
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Wiki Veloz - Environment Variables
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=veloz-fibra-secret-key-2024
PORT=8000

# Google Drive (opcional)
GOOGLE_DRIVE_CREDENTIALS_FILE=
GOOGLE_DRIVE_FOLDER_ID=

# Backup Configuration
BACKUP_RETENTION_DAYS=30
EOF
        log_success "Arquivo .env criado"
    else
        log_info "Arquivo .env já existe"
    fi
}

# Mostrar informações do sistema
show_system_info() {
    echo ""
    echo "🎯 SISTEMA PERFEITO CDD v2.0 - CONFIGURADO"
    echo "=========================================="
    echo ""
    echo "📁 Estrutura do Projeto:"
    echo "   ├── app/                    # Aplicação modular"
    echo "   ├── .kiro/                  # Estrutura CDD v2.0"
    echo "   ├── data/                   # Dados (migrados para app/data/)"
    echo "   ├── backups/                # Backups automáticos"
    echo "   └── logs/                   # Logs do sistema"
    echo ""
    echo "🔧 Comandos Disponíveis:"
    echo "   python3 app.py              # Executar aplicação"
    echo "   python3 -m pytest tests/    # Executar testes"
    echo "   npm run scan                # Escanear tasks CDD"
    echo "   npm run health              # Dashboard de saúde"
    echo ""
    echo "🌐 Acesso:"
    echo "   URL: http://localhost:8000"
    echo "   Admin: admin / B@rcelona1998"
    echo ""
    echo "📊 Status CDD:"
    echo "   ✅ Estrutura modular implementada"
    echo "   ✅ Sistema de autenticação"
    echo "   ✅ Gerenciamento de dados centralizado"
    echo "   ✅ Configuração padronizada"
    echo "   ✅ Logs e monitoramento"
    echo ""
}

# Função principal
main() {
    echo "🚀 Iniciando configuração do Sistema Perfeito CDD v2.0..."
    echo ""
    
    check_python
    check_pip
    setup_venv
    install_dependencies
    setup_data_structure
    check_cdd_structure
    setup_environment
    run_basic_tests
    
    show_system_info
    
    log_success "Sistema configurado com sucesso!"
    echo ""
    echo "🎉 Para iniciar a aplicação, execute:"
    echo "   source .venv/bin/activate"
    echo "   python3 app.py"
    echo ""
}

# Executar função principal
main "$@" 