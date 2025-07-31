#!/bin/bash

# analyze-feedback.sh - Análise dos feedbacks coletados sobre CDD
# Uso: ./analyze-feedback.sh [--json] [--detailed] [--since <days>]

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

# Configurações
FEEDBACK_DIR=".kiro/feedback"
JSON_OUTPUT=false
DETAILED_OUTPUT=false
SINCE_DAYS=""

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
        --since)
            SINCE_DAYS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Uso: $0 [--json] [--detailed] [--since <days>]"
            echo ""
            echo "Opções:"
            echo "  --json             Saída em formato JSON"
            echo "  --detailed         Incluir análise detalhada"
            echo "  --since <days>     Analisar apenas feedbacks dos últimos N dias"
            echo "  -h                 Mostrar esta ajuda"
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

# Verificar se diretório de feedback existe
if [ ! -d "$FEEDBACK_DIR" ]; then
    echo "❌ Nenhum feedback encontrado!"
    echo "Execute ./collect-feedback.sh primeiro para coletar feedback da equipe."
    exit 1
fi

# Função para extrair valor JSON
extract_json_value() {
    local file="$1"
    local path="$2"
    
    if command -v jq >/dev/null 2>&1; then
        jq -r "$path // \"N/A\"" "$file" 2>/dev/null
    else
        # Fallback simples para alguns casos
        case "$path" in
            ".ratings.effectiveness")
                grep -o '"effectiveness":\s*[0-9]*' "$file" | grep -o '[0-9]*' || echo "N/A"
                ;;
            ".ratings.productivity")
                grep -o '"productivity":\s*[0-9]*' "$file" | grep -o '[0-9]*' || echo "N/A"
                ;;
            ".qualitative.pain_point")
                grep -o '"pain_point":\s*"[^"]*"' "$file" | sed 's/.*"\([^"]*\)"/\1/' || echo "N/A"
                ;;
            *)
                echo "N/A"
                ;;
        esac
    fi
}

# Função para calcular média
calculate_average() {
    local sum=0
    local count=0
    
    for value in "$@"; do
        if [[ "$value" =~ ^[0-9]+$ ]]; then
            sum=$((sum + value))
            count=$((count + 1))
        fi
    done
    
    if [ $count -gt 0 ]; then
        echo $((sum / count))
    else
        echo "0"
    fi
}

# Função para contar ocorrências
count_occurrences() {
    local pattern="$1"
    shift
    local count=0
    
    for item in "$@"; do
        if [[ "$item" == *"$pattern"* ]]; then
            count=$((count + 1))
        fi
    done
    
    echo $count
}

# Coletar arquivos de feedback
feedback_files=()
cutoff_date=""

if [ -n "$SINCE_DAYS" ]; then
    cutoff_date=$(date -d "$SINCE_DAYS days ago" +%Y%m%d 2>/dev/null || date -v-"$SINCE_DAYS"d +%Y%m%d 2>/dev/null)
fi

for file in "$FEEDBACK_DIR"/feedback_*.json; do
    if [ -f "$file" ]; then
        if [ -n "$cutoff_date" ]; then
            file_date=$(basename "$file" | sed 's/feedback_\([0-9]\{8\}\).*/\1/')
            if [[ "$file_date" =~ ^[0-9]{8}$ ]] && [ "$file_date" -ge "$cutoff_date" ]; then
                feedback_files+=("$file")
            fi
        else
            feedback_files+=("$file")
        fi
    fi
done

if [ ${#feedback_files[@]} -eq 0 ]; then
    echo "❌ Nenhum feedback encontrado!"
    if [ -n "$SINCE_DAYS" ]; then
        echo "Tente executar sem --since ou com um período maior."
    else
        echo "Execute ./collect-feedback.sh primeiro para coletar feedback da equipe."
    fi
    exit 1
fi

# Função para header
print_header() {
    if [ "$JSON_OUTPUT" = false ]; then
        echo -e "${BOLD}${PURPLE}📊 ANÁLISE DE FEEDBACK CDD${NC}"
        echo -e "${CYAN}Projeto: $(basename "$(pwd)")${NC}"
        echo -e "${BLUE}Período: $([ -n "$SINCE_DAYS" ] && echo "Últimos $SINCE_DAYS dias" || echo "Todos os feedbacks")${NC}"
        echo -e "${BLUE}Gerado em: $(date "+%Y-%m-%d %H:%M:%S")${NC}"
        echo "=========================================================="
    fi
}

# Coletar e processar dados
total_feedbacks=${#feedback_files[@]}
effectiveness_scores=()
productivity_scores=()
clarity_scores=()
ease_of_use_scores=()
time_investment_scores=()
tools_scores=()
documentation_quality_scores=()
team_alignment_scores=()
templates_scores=()
tracking_scores=()
patterns_scores=()
would_recommend_scores=()

pain_points=()
best_aspects=()
improvements=()
roles=()
experience_levels=()
onboarding_experiences=()
previous_methods=()
cdd_usage_frequency=()

# Processar cada arquivo de feedback
for file in "${feedback_files[@]}"; do
    # Extrair ratings
    effectiveness=$(extract_json_value "$file" ".ratings.effectiveness")
    [ "$effectiveness" != "N/A" ] && effectiveness_scores+=("$effectiveness")
    
    productivity=$(extract_json_value "$file" ".ratings.productivity")
    [ "$productivity" != "N/A" ] && productivity_scores+=("$productivity")
    
    clarity=$(extract_json_value "$file" ".ratings.clarity")
    [ "$clarity" != "N/A" ] && clarity_scores+=("$clarity")
    
    ease_of_use=$(extract_json_value "$file" ".ratings.ease_of_use")
    [ "$ease_of_use" != "N/A" ] && ease_of_use_scores+=("$ease_of_use")
    
    time_investment=$(extract_json_value "$file" ".ratings.time_investment")
    [ "$time_investment" != "N/A" ] && time_investment_scores+=("$time_investment")
    
    tools=$(extract_json_value "$file" ".ratings.tools")
    [ "$tools" != "N/A" ] && tools_scores+=("$tools")
    
    documentation_quality=$(extract_json_value "$file" ".ratings.documentation_quality")
    [ "$documentation_quality" != "N/A" ] && documentation_quality_scores+=("$documentation_quality")
    
    team_alignment=$(extract_json_value "$file" ".ratings.team_alignment")
    [ "$team_alignment" != "N/A" ] && team_alignment_scores+=("$team_alignment")
    
    templates=$(extract_json_value "$file" ".ratings.templates")
    [ "$templates" != "N/A" ] && templates_scores+=("$templates")
    
    tracking=$(extract_json_value "$file" ".ratings.tracking")
    [ "$tracking" != "N/A" ] && tracking_scores+=("$tracking")
    
    patterns=$(extract_json_value "$file" ".ratings.patterns")
    [ "$patterns" != "N/A" ] && patterns_scores+=("$patterns")
    
    would_recommend=$(extract_json_value "$file" ".ratings.would_recommend")
    [ "$would_recommend" != "N/A" ] && would_recommend_scores+=("$would_recommend")
    
    # Extrair dados qualitativos
    pain_point=$(extract_json_value "$file" ".qualitative.pain_point")
    [ "$pain_point" != "N/A" ] && pain_points+=("$pain_point")
    
    best_aspect=$(extract_json_value "$file" ".qualitative.best_aspect")
    [ "$best_aspect" != "N/A" ] && best_aspects+=("$best_aspect")
    
    improvement=$(extract_json_value "$file" ".qualitative.improvement")
    [ "$improvement" != "N/A" ] && improvements+=("$improvement")
    
    onboarding=$(extract_json_value "$file" ".qualitative.onboarding")
    [ "$onboarding" != "N/A" ] && onboarding_experiences+=("$onboarding")
    
    previous_method=$(extract_json_value "$file" ".qualitative.previous_method")
    [ "$previous_method" != "N/A" ] && previous_methods+=("$previous_method")
    
    # Extrair perfil
    role=$(extract_json_value "$file" ".profile.role")
    [ "$role" != "N/A" ] && roles+=("$role")
    
    experience=$(extract_json_value "$file" ".profile.experience")
    [ "$experience" != "N/A" ] && experience_levels+=("$experience")
    
    cdd_usage=$(extract_json_value "$file" ".profile.cdd_usage")
    [ "$cdd_usage" != "N/A" ] && cdd_usage_frequency+=("$cdd_usage")
done

# Calcular médias
avg_effectiveness=$(calculate_average "${effectiveness_scores[@]}")
avg_productivity=$(calculate_average "${productivity_scores[@]}")
avg_clarity=$(calculate_average "${clarity_scores[@]}")
avg_ease_of_use=$(calculate_average "${ease_of_use_scores[@]}")
avg_time_investment=$(calculate_average "${time_investment_scores[@]}")
avg_tools=$(calculate_average "${tools_scores[@]}")
avg_documentation_quality=$(calculate_average "${documentation_quality_scores[@]}")
avg_team_alignment=$(calculate_average "${team_alignment_scores[@]}")
avg_templates=$(calculate_average "${templates_scores[@]}")
avg_tracking=$(calculate_average "${tracking_scores[@]}")
avg_patterns=$(calculate_average "${patterns_scores[@]}")
avg_would_recommend=$(calculate_average "${would_recommend_scores[@]}")

# Calcular score geral
overall_metrics=(
    "$avg_effectiveness" "$avg_productivity" "$avg_clarity" 
    "$avg_ease_of_use" "$avg_time_investment"
)
overall_score=$(calculate_average "${overall_metrics[@]}")

# Determinar status geral
if [ $overall_score -ge 8 ]; then
    status="EXCELENTE"
    status_color="${GREEN}"
elif [ $overall_score -ge 7 ]; then
    status="MUITO_BOM"
    status_color="${GREEN}"
elif [ $overall_score -ge 6 ]; then
    status="BOM"
    status_color="${YELLOW}"
elif [ $overall_score -ge 5 ]; then
    status="REGULAR"
    status_color="${YELLOW}"
else
    status="PRECISA_MELHORAR"
    status_color="${RED}"
fi

# Saída dos resultados
if [ "$JSON_OUTPUT" = true ]; then
    # Preparar arrays JSON para pain points, etc.
    pain_points_json="["
    for i in "${!pain_points[@]}"; do
        [ $i -gt 0 ] && pain_points_json="$pain_points_json,"
        pain_points_json="$pain_points_json\"${pain_points[i]}\""
    done
    pain_points_json="$pain_points_json]"
    
    improvements_json="["
    for i in "${!improvements[@]}"; do
        [ $i -gt 0 ] && improvements_json="$improvements_json,"
        improvements_json="$improvements_json\"${improvements[i]}\""
    done
    improvements_json="$improvements_json]"
    
    cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "project": "$(basename "$(pwd)")",
  "analysis": {
    "total_feedbacks": $total_feedbacks,
    "period": $([ -n "$SINCE_DAYS" ] && echo "\"last_${SINCE_DAYS}_days\"" || echo "\"all_time\""),
    "overall_score": $overall_score,
    "status": "$status"
  },
  "ratings_average": {
    "effectiveness": $avg_effectiveness,
    "productivity": $avg_productivity,
    "clarity": $avg_clarity,
    "ease_of_use": $avg_ease_of_use,
    "time_investment": $avg_time_investment,
    "tools": $avg_tools,
    "documentation_quality": $avg_documentation_quality,
    "team_alignment": $avg_team_alignment,
    "templates": $avg_templates,
    "tracking": $avg_tracking,
    "patterns": $avg_patterns,
    "would_recommend": $avg_would_recommend
  },
  "qualitative": {
    "common_pain_points": $pain_points_json,
    "suggested_improvements": $improvements_json
  }
}
EOF
else
    # Saída em texto
    print_header
    
    echo ""
    echo -e "${BOLD}📈 RESUMO GERAL${NC}"
    echo "=========================================================="
    echo -e "📊 Total de feedbacks analisados: ${CYAN}$total_feedbacks${NC}"
    echo -e "🎯 Score geral: ${status_color}${BOLD}$overall_score/10${NC} ($status)"
    
    # Distribuição por score
    high_scores=$(count_occurrences "8\|9\|10" "${effectiveness_scores[@]}")
    medium_scores=$(count_occurrences "5\|6\|7" "${effectiveness_scores[@]}")
    low_scores=$(count_occurrences "1\|2\|3\|4" "${effectiveness_scores[@]}")
    
    echo ""
    echo -e "📊 Distribuição de satisfação:"
    echo -e "   ${GREEN}🟢 Alta (8-10): $high_scores feedbacks${NC}"
    echo -e "   ${YELLOW}🟡 Média (5-7): $medium_scores feedbacks${NC}"
    echo -e "   ${RED}🔴 Baixa (1-4): $low_scores feedbacks${NC}"
    
    # Métricas principais
    echo ""
    echo -e "${BOLD}🎯 MÉTRICAS PRINCIPAIS${NC}"
    echo "=========================================================="
    
    printf "%-25s ${CYAN}%2d/10${NC}\n" "Efetividade geral:" "$avg_effectiveness"
    printf "%-25s ${CYAN}%2d/10${NC}\n" "Aumento produtividade:" "$avg_productivity"
    
    if [ ${#clarity_scores[@]} -gt 0 ]; then
        printf "%-25s ${CYAN}%2d/10${NC}\n" "Clareza documentação:" "$avg_clarity"
        printf "%-25s ${CYAN}%2d/10${NC}\n" "Facilidade de uso:" "$avg_ease_of_use"
        printf "%-25s ${CYAN}%2d/10${NC}\n" "ROI tempo investido:" "$avg_time_investment"
    fi
    
    # Métricas de ferramentas
    if [ ${#tools_scores[@]} -gt 0 ]; then
        echo ""
        echo -e "${BOLD}🛠️  AVALIAÇÃO DE FERRAMENTAS${NC}"
        echo "=========================================================="
        
        printf "%-25s ${CYAN}%2d/10${NC}\n" "Scripts e ferramentas:" "$avg_tools"
        printf "%-25s ${CYAN}%2d/10${NC}\n" "Templates:" "$avg_templates"
        printf "%-25s ${CYAN}%2d/10${NC}\n" "Sistema de tracking:" "$avg_tracking"
        printf "%-25s ${CYAN}%2d/10${NC}\n" "Padrões de código:" "$avg_patterns"
        printf "%-25s ${CYAN}%2d/10${NC}\n" "Recomendaria para outros:" "$avg_would_recommend"
    fi
    
    # Análise qualitativa
    echo ""
    echo -e "${BOLD}💭 ANÁLISE QUALITATIVA${NC}"
    echo "=========================================================="
    
    # Pain points mais comuns
    echo -e "${RED}🔧 Principais dificuldades:${NC}"
    declare -A pain_point_count
    for pain in "${pain_points[@]}"; do
        # Agrupar pain points similares (implementação simplificada)
        if [[ "$pain" == *"tempo"* || "$pain" == *"lento"* ]]; then
            pain_point_count["Tempo/Velocidade"]=$((${pain_point_count["Tempo/Velocidade"]} + 1))
        elif [[ "$pain" == *"complexo"* || "$pain" == *"complicado"* ]]; then
            pain_point_count["Complexidade"]=$((${pain_point_count["Complexidade"]} + 1))
        elif [[ "$pain" == *"documentação"* || "$pain" == *"docs"* ]]; then
            pain_point_count["Documentação"]=$((${pain_point_count["Documentação"]} + 1))
        else
            pain_point_count["Outros"]=$((${pain_point_count["Outros"]} + 1))
        fi
    done
    
    for category in "${!pain_point_count[@]}"; do
        echo "  • $category: ${pain_point_count[$category]} menção(ões)"
    done
    
    # Aspectos mais valorizados
    echo ""
    echo -e "${GREEN}✨ Aspectos mais valorizados:${NC}"
    declare -A best_aspect_count
    for aspect in "${best_aspects[@]}"; do
        if [[ "$aspect" == *"organização"* || "$aspect" == *"estrutura"* ]]; then
            best_aspect_count["Organização/Estrutura"]=$((${best_aspect_count["Organização/Estrutura"]} + 1))
        elif [[ "$aspect" == *"clareza"* || "$aspect" == *"claro"* ]]; then
            best_aspect_count["Clareza"]=$((${best_aspect_count["Clareza"]} + 1))
        elif [[ "$aspect" == *"consistência"* || "$aspect" == *"padrão"* ]]; then
            best_aspect_count["Consistência"]=$((${best_aspect_count["Consistência"]} + 1))
        else
            best_aspect_count["Outros"]=$((${best_aspect_count["Outros"]} + 1))
        fi
    done
    
    for category in "${!best_aspect_count[@]}"; do
        echo "  • $category: ${best_aspect_count[$category]} menção(ões)"
    done
    
    # Perfil da equipe
    if [ ${#roles[@]} -gt 0 ]; then
        echo ""
        echo -e "${BOLD}👥 PERFIL DA EQUIPE${NC}"
        echo "=========================================================="
        
        declare -A role_count
        for role in "${roles[@]}"; do
            role_count["$role"]=$((${role_count["$role"]} + 1))
        done
        
        echo -e "${BLUE}Papéis:${NC}"
        for role in "${!role_count[@]}"; do
            echo "  • $role: ${role_count[$role]}"
        done
        
        if [ ${#experience_levels[@]} -gt 0 ]; then
            declare -A exp_count
            for exp in "${experience_levels[@]}"; do
                exp_count["$exp"]=$((${exp_count["$exp"]} + 1))
            done
            
            echo ""
            echo -e "${BLUE}Experiência:${NC}"
            for exp in "${!exp_count[@]}"; do
                echo "  • $exp: ${exp_count[$exp]}"
            done
        fi
    fi
    
    # Análise detalhada
    if [ "$DETAILED_OUTPUT" = true ]; then
        echo ""
        echo -e "${BOLD}📋 FEEDBACKS INDIVIDUAIS${NC}"
        echo "=========================================================="
        
        for i in "${!feedback_files[@]}"; do
            file="${feedback_files[i]}"
            filename=$(basename "$file")
            user=$(extract_json_value "$file" ".metadata.user")
            effectiveness=$(extract_json_value "$file" ".ratings.effectiveness")
            pain_point=$(extract_json_value "$file" ".qualitative.pain_point")
            
            echo -e "${CYAN}📄 Feedback $((i+1)):${NC}"
            echo "  Arquivo: $filename"
            echo "  Usuário: $user"
            echo "  Efetividade: $effectiveness/10"
            echo "  Principal dificuldade: $pain_point"
            echo ""
        done
    fi
    
    # Recomendações
    echo ""
    echo -e "${BOLD}🎯 RECOMENDAÇÕES${NC}"
    echo "=========================================================="
    
    if [ $avg_effectiveness -lt 6 ]; then
        echo -e "${RED}🚨 CRÍTICO: Efetividade baixa ($avg_effectiveness/10)${NC}"
        echo "  • Revisar fundamentalmente a implementação CDD"
        echo "  • Considerar workshop intensivo de onboarding"
        echo "  • Simplificar processos e ferramentas"
        echo ""
    elif [ $avg_effectiveness -lt 8 ]; then
        echo -e "${YELLOW}⚠️  ATENÇÃO: Efetividade moderada ($avg_effectiveness/10)${NC}"
        echo "  • Focar nos pain points mais mencionados"
        echo "  • Melhorar documentação e treinamento"
        echo "  • Automatizar mais processos"
        echo ""
    fi
    
    if [ $avg_time_investment -lt 6 ] && [ ${#time_investment_scores[@]} -gt 0 ]; then
        echo -e "${YELLOW}⏱️  ROI do tempo baixo ($avg_time_investment/10)${NC}"
        echo "  • Revisar tempo gasto vs benefícios"
        echo "  • Automatizar tarefas repetitivas"
        echo "  • Simplificar templates e processos"
        echo ""
    fi
    
    if [ $avg_tools -lt 7 ] && [ ${#tools_scores[@]} -gt 0 ]; then
        echo -e "${BLUE}🛠️  Melhorar ferramentas ($avg_tools/10)${NC}"
        echo "  • Revisar usabilidade dos scripts"
        echo "  • Adicionar mais automação"
        echo "  • Melhorar documentação das ferramentas"
        echo ""
    fi
    
    # Próximos passos
    echo ""
    echo -e "${BOLD}🚀 PRÓXIMOS PASSOS${NC}"
    echo "=========================================================="
    
    if [ $overall_score -ge 8 ]; then
        echo "🎉 CDD está funcionando muito bem!"
        echo "• Manter qualidade atual"
        echo "• Documentar boas práticas para replicação"
        echo "• Coletar feedback regularmente"
    elif [ $overall_score -ge 6 ]; then
        echo "📈 CDD tem potencial, mas precisa de ajustes:"
        echo "• Focar nos pain points identificados"
        echo "• Melhorar aspectos com scores baixos"
        echo "• Considerar treinamento adicional"
    else
        echo "🚨 CDD precisa de atenção urgente:"
        echo "• Revisar implementação completamente"
        echo "• Simplificar processos"
        echo "• Investir pesadamente em treinamento"
        echo "• Considerar consultoria especializada"
    fi
    
    echo ""
    echo -e "${BLUE}💡 Para melhorar continuamente:${NC}"
    echo "• Execute este script mensalmente"
    echo "• Colete feedback após mudanças importantes"
    echo "• Monitore tendências ao longo do tempo"
    echo "• Ajuste processos baseado no feedback"
fi 