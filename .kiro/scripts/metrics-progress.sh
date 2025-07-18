#!/bin/bash

# metrics-progress.sh - Análise de progresso das tarefas
# Uso: ./metrics-progress.sh [--json] [--detailed] [--feature <nome>]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Flags
JSON_OUTPUT=false
DETAILED_OUTPUT=false
SPECIFIC_FEATURE=""

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
        --feature)
            SPECIFIC_FEATURE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Uso: $0 [--json] [--detailed] [--feature <nome>]"
            echo ""
            echo "Opções:"
            echo "  --json               Saída em formato JSON"
            echo "  --detailed           Incluir detalhes sobre cada feature"
            echo "  --feature <nome>     Analisar apenas uma feature específica"
            echo "  -h                   Mostrar esta ajuda"
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
        echo -e "\n${PURPLE}📈 $1${NC}"
        echo "===================================="
    fi
}

print_metric() {
    local label="$1"
    local value="$2"
    local status="$3"  # success, warning, error, info
    
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
            "info")
                echo -e "${BLUE}ℹ️  $label: $value${NC}"
                ;;
            "progress")
                echo -e "${CYAN}📊 $label: $value${NC}"
                ;;
            *)
                echo -e "${BLUE}📊 $label: $value${NC}"
                ;;
        esac
    fi
}

print_progress_bar() {
    local percentage="$1"
    local width=20
    local filled=$((percentage * width / 100))
    local empty=$((width - filled))
    
    if [ "$JSON_OUTPUT" = false ]; then
        printf "["
        printf "%*s" $filled | tr ' ' '='
        printf "%*s" $empty | tr ' ' '-'
        printf "] %d%%\n" $percentage
    fi
}

# Função para extrair estimativa de tempo de uma string
extract_time_estimate() {
    local task_line="$1"
    
    # Buscar por padrões: (Xh), (XhY), (Xd), (X horas), etc.
    if echo "$task_line" | grep -qiE '\([0-9]+\s*(h|hora|horas|d|dia|dias|min|minuto|minutos)\)'; then
        estimate=$(echo "$task_line" | grep -oiE '\([0-9]+\s*(h|hora|horas|d|dia|dias|min|minuto|minutos)\)' | head -1)
        
        # Converter para horas
        if echo "$estimate" | grep -qiE '(d|dia|dias)'; then
            hours=$(echo "$estimate" | grep -oE '[0-9]+' | head -1)
            echo $((hours * 8))  # 8 horas por dia
        elif echo "$estimate" | grep -qiE '(min|minuto|minutos)'; then
            minutes=$(echo "$estimate" | grep -oE '[0-9]+' | head -1)
            echo $(((minutes + 59) / 60))  # Arredondar para cima
        else
            echo "$estimate" | grep -oE '[0-9]+' | head -1
        fi
    else
        echo "0"
    fi
}

# Função para analisar uma feature específica
analyze_feature() {
    local feature_dir="$1"
    local feature_name=$(basename "$feature_dir")
    
    if [ ! -f "$feature_dir/tasks.md" ]; then
        return
    fi
    
    # Contar tarefas
    local total_tasks=$(grep -c "^-\s\[" "$feature_dir/tasks.md" 2>/dev/null || echo "0")
    local completed_tasks=$(grep -c "^-\s\[x\]" "$feature_dir/tasks.md" 2>/dev/null || echo "0")
    local pending_tasks=$((total_tasks - completed_tasks))
    
    # Calcular progresso
    local progress_percent=0
    if [ $total_tasks -gt 0 ]; then
        progress_percent=$((completed_tasks * 100 / total_tasks))
    fi
    
    # Calcular estimativas de tempo
    local total_estimated=0
    local completed_estimated=0
    local pending_estimated=0
    
    while IFS= read -r line; do
        if echo "$line" | grep -q "^-\s\["; then
            estimate=$(extract_time_estimate "$line")
            total_estimated=$((total_estimated + estimate))
            
            if echo "$line" | grep -q "^-\s\[x\]"; then
                completed_estimated=$((completed_estimated + estimate))
            else
                pending_estimated=$((pending_estimated + estimate))
            fi
        fi
    done < "$feature_dir/tasks.md"
    
    # Detectar fase atual
    local current_phase=""
    local phases=()
    
    while IFS= read -r line; do
        if echo "$line" | grep -qE "^#{1,3}\s+"; then
            phase=$(echo "$line" | sed 's/^#{1,3}\s*//' | sed 's/:.*$//')
            phases+=("$phase")
            
            # Se há tarefas pendentes nesta fase, é a fase atual
            if [ -z "$current_phase" ]; then
                phase_has_pending=false
                while IFS= read -r task_line; do
                    if echo "$task_line" | grep -q "^-\s\[\s\]"; then
                        phase_has_pending=true
                        break
                    elif echo "$task_line" | grep -qE "^#{1,3}\s+"; then
                        break
                    fi
                done < <(grep -A 100 "$line" "$feature_dir/tasks.md")
                
                if [ "$phase_has_pending" = true ]; then
                    current_phase="$phase"
                fi
            fi
        fi
    done < "$feature_dir/tasks.md"
    
    # Se todas as tarefas estão completas
    if [ $pending_tasks -eq 0 ] && [ $total_tasks -gt 0 ]; then
        current_phase="Completa"
    elif [ -z "$current_phase" ] && [ ${#phases[@]} -gt 0 ]; then
        current_phase="${phases[0]}"
    fi
    
    # Detectar tarefas atrasadas (sem critério específico definido, usar placeholder)
    local overdue_tasks=0
    
    # Calcular velocidade (tarefas por semana)
    local velocity=0
    
    # Estimar tempo restante
    local estimated_weeks=0
    if [ $velocity -gt 0 ] && [ $pending_tasks -gt 0 ]; then
        estimated_weeks=$((pending_tasks / velocity))
    fi
    
    # Armazenar dados da feature
    echo "${feature_name}|${total_tasks}|${completed_tasks}|${pending_tasks}|${progress_percent}|${total_estimated}|${completed_estimated}|${pending_estimated}|${current_phase}|${overdue_tasks}|${velocity}|${estimated_weeks}"
}

# Coletar dados de todas as features
features_data=()
total_features=0
completed_features=0
total_all_tasks=0
completed_all_tasks=0
pending_all_tasks=0
total_all_estimated=0
completed_all_estimated=0
pending_all_estimated=0

for spec_dir in .kiro/specs/*/; do
    if [ -d "$spec_dir" ] && [ "$(basename "$spec_dir")" != "_template" ]; then
        feature_name=$(basename "$spec_dir")
        
        # Se feature específica foi solicitada, pular outras
        if [ -n "$SPECIFIC_FEATURE" ] && [ "$feature_name" != "$SPECIFIC_FEATURE" ]; then
            continue
        fi
        
        if [ -f "$spec_dir/tasks.md" ]; then
            feature_data=$(analyze_feature "$spec_dir")
            features_data+=("$feature_data")
            
            # Extrair dados para totais
            IFS='|' read -r fname ftotal fcompleted fpending fprogress ftotal_est fcompleted_est fpending_est fphase foverdue fvelocity festimated <<< "$feature_data"
            
            total_features=$((total_features + 1))
            total_all_tasks=$((total_all_tasks + ftotal))
            completed_all_tasks=$((completed_all_tasks + fcompleted))
            pending_all_tasks=$((pending_all_tasks + fpending))
            total_all_estimated=$((total_all_estimated + ftotal_est))
            completed_all_estimated=$((completed_all_estimated + fcompleted_est))
            pending_all_estimated=$((pending_all_estimated + fpending_est))
            
            if [ $fpending -eq 0 ] && [ $ftotal -gt 0 ]; then
                completed_features=$((completed_features + 1))
            fi
        fi
    fi
done

# Calcular métricas globais
overall_progress=0
if [ $total_all_tasks -gt 0 ]; then
    overall_progress=$((completed_all_tasks * 100 / total_all_tasks))
fi

feature_completion_rate=0
if [ $total_features -gt 0 ]; then
    feature_completion_rate=$((completed_features * 100 / total_features))
fi

# Detectar tendências (simulado por agora)
recent_commits=0
if [ -d ".git" ]; then
    recent_commits=$(git log --since="1 week ago" --oneline 2>/dev/null | wc -l || echo "0")
fi

doc_updates=0
if [ -d ".git" ]; then
    doc_updates=$(git log --since="1 week ago" --oneline -- .kiro/ 2>/dev/null | wc -l || echo "0")
fi

# Saída dos resultados
if [ "$JSON_OUTPUT" = true ]; then
    # Preparar array JSON das features
    features_json="["
    first=true
    
    for feature_data in "${features_data[@]}"; do
        IFS='|' read -r fname ftotal fcompleted fpending fprogress ftotal_est fcompleted_est fpending_est fphase foverdue fvelocity festimated <<< "$feature_data"
        
        if [ "$first" = false ]; then
            features_json="$features_json,"
        fi
        first=false
        
        features_json="$features_json{
      \"name\": \"$fname\",
      \"tasks\": {
        \"total\": $ftotal,
        \"completed\": $fcompleted,
        \"pending\": $fpending,
        \"progress_percentage\": $fprogress
      },
      \"estimates\": {
        \"total_hours\": $ftotal_est,
        \"completed_hours\": $fcompleted_est,
        \"pending_hours\": $fpending_est
      },
      \"status\": {
        \"current_phase\": \"$fphase\",
        \"overdue_tasks\": $foverdue,
        \"velocity\": $fvelocity,
        \"estimated_weeks\": $festimated
      }
    }"
    done
    
    features_json="$features_json]"
    
    # Saída JSON completa
    cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "project": "$(basename "$(pwd)")",
  "summary": {
    "features": {
      "total": $total_features,
      "completed": $completed_features,
      "completion_rate": $feature_completion_rate
    },
    "tasks": {
      "total": $total_all_tasks,
      "completed": $completed_all_tasks,
      "pending": $pending_all_tasks,
      "progress_percentage": $overall_progress
    },
    "estimates": {
      "total_hours": $total_all_estimated,
      "completed_hours": $completed_all_estimated,
      "pending_hours": $pending_all_estimated
    },
    "activity": {
      "recent_commits": $recent_commits,
      "doc_updates": $doc_updates
    }
  },
  "features": $features_json
}
EOF
else
    # Saída em texto
    if [ -n "$SPECIFIC_FEATURE" ]; then
        print_header "PROGRESSO DA FEATURE: $SPECIFIC_FEATURE"
    else
        print_header "PROGRESSO GERAL DO PROJETO"
    fi
    
    echo "📊 Resumo executivo:"
    print_metric "Features totais" "$total_features" "info"
    print_metric "Features completas" "$completed_features" "$([ $completed_features -eq $total_features ] && [ $total_features -gt 0 ] && echo "success" || echo "info")"
    print_metric "Taxa de conclusão de features" "$feature_completion_rate%" "$([ $feature_completion_rate -ge 80 ] && echo "success" || [ $feature_completion_rate -ge 50 ] && echo "warning" || echo "error")"
    
    echo ""
    echo "✅ Tarefas:"
    print_metric "Total de tarefas" "$total_all_tasks" "info"
    print_metric "Tarefas concluídas" "$completed_all_tasks" "success"
    print_metric "Tarefas pendentes" "$pending_all_tasks" "$([ $pending_all_tasks -eq 0 ] && echo "success" || echo "info")"
    print_metric "Progresso geral" "$overall_progress%" "$([ $overall_progress -ge 80 ] && echo "success" || [ $overall_progress -ge 50 ] && echo "warning" || echo "error")"
    
    if [ "$JSON_OUTPUT" = false ]; then
        echo -n "Progresso visual: "
        print_progress_bar $overall_progress
    fi
    
    if [ $total_all_estimated -gt 0 ]; then
        echo ""
        echo "⏱️  Estimativas de tempo:"
        print_metric "Total estimado" "${total_all_estimated}h" "info"
        print_metric "Tempo completado" "${completed_all_estimated}h" "success"
        print_metric "Tempo restante estimado" "${pending_all_estimated}h" "info"
        
        if [ $total_all_estimated -gt 0 ]; then
            time_progress=$((completed_all_estimated * 100 / total_all_estimated))
            print_metric "Progresso por tempo" "$time_progress%" "$([ $time_progress -ge 80 ] && echo "success" || [ $time_progress -ge 50 ] && echo "warning" || echo "error")"
        fi
    fi
    
    echo ""
    echo "🔄 Atividade recente:"
    print_metric "Commits esta semana" "$recent_commits" "$([ $recent_commits -gt 5 ] && echo "success" || [ $recent_commits -gt 0 ] && echo "warning" || echo "error")"
    print_metric "Atualizações de documentação" "$doc_updates" "$([ $doc_updates -gt 0 ] && echo "success" || echo "warning")"
    
    # Detalhamento por feature
    if [ "$DETAILED_OUTPUT" = true ] || [ -n "$SPECIFIC_FEATURE" ]; then
        print_header "DETALHAMENTO POR FEATURE"
        
        for feature_data in "${features_data[@]}"; do
            IFS='|' read -r fname ftotal fcompleted fpending fprogress ftotal_est fcompleted_est fpending_est fphase foverdue fvelocity festimated <<< "$feature_data"
            
            echo ""
            echo -e "${CYAN}🎯 Feature: $fname${NC}"
            print_metric "Progresso" "$fcompleted/$ftotal tarefas ($fprogress%)" "$([ $fprogress -eq 100 ] && echo "success" || [ $fprogress -ge 50 ] && echo "warning" || echo "error")"
            
            if [ "$JSON_OUTPUT" = false ]; then
                echo -n "  Progresso visual: "
                print_progress_bar $fprogress
            fi
            
            if [ "$fphase" != "" ]; then
                print_metric "Fase atual" "$fphase" "info"
            fi
            
            if [ $ftotal_est -gt 0 ]; then
                print_metric "Tempo estimado" "${fpending_est}h restantes de ${ftotal_est}h totais" "info"
            fi
            
            if [ $foverdue -gt 0 ]; then
                print_metric "Tarefas atrasadas" "$foverdue" "warning"
            fi
        done
    fi
    
    # Insights e recomendações
    print_header "INSIGHTS E RECOMENDAÇÕES"
    
    if [ $overall_progress -ge 80 ]; then
        echo -e "${GREEN}🎉 Projeto próximo da conclusão! Foque na finalização.${NC}"
    elif [ $overall_progress -ge 50 ]; then
        echo -e "${YELLOW}📈 Projeto em andamento. Mantenha o ritmo.${NC}"
    elif [ $overall_progress -ge 20 ]; then
        echo -e "${YELLOW}🚀 Projeto iniciado. Considere acelerar o desenvolvimento.${NC}"
    else
        echo -e "${RED}⚠️  Projeto pouco avançado. Revise prioridades e recursos.${NC}"
    fi
    
    echo ""
    
    if [ $recent_commits -eq 0 ]; then
        echo "🔄 Nenhum commit esta semana - considere aumentar atividade"
    elif [ $recent_commits -gt 10 ]; then
        echo "🔥 Alta atividade de desenvolvimento - excelente!"
    fi
    
    if [ $doc_updates -eq 0 ]; then
        echo "📚 Documentação não atualizada esta semana - mantenha docs sincronizados"
    fi
    
    if [ $pending_all_estimated -gt 0 ] && [ $completed_all_estimated -gt 0 ]; then
        weeks_remaining=$((pending_all_estimated / 40))  # 40h por semana
        if [ $weeks_remaining -gt 0 ]; then
            echo "📅 Estimativa: aproximadamente $weeks_remaining semana(s) restantes"
        fi
    fi
    
    # Comando para marcar progresso
    echo ""
    print_header "AÇÕES RÁPIDAS"
    echo "Para marcar tarefas como concluídas:"
    echo "  cd .kiro/scripts && npm run complete <task-id>"
    echo ""
    echo "Para ver tarefas de uma feature específica:"
    echo "  $0 --feature <nome-da-feature> --detailed"
fi 