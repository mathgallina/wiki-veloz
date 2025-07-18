#!/bin/bash

# collect-feedback.sh - Coleta estruturada de feedback sobre CDD
# Uso: ./collect-feedback.sh [--quick] [--anonymous]

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
QUICK_MODE=false
ANONYMOUS_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --anonymous)
            ANONYMOUS_MODE=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [--quick] [--anonymous]"
            echo ""
            echo "Opções:"
            echo "  --quick      Coleta rápida (apenas perguntas essenciais)"
            echo "  --anonymous  Feedback anônimo (sem identificação do usuário)"
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

# Criar diretório de feedback
mkdir -p "$FEEDBACK_DIR"

# Função para validar entrada numérica
validate_numeric() {
    local input="$1"
    local min="$2"
    local max="$3"
    
    if [[ "$input" =~ ^[0-9]+$ ]] && [ "$input" -ge "$min" ] && [ "$input" -le "$max" ]; then
        return 0
    else
        return 1
    fi
}

# Função para fazer pergunta com validação
ask_question() {
    local question="$1"
    local type="$2"  # text, numeric, scale, choice
    local options="$3"  # Para numeric: "min:max", para choice: "opt1,opt2,opt3"
    local response=""
    
    while true; do
        echo -e "\n${CYAN}$question${NC}"
        
        case $type in
            "scale")
                echo -e "${BLUE}(Escala de 1-10, onde 1 = muito ruim, 10 = excelente)${NC}"
                read -p "Resposta (1-10): " response
                if validate_numeric "$response" 1 10; then
                    break
                else
                    echo -e "${RED}❌ Por favor, digite um número entre 1 e 10${NC}"
                fi
                ;;
            "numeric")
                IFS=':' read -r min max <<< "$options"
                echo -e "${BLUE}(Número entre $min e $max)${NC}"
                read -p "Resposta ($min-$max): " response
                if validate_numeric "$response" "$min" "$max"; then
                    break
                else
                    echo -e "${RED}❌ Por favor, digite um número entre $min e $max${NC}"
                fi
                ;;
            "choice")
                echo -e "${BLUE}Opções: $options${NC}"
                echo -e "${BLUE}Digite o número da opção ou a resposta completa${NC}"
                IFS=',' read -ra CHOICES <<< "$options"
                for i in "${!CHOICES[@]}"; do
                    echo "  $((i+1)). ${CHOICES[i]}"
                done
                read -p "Resposta: " response
                
                # Verificar se é um número válido
                if validate_numeric "$response" 1 "${#CHOICES[@]}"; then
                    response="${CHOICES[$((response-1))]}"
                    break
                elif [[ ",$options," =~ ",$response," ]]; then
                    break
                else
                    echo -e "${RED}❌ Por favor, escolha uma opção válida${NC}"
                fi
                ;;
            "text")
                read -p "Resposta: " response
                if [ -n "$response" ]; then
                    break
                else
                    echo -e "${RED}❌ Por favor, forneça uma resposta${NC}"
                fi
                ;;
        esac
    done
    
    echo "$response"
}

# Header
echo -e "${BOLD}${PURPLE}📝 COLETA DE FEEDBACK - CDD${NC}"
echo -e "${CYAN}Projeto: $(basename "$(pwd)")${NC}"
echo -e "${BLUE}Data: $(date "+%Y-%m-%d %H:%M:%S")${NC}"
echo "=========================================================="

echo -e "\n${YELLOW}💭 Seu feedback é importante para melhorar a metodologia CDD!${NC}"
echo -e "${BLUE}Todas as respostas serão usadas para evolução contínua do processo.${NC}"

# Coletar informações do usuário
user_info=""
if [ "$ANONYMOUS_MODE" = false ]; then
    if git config user.name >/dev/null 2>&1; then
        git_user=$(git config user.name)
        echo -e "\n${BLUE}Usuário detectado: $git_user${NC}"
        read -p "Confirma este nome? (s/n): " confirm
        
        if [[ "$confirm" =~ ^[Ss]$ ]]; then
            user_info="$git_user"
        else
            user_info=$(ask_question "Como você gostaria de ser identificado?" "text")
        fi
    else
        user_info=$(ask_question "Como você gostaria de ser identificado?" "text")
    fi
else
    user_info="anonymous_$(date +%s)"
fi

# Coleta de feedback
echo -e "\n${BOLD}📊 PERGUNTAS SOBRE EFETIVIDADE${NC}"

effectiveness=$(ask_question "1. Como você avalia a efetividade geral do CDD?" "scale")

productivity=$(ask_question "2. O CDD aumentou sua produtividade?" "scale")

if [ "$QUICK_MODE" = false ]; then
    clarity=$(ask_question "3. A documentação CDD está clara e útil?" "scale")
    
    ease_of_use=$(ask_question "4. Quão fácil é seguir os processos CDD?" "scale")
    
    time_investment=$(ask_question "5. O tempo investido em documentação vale a pena?" "scale")
fi

# Feedback qualitativo
echo -e "\n${BOLD}💭 FEEDBACK QUALITATIVO${NC}"

pain_point=$(ask_question "6. Qual é o maior ponto de dor ou dificuldade com CDD?" "text")

best_aspect=$(ask_question "7. Qual o melhor aspecto do CDD?" "text")

improvement=$(ask_question "8. Que melhoria você sugere para o CDD?" "text")

if [ "$QUICK_MODE" = false ]; then
    # Perguntas específicas
    echo -e "\n${BOLD}🎯 ASPECTOS ESPECÍFICOS${NC}"
    
    onboarding=$(ask_question "9. Como foi sua experiência de onboarding com CDD?" "choice" "Excelente,Boa,Regular,Ruim,Não tive onboarding formal")
    
    tools=$(ask_question "10. As ferramentas/scripts CDD são úteis?" "scale")
    
    documentation_quality=$(ask_question "11. A qualidade da documentação produzida melhorou?" "scale")
    
    team_alignment=$(ask_question "12. O CDD melhorou o alinhamento da equipe?" "scale")
    
    # Feedback sobre features específicas
    echo -e "\n${BOLD}🔧 FEATURES ESPECÍFICAS${NC}"
    
    templates=$(ask_question "13. Os templates são úteis e bem estruturados?" "scale")
    
    tracking=$(ask_question "14. O sistema de tracking de tarefas é eficaz?" "scale")
    
    patterns=$(ask_question "15. Os padrões de código ajudam na consistência?" "scale")
    
    # Comparação com métodos anteriores
    previous_method=$(ask_question "16. Que método você usava antes do CDD?" "choice" "Documentação ad-hoc,Wikis,Comentários no código,Comunicação verbal,Outro")
    
    would_recommend=$(ask_question "17. Você recomendaria CDD para outras equipes?" "scale")
fi

# Categorizar o tipo de usuário
echo -e "\n${BOLD}👤 PERFIL DO USUÁRIO${NC}"

role=$(ask_question "18. Qual seu papel principal no projeto?" "choice" "Desenvolvedor Senior,Desenvolvedor Junior,Tech Lead,Product Manager,Designer,QA,Outro")

experience=$(ask_question "19. Há quanto tempo trabalha com desenvolvimento?" "choice" "< 1 ano,1-3 anos,3-5 anos,5-10 anos,> 10 anos")

if [ "$QUICK_MODE" = false ]; then
    cdd_usage=$(ask_question "20. Com que frequência você usa documentação CDD?" "choice" "Diariamente,Algumas vezes por semana,Semanalmente,Raramente,Nunca")
fi

# Salvar feedback
timestamp=$(date -Iseconds)
feedback_file="$FEEDBACK_DIR/feedback_$(date +%Y%m%d_%H%M%S)_${user_info// /_}.json"

# Construir JSON
cat > "$feedback_file" << EOF
{
  "metadata": {
    "timestamp": "$timestamp",
    "user": "$user_info",
    "project": "$(basename "$(pwd)")",
    "quick_mode": $QUICK_MODE,
    "anonymous": $ANONYMOUS_MODE,
    "version": "1.0"
  },
  "ratings": {
    "effectiveness": $effectiveness,
    "productivity": $productivity$([ "$QUICK_MODE" = false ] && echo ",
    \"clarity\": $clarity,
    \"ease_of_use\": $ease_of_use,
    \"time_investment\": $time_investment,
    \"tools\": $tools,
    \"documentation_quality\": $documentation_quality,
    \"team_alignment\": $team_alignment,
    \"templates\": $templates,
    \"tracking\": $tracking,
    \"patterns\": $patterns,
    \"would_recommend\": $would_recommend")
  },
  "qualitative": {
    "pain_point": "$pain_point",
    "best_aspect": "$best_aspect",
    "improvement": "$improvement"$([ "$QUICK_MODE" = false ] && echo ",
    \"onboarding\": \"$onboarding\",
    \"previous_method\": \"$previous_method\"")
  },
  "profile": {
    "role": "$role",
    "experience": "$experience"$([ "$QUICK_MODE" = false ] && echo ",
    \"cdd_usage\": \"$cdd_usage\"")
  }
}
EOF

# Resumo e confirmação
echo -e "\n${BOLD}📄 RESUMO DO FEEDBACK${NC}"
echo "=========================================================="
echo -e "👤 Usuário: ${CYAN}$user_info${NC}"
echo -e "📊 Efetividade geral: ${CYAN}$effectiveness/10${NC}"
echo -e "⚡ Produtividade: ${CYAN}$productivity/10${NC}"
echo -e "🔧 Principal dificuldade: ${CYAN}$pain_point${NC}"
echo -e "✨ Melhor aspecto: ${CYAN}$best_aspect${NC}"
echo -e "💡 Sugestão: ${CYAN}$improvement${NC}"

echo ""
echo -e "${GREEN}✅ Feedback salvo com sucesso!${NC}"
echo -e "${BLUE}📁 Arquivo: $feedback_file${NC}"

# Análise rápida
echo -e "\n${BOLD}📈 ANÁLISE RÁPIDA${NC}"
echo "=========================================================="

total_feedbacks=$(find "$FEEDBACK_DIR" -name "feedback_*.json" 2>/dev/null | wc -l)
echo -e "📊 Total de feedbacks coletados: ${CYAN}$total_feedbacks${NC}"

if [ $total_feedbacks -gt 1 ]; then
    echo -e "${BLUE}💡 Execute ./analyze-feedback.sh para ver análise completa${NC}"
fi

# Agradecimento
echo ""
echo -e "${GREEN}🙏 Obrigado pelo seu feedback!${NC}"
echo -e "${BLUE}Suas opiniões são fundamentais para evolução do CDD.${NC}"

# Dicas baseadas no feedback
echo ""
echo -e "${BOLD}💡 DICA PERSONALIZADA${NC}"
echo "=========================================================="

if [ $effectiveness -le 5 ]; then
    echo -e "${YELLOW}📚 Considera revisar a documentação de princípios e fazer o workshop de onboarding.${NC}"
elif [ $effectiveness -le 7 ]; then
    echo -e "${BLUE}🎯 Você está no caminho certo! Foque nas áreas que mais impactam seu trabalho.${NC}"
else
    echo -e "${GREEN}🎉 Ótimo! Considere compartilhar suas boas práticas com a equipe.${NC}"
fi

if [ ! -z "$pain_point" ]; then
    echo -e "${CYAN}🔧 Sua dificuldade '$pain_point' será considerada nas próximas melhorias.${NC}"
fi 