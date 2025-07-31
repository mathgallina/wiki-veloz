#!/bin/bash

# validate-project.sh - Script para validar estrutura CDD completa
# Uso: ./validate-project.sh [--fix]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Flags
FIX_MODE=false
ERRORS=0
WARNINGS=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            FIX_MODE=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [--fix]"
            echo ""
            echo "Opções:"
            echo "  --fix    Tentar corrigir problemas automaticamente"
            echo "  -h       Mostrar esta ajuda"
            exit 0
            ;;
        *)
            echo "Opção desconhecida: $1"
            exit 1
            ;;
    esac
done

# Funções para output colorido
print_header() {
    echo -e "\n${PURPLE}🔍 $1${NC}"
    echo "=================================="
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    ((ERRORS++))
}

print_fix() {
    echo -e "${GREEN}🔧 $1${NC}"
}

# Função para criar diretório se não existir
ensure_directory() {
    local dir="$1"
    local description="$2"
    
    if [ ! -d "$dir" ]; then
        if [ "$FIX_MODE" = true ]; then
            mkdir -p "$dir"
            print_fix "Criado diretório: $dir"
        else
            print_error "Diretório obrigatório não encontrado: $dir ($description)"
        fi
    else
        print_success "Diretório encontrado: $dir"
    fi
}

# Função para criar arquivo se não existir
ensure_file() {
    local file="$1"
    local description="$2"
    local template_content="$3"
    
    if [ ! -f "$file" ]; then
        if [ "$FIX_MODE" = true ]; then
            if [ -n "$template_content" ]; then
                echo "$template_content" > "$file"
                print_fix "Criado arquivo: $file"
            else
                touch "$file"
                print_fix "Criado arquivo vazio: $file"
            fi
        else
            print_error "Arquivo obrigatório não encontrado: $file ($description)"
        fi
    else
        print_success "Arquivo encontrado: $file"
    fi
}

# Verificar se estamos no diretório correto
print_header "VERIFICAÇÃO DE LOCALIZAÇÃO"

if [ ! -d ".kiro" ]; then
    print_error "Diretório .kiro não encontrado!"
    print_info "Este script deve ser executado no diretório raiz do projeto"
    exit 1
fi

print_success "Executando no diretório correto (encontrado .kiro/)"

# Verificar estrutura base do CDD
print_header "ESTRUTURA BASE CDD"

# Diretórios obrigatórios
ensure_directory ".kiro/steering" "Documentos de direcionamento do projeto"
ensure_directory ".kiro/specs" "Especificações de funcionalidades"
ensure_directory ".kiro/specs/_template" "Templates para novas features"

# Verificar se patterns existe (recomendado)
if [ ! -d ".kiro/patterns" ]; then
    print_warning "Diretório .kiro/patterns não encontrado (recomendado para projetos maduros)"
    if [ "$FIX_MODE" = true ]; then
        mkdir -p ".kiro/patterns"
        print_fix "Criado diretório: .kiro/patterns"
    fi
else
    print_success "Diretório encontrado: .kiro/patterns"
fi

# Verificar arquivos de steering
print_header "DOCUMENTOS DE STEERING"

# Templates para arquivos de steering
product_template='# [Nome do Projeto] - Visão de Produto

## Problema que Resolve
[Descreva o problema que o projeto resolve]

## Solução Proposta
[Descreva a solução e valor único]

## Objetivos de Negócio
[Defina métricas de sucesso e KPIs]

## Usuários-Alvo
[Identifique personas e casos de uso]'

structure_template='# Organização & Estrutura de Pastas

## Filosofia de Organização
[Explique os princípios que guiam a organização]

## Estrutura de Diretórios
```
projeto/
├── src/           # Código principal
├── docs/          # Documentação
├── tests/         # Testes
└── config/        # Configurações
```

## Convenções
[Defina padrões de nomenclatura e organização]'

tech_template='# Stack Tecnológico e Decisões Técnicas

## Stack Principal
[Liste as tecnologias principais e suas justificativas]

## Ferramentas de Desenvolvimento
[Ferramentas para desenvolvimento, build, deploy]

## Configurações Essenciais
[Comandos e configurações importantes]

## Decisões Arquiteturais
[Documente decisões técnicas importantes]'

ensure_file ".kiro/steering/product.md" "Visão de produto" "$product_template"
ensure_file ".kiro/steering/structure.md" "Estrutura do projeto" "$structure_template"
ensure_file ".kiro/steering/tech.md" "Stack tecnológico" "$tech_template"

# Verificar templates
print_header "TEMPLATES DE ESPECIFICAÇÃO"

requirements_template='# [Nome da Funcionalidade] - Requisitos

## Visão Geral
[Descrição geral da funcionalidade]

## Requisitos Funcionais

### RF01 - [Nome do Requisito]
**Como** [tipo de usuário]
**Eu quero** [ação/funcionalidade]
**Para que** [benefício/valor]

**Critérios de Aceite:**
- [ ] [Critério específico e testável]
- [ ] [Critério específico e testável]

## Requisitos Não Funcionais
[Performance, segurança, usabilidade, etc.]

## Regras de Negócio
[Regras específicas do domínio]'

design_template='# [Nome da Funcionalidade] - Design Técnico

## Arquitetura

### Visão Geral
[Descrição da arquitetura da funcionalidade]

### Componentes
[Liste os principais componentes]

### Fluxo de Dados
[Descreva o fluxo de dados]

## APIs e Interfaces
[Defina APIs, endpoints, contratos]

## Considerações Técnicas
[Performance, segurança, patterns a serem usados]'

tasks_template='# [Nome da Funcionalidade] - Plano de Execução

## Fases de Desenvolvimento

### Fase 1: [Nome da Fase]
- [ ] [nome-da-funcionalidade-1.1] [Descrição da tarefa] (Estimativa: XhY)
- [ ] [nome-da-funcionalidade-1.2] [Descrição da tarefa] (Estimativa: XhY)

### Fase 2: [Nome da Fase]
- [ ] [nome-da-funcionalidade-2.1] [Descrição da tarefa] (Estimativa: XhY)
- [ ] [nome-da-funcionalidade-2.2] [Descrição da tarefa] (Estimativa: XhY)

## Critérios de Aceite Geral
[Critérios para considerar a feature completa]

## Dependências
[Liste dependências de outras features ou sistemas]'

ensure_file ".kiro/specs/_template/requirements.md" "Template de requisitos" "$requirements_template"
ensure_file ".kiro/specs/_template/design.md" "Template de design" "$design_template"
ensure_file ".kiro/specs/_template/tasks.md" "Template de tarefas" "$tasks_template"

# Verificar patterns (se existir)
if [ -d ".kiro/patterns" ]; then
    print_header "PADRÕES DE CÓDIGO"
    
    conventions_template='# Convenções Gerais de Código

## Nomenclatura
[Defina padrões de nomenclatura]

## Estrutura de Arquivos
[Como organizar arquivos e pastas]

## Comentários e Documentação
[Quando e como comentar código]

## Boas Práticas Gerais
[Práticas recomendadas para o projeto]'

    ensure_file ".kiro/patterns/README.md" "Índice dos padrões"
    ensure_file ".kiro/patterns/conventions.md" "Convenções gerais" "$conventions_template"
    
    # Verificar estrutura de patterns
    if [ ! -d ".kiro/patterns/examples" ]; then
        if [ "$FIX_MODE" = true ]; then
            mkdir -p ".kiro/patterns/examples"
            print_fix "Criado diretório: .kiro/patterns/examples"
        else
            print_warning "Diretório .kiro/patterns/examples não encontrado (recomendado)"
        fi
    fi
    
    if [ ! -d ".kiro/patterns/linting" ]; then
        if [ "$FIX_MODE" = true ]; then
            mkdir -p ".kiro/patterns/linting"
            print_fix "Criado diretório: .kiro/patterns/linting"
        else
            print_warning "Diretório .kiro/patterns/linting não encontrado (recomendado)"
        fi
    fi
fi

# Verificar scripts de automação
print_header "SCRIPTS DE AUTOMAÇÃO"

if [ ! -d ".kiro/scripts" ]; then
    print_warning "Diretório .kiro/scripts não encontrado (funcionalidades limitadas)"
else
    print_success "Diretório encontrado: .kiro/scripts"
    
    # Verificar arquivos importantes
    if [ ! -f ".kiro/scripts/package.json" ]; then
        print_warning "package.json não encontrado em scripts/"
    else
        print_success "package.json encontrado"
    fi
    
    if [ ! -f ".kiro/scripts/task-manager.js" ]; then
        print_warning "task-manager.js não encontrado (tracking limitado)"
    else
        print_success "task-manager.js encontrado"
    fi
fi

# Verificar integridade das specs existentes
print_header "INTEGRIDADE DAS ESPECIFICAÇÕES"

spec_count=0
incomplete_specs=0

for spec_dir in .kiro/specs/*/; do
    if [ -d "$spec_dir" ] && [ "$(basename "$spec_dir")" != "_template" ]; then
        spec_name=$(basename "$spec_dir")
        spec_count=$((spec_count + 1))
        
        missing_files=()
        
        if [ ! -f "$spec_dir/requirements.md" ]; then
            missing_files+=("requirements.md")
        fi
        
        if [ ! -f "$spec_dir/design.md" ]; then
            missing_files+=("design.md")
        fi
        
        if [ ! -f "$spec_dir/tasks.md" ]; then
            missing_files+=("tasks.md")
        fi
        
        if [ ${#missing_files[@]} -eq 0 ]; then
            print_success "Spec completa: $spec_name"
        else
            print_error "Spec incompleta: $spec_name (faltam: ${missing_files[*]})"
            incomplete_specs=$((incomplete_specs + 1))
        fi
    fi
done

if [ $spec_count -eq 0 ]; then
    print_info "Nenhuma especificação encontrada (apenas template existe)"
else
    print_info "Total de specs: $spec_count (completas: $((spec_count - incomplete_specs)), incompletas: $incomplete_specs)"
fi

# Verificar placeholders não substituídos
print_header "VERIFICAÇÃO DE PLACEHOLDERS"

placeholder_files=$(find .kiro -name "*.md" -exec grep -l "\[.*\]" {} \; 2>/dev/null | grep -v "_template" || true)

if [ -n "$placeholder_files" ]; then
    print_warning "Arquivos com placeholders encontrados:"
    echo "$placeholder_files" | while read -r file; do
        placeholders=$(grep -o "\[.*\]" "$file" | head -3 | tr '\n' ' ')
        echo "  $file: $placeholders"
    done
else
    print_success "Nenhum placeholder encontrado (exceto templates)"
fi

# Verificar TODOs pendentes
print_header "TODOs PENDENTES"

todo_count=$(find .kiro -name "*.md" -exec grep -c "TODO\|FIXME\|XXX" {} \; 2>/dev/null | awk '{s+=$1} END {print s+0}')

if [ $todo_count -gt 0 ]; then
    print_warning "$todo_count TODOs encontrados na documentação"
    find .kiro -name "*.md" -exec grep -Hn "TODO\|FIXME\|XXX" {} \; 2>/dev/null | head -5
    if [ $todo_count -gt 5 ]; then
        print_info "... e mais $((todo_count - 5)) TODOs"
    fi
else
    print_success "Nenhum TODO pendente encontrado"
fi

# Verificar configurações de projeto
print_header "CONFIGURAÇÕES DE PROJETO"

# Verificar git
if [ ! -d ".git" ]; then
    print_warning "Projeto não está em um repositório git"
else
    print_success "Repositório git encontrado"
fi

# Verificar .gitignore
if [ ! -f ".gitignore" ]; then
    print_warning "Arquivo .gitignore não encontrado"
else
    print_success "Arquivo .gitignore encontrado"
fi

# Resumo final
print_header "RESUMO DA VALIDAÇÃO"

echo "📊 Estatísticas:"
echo "  - Erros: $ERRORS"
echo "  - Avisos: $WARNINGS"
echo "  - Specs encontradas: $spec_count"
echo "  - TODOs pendentes: $todo_count"

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        print_success "🎉 Projeto CDD está em perfeito estado!"
    else
        print_warning "✅ Projeto CDD está funcional, mas há algumas melhorias recomendadas"
    fi
else
    print_error "❌ Projeto CDD tem problemas que precisam ser corrigidos"
    
    if [ "$FIX_MODE" = false ]; then
        echo ""
        print_info "Execute com --fix para tentar corrigir automaticamente:"
        echo "  $0 --fix"
    fi
fi

# Exit code baseado nos resultados
if [ $ERRORS -gt 0 ]; then
    exit 1
else
    exit 0
fi 