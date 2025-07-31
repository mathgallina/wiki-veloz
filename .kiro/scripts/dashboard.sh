#!/bin/bash

# dashboard.sh - Dashboard básico de métricas CDD
# Uso: ./dashboard.sh [--refresh-interval <seconds>] [--compact]

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
REFRESH_INTERVAL=0
COMPACT_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --refresh-interval)
            REFRESH_INTERVAL="$2"
            shift 2
            ;;
        --compact)
            COMPACT_MODE=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [--refresh-interval <seconds>] [--compact]"
            echo ""
            echo "Opções:"
            echo "  --refresh-interval <n>   Atualizar a cada N segundos (0 = sem refresh)"
            echo "  --compact               Modo compacto (menos detalhes)"
            echo "  -h                      Mostrar esta ajuda"
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

# Função para limpar tela
clear_screen() {
    if [ $REFRESH_INTERVAL -gt 0 ]; then
        clear
    fi
}

# Função para exibir header
print_header() {
    local title="$1"
    echo -e "${BOLD}${PURPLE}📊 CDD DASHBOARD${NC}"
    echo -e "${CYAN}Projeto: $(basename "$(pwd)")${NC}"
    echo -e "${BLUE}Última atualização: $(date "+%Y-%m-%d %H:%M:%S")${NC}"
    echo "================================================="
}

# Função para exibir barra de progresso colorida
print_colored_progress_bar() {
    local percentage="$1"
    local width=20
    local filled=$((percentage * width / 100))
    local empty=$((width - filled))
    
    # Definir cor baseada na porcentagem
    local color=""
    if [ $percentage -ge 80 ]; then
        color="${GREEN}"
    elif [ $percentage -ge 50 ]; then
        color="${YELLOW}"
    else
        color="${RED}"
    fi
    
    printf "${color}["
    printf "%*s" $filled | tr ' ' '█'
    printf "%*s" $empty | tr ' ' '░'
    printf "]${NC} %d%%" $percentage
}

# Função para coletar métricas rapidamente
collect_metrics() {
    # Progresso geral
    total_tasks=$(find .kiro/specs -name "tasks.md" -exec grep -c "^-\s\[" {} \; 2>/dev/null | awk '{s+=$1} END {print s+0}')
    completed_tasks=$(find .kiro/specs -name "tasks.md" -exec grep -c "^-\s\[x\]" {} \; 2>/dev/null | awk '{s+=$1} END {print s+0}')
    
    if [ $total_tasks -gt 0 ]; then
        progress=$((completed_tasks * 100 / total_tasks))
    else
        progress=0
    fi
    
    # Features
    total_features=$(find .kiro/specs -mindepth 1 -maxdepth 1 -type d | grep -v "_template" | wc -l)
    completed_features=0
    
    for spec_dir in .kiro/specs/*/; do
        if [ -d "$spec_dir" ] && [ "$(basename "$spec_dir")" != "_template" ]; then
            if [ -f "$spec_dir/tasks.md" ]; then
                pending_in_feature=$(grep -c "^-\s\[\s\]" "$spec_dir/tasks.md" 2>/dev/null || echo "1")
                if [ $pending_in_feature -eq 0 ]; then
                    total_in_feature=$(grep -c "^-\s\[" "$spec_dir/tasks.md" 2>/dev/null || echo "0")
                    if [ $total_in_feature -gt 0 ]; then
                        completed_features=$((completed_features + 1))
                    fi
                fi
            fi
        fi
    done
    
    # Qualidade da documentação
    total_docs=$(find .kiro -name "*.md" | wc -l)
    docs_with_placeholders=$(find .kiro -name "*.md" -exec grep -l "\[.*\]" {} \; 2>/dev/null | grep -v "_template" | wc -l)
    docs_with_todos=$(find .kiro -name "*.md" -exec grep -l "TODO\|FIXME\|XXX" {} \; 2>/dev/null | wc -l)
    
    if [ $total_docs -gt 0 ]; then
        doc_quality=$(((total_docs - docs_with_placeholders - docs_with_todos) * 100 / total_docs))
        if [ $doc_quality -lt 0 ]; then
            doc_quality=0
        fi
    else
        doc_quality=100
    fi
    
    # Atividade recente
    recent_commits=0
    if [ -d ".git" ]; then
        recent_commits=$(git log --since="1 week ago" --oneline 2>/dev/null | wc -l || echo "0")
    fi
    
    # Verificar configurações de qualidade
    quality_score=0
    quality_checks=0
    
    # TypeScript
    if [ -f "tsconfig.json" ]; then
        quality_score=$((quality_score + 1))
    fi
    quality_checks=$((quality_checks + 1))
    
    # ESLint
    if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ]; then
        quality_score=$((quality_score + 1))
    fi
    quality_checks=$((quality_checks + 1))
    
    # Package.json
    if [ -f "package.json" ]; then
        quality_score=$((quality_score + 1))
    fi
    quality_checks=$((quality_checks + 1))
    
    # Git
    if [ -d ".git" ]; then
        quality_score=$((quality_score + 1))
    fi
    quality_checks=$((quality_checks + 1))
    
    quality_percentage=$((quality_score * 100 / quality_checks))
}

# Função para exibir métricas principais
show_main_metrics() {
    echo ""
    echo -e "${BOLD}🎯 PROGRESSO GERAL${NC}"
    echo "────────────────────────────────────────────────"
    
    printf "%-20s " "Tarefas:"
    print_colored_progress_bar $progress
    echo " ($completed_tasks/$total_tasks)"
    
    if [ $total_features -gt 0 ]; then
        feature_progress=$((completed_features * 100 / total_features))
        printf "%-20s " "Features:"
        print_colored_progress_bar $feature_progress
        echo " ($completed_features/$total_features)"
    fi
    
    printf "%-20s " "Qualidade docs:"
    print_colored_progress_bar $doc_quality
    echo ""
    
    printf "%-20s " "Configuração:"
    print_colored_progress_bar $quality_percentage
    echo " ($quality_score/$quality_checks)"
}

# Função para exibir detalhes por feature
show_feature_details() {
    if [ "$COMPACT_MODE" = true ]; then
        return
    fi
    
    echo ""
    echo -e "${BOLD}🎯 FEATURES INDIVIDUAIS${NC}"
    echo "────────────────────────────────────────────────"
    
    for spec_dir in .kiro/specs/*/; do
        if [ -d "$spec_dir" ] && [ "$(basename "$spec_dir")" != "_template" ]; then
            feature_name=$(basename "$spec_dir")
            
            if [ -f "$spec_dir/tasks.md" ]; then
                feature_total=$(grep -c "^-\s\[" "$spec_dir/tasks.md" 2>/dev/null || echo "0")
                feature_completed=$(grep -c "^-\s\[x\]" "$spec_dir/tasks.md" 2>/dev/null || echo "0")
                
                if [ $feature_total -gt 0 ]; then
                    feature_progress=$((feature_completed * 100 / feature_total))
                    
                    printf "%-15s " "$feature_name:"
                    print_colored_progress_bar $feature_progress
                    echo " ($feature_completed/$feature_total)"
                else
                    printf "%-15s ${YELLOW}⚠️  Sem tarefas definidas${NC}\n" "$feature_name:"
                fi
            else
                printf "%-15s ${RED}❌ tasks.md não encontrado${NC}\n" "$feature_name:"
            fi
        fi
    done
}

# Função para exibir alertas e avisos
show_alerts() {
    echo ""
    echo -e "${BOLD}⚠️  ALERTAS E AVISOS${NC}"
    echo "────────────────────────────────────────────────"
    
    alerts_found=false
    
    # Verificar documentação incompleta
    if [ $docs_with_placeholders -gt 0 ]; then
        echo -e "${YELLOW}📝 $docs_with_placeholders arquivo(s) com placeholders não substituídos${NC}"
        alerts_found=true
    fi
    
    if [ $docs_with_todos -gt 0 ]; then
        echo -e "${YELLOW}✅ $docs_with_todos arquivo(s) com TODOs pendentes${NC}"
        alerts_found=true
    fi
    
    # Verificar atividade
    if [ $recent_commits -eq 0 ]; then
        echo -e "${RED}🔄 Nenhum commit na última semana${NC}"
        alerts_found=true
    fi
    
    # Verificar features sem progresso
    stalled_features=0
    for spec_dir in .kiro/specs/*/; do
        if [ -d "$spec_dir" ] && [ "$(basename "$spec_dir")" != "_template" ]; then
            if [ -f "$spec_dir/tasks.md" ]; then
                feature_completed=$(grep -c "^-\s\[x\]" "$spec_dir/tasks.md" 2>/dev/null || echo "0")
                feature_total=$(grep -c "^-\s\[" "$spec_dir/tasks.md" 2>/dev/null || echo "0")
                
                if [ $feature_total -gt 0 ] && [ $feature_completed -eq 0 ]; then
                    stalled_features=$((stalled_features + 1))
                fi
            fi
        fi
    done
    
    if [ $stalled_features -gt 0 ]; then
        echo -e "${YELLOW}🚧 $stalled_features feature(s) sem progresso${NC}"
        alerts_found=true
    fi
    
    # Verificar configurações ausentes
    if [ $quality_percentage -lt 75 ]; then
        echo -e "${YELLOW}⚙️  Configurações de projeto incompletas${NC}"
        alerts_found=true
    fi
    
    if [ "$alerts_found" = false ]; then
        echo -e "${GREEN}🎉 Nenhum alerta! Projeto em boa forma.${NC}"
    fi
}

# Função para exibir estatísticas rápidas
show_quick_stats() {
    echo ""
    echo -e "${BOLD}📈 ESTATÍSTICAS RÁPIDAS${NC}"
    echo "────────────────────────────────────────────────"
    
    echo -e "📊 Total de tarefas: ${CYAN}$total_tasks${NC}"
    echo -e "✅ Tarefas completas: ${GREEN}$completed_tasks${NC}"
    echo -e "📋 Tarefas pendentes: ${YELLOW}$((total_tasks - completed_tasks))${NC}"
    echo -e "🎯 Features ativas: ${BLUE}$total_features${NC}"
    echo -e "🔄 Commits (7 dias): ${CYAN}$recent_commits${NC}"
    
    if [ $total_tasks -gt 0 ] && [ $completed_tasks -gt 0 ]; then
        avg_completion_rate=$((completed_tasks * 100 / total_tasks))
        echo -e "📈 Taxa de conclusão: ${GREEN}$avg_completion_rate%${NC}"
    fi
    
    # Estimar tempo restante (assumindo 5 tarefas por semana)
    if [ $total_tasks -gt $completed_tasks ]; then
        remaining_tasks=$((total_tasks - completed_tasks))
        estimated_weeks=$((remaining_tasks / 5))
        if [ $estimated_weeks -eq 0 ]; then
            estimated_weeks=1
        fi
        echo -e "⏱️  Estimativa: ${YELLOW}~$estimated_weeks semana(s)${NC}"
    fi
}

# Função para exibir comandos úteis
show_quick_actions() {
    if [ "$COMPACT_MODE" = true ]; then
        return
    fi
    
    echo ""
    echo -e "${BOLD}🚀 AÇÕES RÁPIDAS${NC}"
    echo "────────────────────────────────────────────────"
    echo "📋 Ver progresso detalhado: ./metrics-progress.sh --detailed"
    echo "🔍 Analisar qualidade: ./metrics-code-quality.sh"
    echo "📊 Análise completa: ./full-dashboard.sh"
    echo "✅ Marcar tarefa: npm run complete <task-id>"
    echo "🏗️  Nova feature: ./new-feature.sh <nome>"
    echo "🔧 Validar projeto: ./validate-project.sh"
}

# Função principal do dashboard
main_dashboard() {
    clear_screen
    collect_metrics
    print_header
    show_main_metrics
    show_feature_details
    show_alerts
    show_quick_stats
    show_quick_actions
    
    if [ $REFRESH_INTERVAL -gt 0 ]; then
        echo ""
        echo -e "${BLUE}🔄 Atualizando em $REFRESH_INTERVAL segundos... (Ctrl+C para sair)${NC}"
    fi
}

# Loop principal
if [ $REFRESH_INTERVAL -gt 0 ]; then
    # Modo contínuo
    trap 'echo -e "\n${YELLOW}Dashboard finalizado.${NC}"; exit 0' INT
    
    while true; do
        main_dashboard
        sleep $REFRESH_INTERVAL
    done
else
    # Execução única
    main_dashboard
fi 