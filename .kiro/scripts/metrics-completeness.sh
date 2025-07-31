#!/bin/bash

# metrics-completeness.sh - Análise de completude da documentação CDD
# Uso: ./metrics-completeness.sh [--json] [--detailed]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Flags
JSON_OUTPUT=false
DETAILED_OUTPUT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --detailed)
            DETAILED_OUTPUT=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [--json] [--detailed]"
            echo ""
            echo "Opções:"
            echo "  --json       Saída em formato JSON"
            echo "  --detailed   Incluir detalhes sobre cada problema"
            echo "  -h           Mostrar esta ajuda"
            exit 0
            ;;
        *)
            echo "Opção desconhecida: $1"
            exit 1
            ;;
    esac
done

# Verificar se estamos no diretório correto
if [ ! -d ".kiro" ]; then
    echo "❌ Erro: Diretório .kiro não encontrado!"
    echo "Execute este script no diretório raiz do projeto"
    exit 1
fi

# Funções para output
print_header() {
    if [ "$JSON_OUTPUT" = false ]; then
        echo -e "\n${PURPLE}📋 $1${NC}"
        echo "===================================="
    fi
}

print_metric() {
    local label="$1"
    local value="$2"
    local status="$3"  # success, warning, error
    
    if [ "$JSON_OUTPUT" = false ]; then
        case $status in
            "success")
                echo -e "${GREEN}✅ $label: $value${NC}"
                ;;
            "warning")
                echo -e "${YELLOW}⚠️  $label: $value${NC}"
                ;;
            "error")
                echo -e "${RED}❌ $label: $value${NC}"
                ;;
            *)
                echo -e "${BLUE}📊 $label: $value${NC}"
                ;;
        esac
    fi
}

# Variáveis para coleta de métricas
total_specs=0
complete_specs=0
incomplete_specs=0
specs_with_placeholders=0
specs_with_todos=0
total_placeholders=0
total_todos=0
missing_files=()
incomplete_spec_details=()

# Análise das especificações
print_header "ANÁLISE DE COMPLETUDE DAS ESPECIFICAÇÕES"

# Verificar cada spec
for spec_dir in .kiro/specs/*/; do
    if [ -d "$spec_dir" ] && [ "$(basename "$spec_dir")" != "_template" ]; then
        spec_name=$(basename "$spec_dir")
        total_specs=$((total_specs + 1))
        
        spec_missing=()
        spec_incomplete=false
        
        # Verificar arquivos obrigatórios
        if [ ! -f "$spec_dir/requirements.md" ]; then
            spec_missing+=("requirements.md")
            missing_files+=("$spec_name/requirements.md")
            spec_incomplete=true
        fi
        
        if [ ! -f "$spec_dir/design.md" ]; then
            spec_missing+=("design.md")
            missing_files+=("$spec_name/design.md")
            spec_incomplete=true
        fi
        
        if [ ! -f "$spec_dir/tasks.md" ]; then
            spec_missing+=("tasks.md")
            missing_files+=("$spec_name/tasks.md")
            spec_incomplete=true
        fi
        
        if [ "$spec_incomplete" = true ]; then
            incomplete_specs=$((incomplete_specs + 1))
            incomplete_spec_details+=("$spec_name: faltam ${spec_missing[*]}")
            print_metric "Spec incompleta" "$spec_name (faltam: ${spec_missing[*]})" "error"
        else
            complete_specs=$((complete_specs + 1))
            print_metric "Spec completa" "$spec_name" "success"
        fi
        
        # Verificar placeholders em arquivos existentes
        spec_placeholders=0
        for file in "$spec_dir"/*.md; do
            if [ -f "$file" ]; then
                file_placeholders=$(grep -c "\[.*\]" "$file" 2>/dev/null || echo "0")
                spec_placeholders=$((spec_placeholders + file_placeholders))
            fi
        done
        
        if [ $spec_placeholders -gt 0 ]; then
            specs_with_placeholders=$((specs_with_placeholders + 1))
            total_placeholders=$((total_placeholders + spec_placeholders))
            if [ "$DETAILED_OUTPUT" = true ]; then
                print_metric "Placeholders encontrados" "$spec_name ($spec_placeholders placeholders)" "warning"
            fi
        fi
        
        # Verificar TODOs
        spec_todos=0
        for file in "$spec_dir"/*.md; do
            if [ -f "$file" ]; then
                file_todos=$(grep -c "TODO\|FIXME\|XXX" "$file" 2>/dev/null || echo "0")
                spec_todos=$((spec_todos + file_todos))
            fi
        done
        
        if [ $spec_todos -gt 0 ]; then
            specs_with_todos=$((specs_with_todos + 1))
            total_todos=$((total_todos + spec_todos))
            if [ "$DETAILED_OUTPUT" = true ]; then
                print_metric "TODOs encontrados" "$spec_name ($spec_todos TODOs)" "warning"
            fi
        fi
    fi
done

# Calcular métricas de completude
if [ $total_specs -gt 0 ]; then
    completion_rate=$((complete_specs * 100 / total_specs))
else
    completion_rate=100
fi

# Verificar arquivos de steering
print_header "ANÁLISE DOS DOCUMENTOS DE STEERING"

steering_files=("product.md" "structure.md" "tech.md")
steering_complete=true
steering_missing=()
steering_placeholders=0
steering_todos=0

for file in "${steering_files[@]}"; do
    if [ ! -f ".kiro/steering/$file" ]; then
        steering_complete=false
        steering_missing+=("$file")
        missing_files+=("steering/$file")
        print_metric "Arquivo de steering ausente" "$file" "error"
    else
        print_metric "Arquivo de steering encontrado" "$file" "success"
        
        # Contar placeholders
        file_placeholders=$(grep -c "\[.*\]" ".kiro/steering/$file" 2>/dev/null || echo "0")
        steering_placeholders=$((steering_placeholders + file_placeholders))
        
        # Contar TODOs
        file_todos=$(grep -c "TODO\|FIXME\|XXX" ".kiro/steering/$file" 2>/dev/null || echo "0")
        steering_todos=$((steering_todos + file_todos))
    fi
done

# Verificar templates
print_header "ANÁLISE DOS TEMPLATES"

template_files=("requirements.md" "design.md" "tasks.md")
template_complete=true
template_missing=()

for file in "${template_files[@]}"; do
    if [ ! -f ".kiro/specs/_template/$file" ]; then
        template_complete=false
        template_missing+=("$file")
        missing_files+=("_template/$file")
        print_metric "Template ausente" "$file" "error"
    else
        print_metric "Template encontrado" "$file" "success"
    fi
done

# Verificar patterns (se existir)
patterns_exists=false
patterns_complete=true
patterns_missing=()
patterns_placeholders=0
patterns_todos=0

if [ -d ".kiro/patterns" ]; then
    patterns_exists=true
    print_header "ANÁLISE DOS PADRÕES"
    
    if [ ! -f ".kiro/patterns/README.md" ]; then
        patterns_complete=false
        patterns_missing+=("README.md")
        print_metric "Arquivo de patterns ausente" "README.md" "warning"
    else
        print_metric "Arquivo de patterns encontrado" "README.md" "success"
    fi
    
    if [ ! -f ".kiro/patterns/conventions.md" ]; then
        patterns_complete=false
        patterns_missing+=("conventions.md")
        print_metric "Arquivo de patterns ausente" "conventions.md" "warning"
    else
        print_metric "Arquivo de patterns encontrado" "conventions.md" "success"
    fi
    
    # Contar placeholders e TODOs em patterns
    for file in .kiro/patterns/*.md; do
        if [ -f "$file" ]; then
            file_placeholders=$(grep -c "\[.*\]" "$file" 2>/dev/null || echo "0")
            patterns_placeholders=$((patterns_placeholders + file_placeholders))
            
            file_todos=$(grep -c "TODO\|FIXME\|XXX" "$file" 2>/dev/null || echo "0")
            patterns_todos=$((patterns_todos + file_todos))
        fi
    done
fi

# Calcular métricas globais
total_placeholders=$((total_placeholders + steering_placeholders + patterns_placeholders))
total_todos=$((total_todos + steering_todos + patterns_todos))

# Saída dos resultados
if [ "$JSON_OUTPUT" = true ]; then
    # Saída em JSON
    cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "project": "$(basename "$(pwd)")",
  "metrics": {
    "specs": {
      "total": $total_specs,
      "complete": $complete_specs,
      "incomplete": $incomplete_specs,
      "completion_rate": $completion_rate,
      "with_placeholders": $specs_with_placeholders,
      "with_todos": $specs_with_todos
    },
    "steering": {
      "complete": $([ "$steering_complete" = true ] && echo "true" || echo "false"),
      "missing_files": $(printf '%s\n' "${steering_missing[@]}" | jq -R . | jq -s .),
      "placeholders": $steering_placeholders,
      "todos": $steering_todos
    },
    "templates": {
      "complete": $([ "$template_complete" = true ] && echo "true" || echo "false"),
      "missing_files": $(printf '%s\n' "${template_missing[@]}" | jq -R . | jq -s .)
    },
    "patterns": {
      "exists": $([ "$patterns_exists" = true ] && echo "true" || echo "false"),
      "complete": $([ "$patterns_complete" = true ] && echo "true" || echo "false"),
      "missing_files": $(printf '%s\n' "${patterns_missing[@]}" | jq -R . | jq -s .),
      "placeholders": $patterns_placeholders,
      "todos": $patterns_todos
    },
    "global": {
      "total_placeholders": $total_placeholders,
      "total_todos": $total_todos,
      "missing_files_count": ${#missing_files[@]}
    }
  },
  "details": {
    "incomplete_specs": $(printf '%s\n' "${incomplete_spec_details[@]}" | jq -R . | jq -s .),
    "missing_files": $(printf '%s\n' "${missing_files[@]}" | jq -R . | jq -s .)
  }
}
EOF
else
    # Saída em texto
    print_header "RESUMO DE COMPLETUDE"
    
    echo "📊 Especificações:"
    print_metric "Total de specs" "$total_specs"
    print_metric "Specs completas" "$complete_specs" "$([ $complete_specs -eq $total_specs ] && echo "success" || echo "warning")"
    print_metric "Specs incompletas" "$incomplete_specs" "$([ $incomplete_specs -eq 0 ] && echo "success" || echo "error")"
    print_metric "Taxa de conclusão" "$completion_rate%" "$([ $completion_rate -ge 90 ] && echo "success" || [ $completion_rate -ge 70 ] && echo "warning" || echo "error")"
    
    echo ""
    echo "📋 Documentação de steering:"
    print_metric "Arquivos de steering completos" "$([ "$steering_complete" = true ] && echo "Sim" || echo "Não")" "$([ "$steering_complete" = true ] && echo "success" || echo "error")"
    if [ ${#steering_missing[@]} -gt 0 ]; then
        print_metric "Arquivos ausentes" "${steering_missing[*]}" "error"
    fi
    
    echo ""
    echo "📐 Templates:"
    print_metric "Templates completos" "$([ "$template_complete" = true ] && echo "Sim" || echo "Não")" "$([ "$template_complete" = true ] && echo "success" || echo "error")"
    if [ ${#template_missing[@]} -gt 0 ]; then
        print_metric "Templates ausentes" "${template_missing[*]}" "error"
    fi
    
    if [ "$patterns_exists" = true ]; then
        echo ""
        echo "🎨 Padrões:"
        print_metric "Padrões configurados" "$([ "$patterns_complete" = true ] && echo "Sim" || echo "Parcialmente")" "$([ "$patterns_complete" = true ] && echo "success" || echo "warning")"
    fi
    
    echo ""
    echo "🔧 Trabalho pendente:"
    print_metric "Placeholders não substituídos" "$total_placeholders" "$([ $total_placeholders -eq 0 ] && echo "success" || [ $total_placeholders -le 5 ] && echo "warning" || echo "error")"
    print_metric "TODOs pendentes" "$total_todos" "$([ $total_todos -eq 0 ] && echo "success" || [ $total_todos -le 10 ] && echo "warning" || echo "error")"
    print_metric "Arquivos ausentes" "${#missing_files[@]}" "$([ ${#missing_files[@]} -eq 0 ] && echo "success" || echo "error")"
    
    if [ "$DETAILED_OUTPUT" = true ] && [ ${#missing_files[@]} -gt 0 ]; then
        echo ""
        echo "❌ Arquivos ausentes:"
        for file in "${missing_files[@]}"; do
            echo "  - .kiro/$file"
        done
    fi
    
    if [ "$DETAILED_OUTPUT" = true ] && [ ${#incomplete_spec_details[@]} -gt 0 ]; then
        echo ""
        echo "⚠️  Specs incompletas:"
        for detail in "${incomplete_spec_details[@]}"; do
            echo "  - $detail"
        done
    fi
    
    # Score geral
    echo ""
    print_header "SCORE DE COMPLETUDE"
    
    # Calcular score (0-100)
    score=0
    max_score=100
    
    # Peso das métricas
    spec_weight=40
    steering_weight=25
    template_weight=15
    quality_weight=20
    
    # Score de specs
    if [ $total_specs -gt 0 ]; then
        spec_score=$((completion_rate * spec_weight / 100))
    else
        spec_score=$spec_weight  # Se não há specs, considera completo
    fi
    
    # Score de steering
    if [ "$steering_complete" = true ]; then
        steering_score=$steering_weight
    else
        steering_score=0
    fi
    
    # Score de templates
    if [ "$template_complete" = true ]; then
        template_score=$template_weight
    else
        template_score=0
    fi
    
    # Score de qualidade (baseado em placeholders e TODOs)
    quality_penalty=$((total_placeholders + total_todos))
    quality_score=$((quality_weight - quality_penalty))
    if [ $quality_score -lt 0 ]; then
        quality_score=0
    fi
    
    total_score=$((spec_score + steering_score + template_score + quality_score))
    
    if [ $total_score -ge 90 ]; then
        print_metric "Score geral" "$total_score/100" "success"
        echo -e "${GREEN}🎉 Excelente! Documentação está muito bem estruturada.${NC}"
    elif [ $total_score -ge 70 ]; then
        print_metric "Score geral" "$total_score/100" "warning"
        echo -e "${YELLOW}👍 Boa! Algumas melhorias podem ser feitas.${NC}"
    else
        print_metric "Score geral" "$total_score/100" "error"
        echo -e "${RED}🔧 Atenção! Documentação precisa de melhorias significativas.${NC}"
    fi
fi 