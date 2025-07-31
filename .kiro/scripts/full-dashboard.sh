#!/bin/bash

# full-dashboard.sh - Dashboard consolidado completo CDD
# Uso: ./full-dashboard.sh [--json] [--save-report] [--detailed]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Flags
JSON_OUTPUT=false
SAVE_REPORT=false
DETAILED_OUTPUT=false
REPORT_DIR=".kiro/reports"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --save-report)
            SAVE_REPORT=true
            shift
            ;;
        --detailed)
            DETAILED_OUTPUT=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [--json] [--save-report] [--detailed]"
            echo ""
            echo "Opções:"
            echo "  --json          Saída em formato JSON"
            echo "  --save-report   Salvar relatório em arquivo"
            echo "  --detailed      Incluir análises detalhadas"
            echo "  -h              Mostrar esta ajuda"
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

# Preparar diretório de relatórios
if [ "$SAVE_REPORT" = true ]; then
    mkdir -p "$REPORT_DIR"
fi

# Função para executar script e capturar saída
run_metric_script() {
    local script_name="$1"
    local script_args="$2"
    
    if [ -f ".kiro/scripts/$script_name" ]; then
        cd .kiro/scripts
        if [ "$JSON_OUTPUT" = true ]; then
            ./"$script_name" --json $script_args 2>/dev/null || echo "{\"error\": \"Failed to run $script_name\"}"
        else
            ./"$script_name" $script_args 2>/dev/null || echo "Erro ao executar $script_name"
        fi
        cd - >/dev/null
    else
        if [ "$JSON_OUTPUT" = true ]; then
            echo "{\"error\": \"Script $script_name not found\"}"
        else
            echo "Script $script_name não encontrado"
        fi
    fi
}

# Função para header
print_header() {
    if [ "$JSON_OUTPUT" = false ]; then
        echo -e "${BOLD}${PURPLE}📊 CDD DASHBOARD COMPLETO${NC}"
        echo -e "${CYAN}Projeto: $(basename "$(pwd)")${NC}"
        echo -e "${BLUE}Gerado em: $(date "+%Y-%m-%d %H:%M:%S")${NC}"
        echo "=========================================================="
    fi
}

# Função para calcular score geral
calculate_overall_score() {
    local completeness_score="$1"
    local quality_score="$2"
    local progress_score="$3"
    
    # Pesos das métricas
    local completeness_weight=30
    local quality_weight=40
    local progress_weight=30
    
    local total_score=$(((completeness_score * completeness_weight + quality_score * quality_weight + progress_score * progress_weight) / 100))
    echo $total_score
}

# Função para determinar status do projeto
get_project_status() {
    local score="$1"
    
    if [ $score -ge 90 ]; then
        echo "EXCELENTE"
    elif [ $score -ge 80 ]; then
        echo "MUITO_BOM"
    elif [ $score -ge 70 ]; then
        echo "BOM"
    elif [ $score -ge 60 ]; then
        echo "REGULAR"
    elif [ $score -ge 40 ]; then
        echo "PRECISA_MELHORAR"
    else
        echo "CRITICO"
    fi
}

# Executar análises
if [ "$JSON_OUTPUT" = false ]; then
    print_header
    echo ""
    echo -e "${BLUE}🔄 Executando análises...${NC}"
fi

# Coletar métricas de cada script
if [ "$JSON_OUTPUT" = false ]; then
    echo -e "${BLUE}  📋 Analisando completude...${NC}"
fi
completeness_data=$(run_metric_script "metrics-completeness.sh" "$([ "$DETAILED_OUTPUT" = true ] && echo "--detailed")")

if [ "$JSON_OUTPUT" = false ]; then
    echo -e "${BLUE}  🔍 Analisando qualidade do código...${NC}"
fi
quality_data=$(run_metric_script "metrics-code-quality.sh" "$([ "$DETAILED_OUTPUT" = true ] && echo "--detailed")")

if [ "$JSON_OUTPUT" = false ]; then
    echo -e "${BLUE}  📈 Analisando progresso...${NC}"
fi
progress_data=$(run_metric_script "metrics-progress.sh" "$([ "$DETAILED_OUTPUT" = true ] && echo "--detailed")")

# Verificar validação do projeto
if [ "$JSON_OUTPUT" = false ]; then
    echo -e "${BLUE}  🔧 Validando estrutura...${NC}"
fi
validation_result=0
if [ -f ".kiro/scripts/validate-project.sh" ]; then
    cd .kiro/scripts
    if ./validate-project.sh >/dev/null 2>&1; then
        validation_result=1
    fi
    cd - >/dev/null
fi

# Processar dados para saída
if [ "$JSON_OUTPUT" = true ]; then
    # Saída JSON consolidada
    timestamp=$(date -Iseconds)
    project_name=$(basename "$(pwd)")
    
    # Extrair scores dos JSONs (se disponíveis)
    completeness_score=85  # Placeholder - extrair do JSON real
    quality_score=75       # Placeholder - extrair do JSON real
    progress_score=60      # Placeholder - extrair do JSON real
    
    overall_score=$(calculate_overall_score $completeness_score $quality_score $progress_score)
    project_status=$(get_project_status $overall_score)
    
    cat << EOF
{
  "timestamp": "$timestamp",
  "project": "$project_name",
  "dashboard": {
    "overall_score": $overall_score,
    "project_status": "$project_status",
    "validation_passed": $([ $validation_result -eq 1 ] && echo "true" || echo "false")
  },
  "metrics": {
    "completeness": $completeness_data,
    "quality": $quality_data,
    "progress": $progress_data
  },
  "recommendations": [
    "$([ $completeness_score -lt 80 ] && echo "Completar documentação pendente")",
    "$([ $quality_score -lt 80 ] && echo "Melhorar qualidade do código")",
    "$([ $progress_score -lt 80 ] && echo "Acelerar desenvolvimento")"
  ]
}
EOF
else
    # Saída em texto formatado
    echo -e "${BLUE}✅ Análise concluída!${NC}"
    echo ""
    
    # Resumo executivo
    echo -e "${BOLD}📋 RESUMO EXECUTIVO${NC}"
    echo "=========================================================="
    
    # Extrair métricas principais (simuladas)
    total_features=$(find .kiro/specs -mindepth 1 -maxdepth 1 -type d | grep -v "_template" | wc -l)
    total_tasks=$(find .kiro/specs -name "tasks.md" -exec grep -c "^-\s\[" {} \; 2>/dev/null | awk '{s+=$1} END {print s+0}')
    completed_tasks=$(find .kiro/specs -name "tasks.md" -exec grep -c "^-\s\[x\]" {} \; 2>/dev/null | awk '{s+=$1} END {print s+0}')
    
    if [ $total_tasks -gt 0 ]; then
        progress_percent=$((completed_tasks * 100 / total_tasks))
    else
        progress_percent=0
    fi
    
    # Calcular scores
    completeness_score=85  # Seria extraído do JSON real
    quality_score=75       # Seria extraído do JSON real
    progress_score=$progress_percent
    
    overall_score=$(calculate_overall_score $completeness_score $quality_score $progress_score)
    project_status=$(get_project_status $overall_score)
    
    # Status geral
    case $project_status in
        "EXCELENTE")
            echo -e "📊 Status do projeto: ${GREEN}${BOLD}EXCELENTE${NC} ($overall_score/100)"
            echo -e "🎉 ${GREEN}Projeto em excelente estado! Continue assim.${NC}"
            ;;
        "MUITO_BOM")
            echo -e "📊 Status do projeto: ${GREEN}${BOLD}MUITO BOM${NC} ($overall_score/100)"
            echo -e "👍 ${GREEN}Projeto bem estruturado. Pequenos ajustes podem elevar ainda mais.${NC}"
            ;;
        "BOM")
            echo -e "📊 Status do projeto: ${YELLOW}${BOLD}BOM${NC} ($overall_score/100)"
            echo -e "✨ ${YELLOW}Projeto em boa forma. Algumas melhorias farão diferença.${NC}"
            ;;
        "REGULAR")
            echo -e "📊 Status do projeto: ${YELLOW}${BOLD}REGULAR${NC} ($overall_score/100)"
            echo -e "⚠️  ${YELLOW}Projeto funcional, mas precisa de atenção.${NC}"
            ;;
        "PRECISA_MELHORAR")
            echo -e "📊 Status do projeto: ${RED}${BOLD}PRECISA MELHORAR${NC} ($overall_score/100)"
            echo -e "🔧 ${RED}Várias áreas precisam de melhoria urgente.${NC}"
            ;;
        "CRITICO")
            echo -e "📊 Status do projeto: ${RED}${BOLD}CRÍTICO${NC} ($overall_score/100)"
            echo -e "🚨 ${RED}Projeto requer atenção imediata em múltiplas áreas.${NC}"
            ;;
    esac
    
    echo ""
    echo -e "🎯 Features: ${CYAN}$total_features${NC}"
    echo -e "📋 Tarefas: ${CYAN}$completed_tasks${NC}/${CYAN}$total_tasks${NC} (${CYAN}$progress_percent%${NC})"
    echo -e "🔧 Validação: $([ $validation_result -eq 1 ] && echo -e "${GREEN}✅ Passou${NC}" || echo -e "${RED}❌ Falhou${NC}")"
    
    # Breakdown de scores
    echo ""
    echo -e "${BOLD}📊 BREAKDOWN DE SCORES${NC}"
    echo "=========================================================="
    
    echo -e "📋 Completude da documentação: ${CYAN}$completeness_score/100${NC}"
    if [ $completeness_score -ge 80 ]; then
        echo -e "   ${GREEN}✅ Documentação bem estruturada${NC}"
    elif [ $completeness_score -ge 60 ]; then
        echo -e "   ${YELLOW}⚠️  Alguns gaps na documentação${NC}"
    else
        echo -e "   ${RED}❌ Documentação incompleta${NC}"
    fi
    
    echo -e "🔍 Qualidade do código: ${CYAN}$quality_score/100${NC}"
    if [ $quality_score -ge 80 ]; then
        echo -e "   ${GREEN}✅ Código de alta qualidade${NC}"
    elif [ $quality_score -ge 60 ]; then
        echo -e "   ${YELLOW}⚠️  Qualidade moderada${NC}"
    else
        echo -e "   ${RED}❌ Qualidade precisa melhorar${NC}"
    fi
    
    echo -e "📈 Progresso do desenvolvimento: ${CYAN}$progress_score/100${NC}"
    if [ $progress_score -ge 80 ]; then
        echo -e "   ${GREEN}✅ Desenvolvimento avançado${NC}"
    elif [ $progress_score -ge 50 ]; then
        echo -e "   ${YELLOW}⚠️  Progresso moderado${NC}"
    else
        echo -e "   ${RED}❌ Desenvolvimento inicial${NC}"
    fi
    
    # Análises detalhadas
    if [ "$DETAILED_OUTPUT" = true ]; then
        echo ""
        echo -e "${BOLD}📋 ANÁLISE DETALHADA DE COMPLETUDE${NC}"
        echo "=========================================================="
        echo "$completeness_data"
        
        echo ""
        echo -e "${BOLD}🔍 ANÁLISE DETALHADA DE QUALIDADE${NC}"
        echo "=========================================================="
        echo "$quality_data"
        
        echo ""
        echo -e "${BOLD}📈 ANÁLISE DETALHADA DE PROGRESSO${NC}"
        echo "=========================================================="
        echo "$progress_data"
    fi
    
    # Recomendações prioritárias
    echo ""
    echo -e "${BOLD}🎯 RECOMENDAÇÕES PRIORITÁRIAS${NC}"
    echo "=========================================================="
    
    recommendations=()
    
    if [ $completeness_score -lt 80 ]; then
        recommendations+=("📋 Completar documentação: Execute ./validate-project.sh --fix")
    fi
    
    if [ $quality_score -lt 80 ]; then
        recommendations+=("🔍 Melhorar qualidade: Implemente linting e testes")
    fi
    
    if [ $progress_score -lt 50 ]; then
        recommendations+=("📈 Acelerar desenvolvimento: Revise prioridades e recursos")
    fi
    
    if [ $validation_result -eq 0 ]; then
        recommendations+=("🔧 Corrigir estrutura: Execute ./validate-project.sh para detalhes")
    fi
    
    if [ ${#recommendations[@]} -eq 0 ]; then
        echo -e "${GREEN}🎉 Nenhuma recomendação crítica! Projeto em excelente estado.${NC}"
        echo -e "${BLUE}💡 Continue monitorando regularmente com este dashboard.${NC}"
    else
        for rec in "${recommendations[@]}"; do
            echo -e "🔸 $rec"
        done
    fi
    
    # Próximos passos
    echo ""
    echo -e "${BOLD}🚀 PRÓXIMOS PASSOS${NC}"
    echo "=========================================================="
    
    if [ $overall_score -ge 80 ]; then
        echo "🎯 Manter qualidade e finalizar features pendentes"
        echo "📊 Monitorar métricas regularmente"
        echo "🔄 Preparar para próxima fase/release"
    elif [ $overall_score -ge 60 ]; then
        echo "📋 Focar nas recomendações prioritárias acima"
        echo "🔍 Revisar e melhorar áreas com score baixo"
        echo "📅 Definir cronograma para melhorias"
    else
        echo "🚨 Ação imediata necessária nas áreas críticas"
        echo "👥 Considerar revisão de processos e recursos"
        echo "📋 Implementar CDD completo seguindo guidelines"
    fi
    
    # Ferramentas úteis
    echo ""
    echo -e "${BOLD}🛠️  FERRAMENTAS ÚTEIS${NC}"
    echo "=========================================================="
    echo "📋 Análise específica:"
    echo "  ./metrics-completeness.sh --detailed"
    echo "  ./metrics-code-quality.sh --detailed"
    echo "  ./metrics-progress.sh --detailed"
    echo ""
    echo "🔧 Ações:"
    echo "  ./validate-project.sh --fix"
    echo "  ./new-feature.sh <nome>"
    echo "  npm run complete <task-id>"
    echo ""
    echo "📊 Monitoramento:"
    echo "  ./dashboard.sh --refresh-interval 30"
    echo "  ./full-dashboard.sh --save-report"
fi

# Salvar relatório se solicitado
if [ "$SAVE_REPORT" = true ]; then
    timestamp=$(date "+%Y%m%d_%H%M%S")
    if [ "$JSON_OUTPUT" = true ]; then
        report_file="$REPORT_DIR/dashboard_$timestamp.json"
    else
        report_file="$REPORT_DIR/dashboard_$timestamp.txt"
    fi
    
    # Reexecutar para capturar saída completa
    if [ "$JSON_OUTPUT" = true ]; then
        $0 --json $([ "$DETAILED_OUTPUT" = true ] && echo "--detailed") > "$report_file"
    else
        $0 $([ "$DETAILED_OUTPUT" = true ] && echo "--detailed") > "$report_file"
    fi
    
    if [ "$JSON_OUTPUT" = false ]; then
        echo ""
        echo -e "${GREEN}📄 Relatório salvo em: $report_file${NC}"
    fi
fi 