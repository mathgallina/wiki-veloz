#!/bin/bash

# metrics-code-quality.sh - Análise de qualidade do código
# Uso: ./metrics-code-quality.sh [--json] [--detailed]

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
            echo "  --detailed   Incluir detalhes sobre problemas encontrados"
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
        echo -e "\n${PURPLE}🔍 $1${NC}"
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
            *)
                echo -e "${BLUE}📊 $label: $value${NC}"
                ;;
        esac
    fi
}

# Variáveis para coleta de métricas
pattern_violations=0
pattern_check_available=false
linting_errors=0
linting_warnings=0
linting_available=false
test_coverage=0
test_coverage_available=false
outdated_dependencies=0
dependency_check_available=false
security_vulnerabilities=0
security_check_available=false
code_complexity=0
complexity_check_available=false

# Verificar patterns compliance
print_header "CONFORMIDADE COM PADRÕES"

if [ -f ".kiro/scripts/check-patterns.js" ]; then
    pattern_check_available=true
    
    # Executar verificação de patterns
    pattern_output=$(cd .kiro/scripts && node check-patterns.js 2>&1 || true)
    
    # Contar violações
    pattern_violations=$(echo "$pattern_output" | grep -c "violation\|❌\|ERROR" 2>/dev/null || echo "0")
    pattern_successes=$(echo "$pattern_output" | grep -c "✅\|SUCCESS\|OK" 2>/dev/null || echo "0")
    
    if [ $pattern_violations -eq 0 ]; then
        print_metric "Violações de padrões" "$pattern_violations" "success"
    elif [ $pattern_violations -le 5 ]; then
        print_metric "Violações de padrões" "$pattern_violations" "warning"
    else
        print_metric "Violações de padrões" "$pattern_violations" "error"
    fi
    
    print_metric "Verificações de padrões OK" "$pattern_successes" "info"
    
    if [ "$DETAILED_OUTPUT" = true ] && [ $pattern_violations -gt 0 ]; then
        echo ""
        echo "🔍 Detalhes das violações:"
        echo "$pattern_output" | grep -E "violation|❌|ERROR" | head -5
        if [ $pattern_violations -gt 5 ]; then
            echo "  ... e mais $((pattern_violations - 5)) violações"
        fi
    fi
else
    print_metric "Verificação de padrões" "Não disponível" "warning"
    print_metric "Configurar" "Execute: cd .kiro/scripts && npm install" "info"
fi

# Verificar linting
print_header "ANÁLISE DE LINTING"

# Verificar ESLint
if command -v npx >/dev/null 2>&1 && [ -f "package.json" ]; then
    linting_available=true
    
    # Verificar se ESLint está configurado
    if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] || [ -f "eslint.config.js" ]; then
        # Executar ESLint
        lint_output=""
        
        # Tentar diferentes diretórios de código
        for src_dir in "src" "lib" "app" "frontend" "backend" "."; do
            if [ -d "$src_dir" ]; then
                temp_output=$(npx eslint "$src_dir" --format=unix 2>/dev/null || true)
                if [ -n "$temp_output" ]; then
                    lint_output="$lint_output$temp_output"
                fi
            fi
        done
        
        # Contar erros e warnings
        linting_errors=$(echo "$lint_output" | grep -c ": error " 2>/dev/null || echo "0")
        linting_warnings=$(echo "$lint_output" | grep -c ": warning " 2>/dev/null || echo "0")
        
        if [ $linting_errors -eq 0 ] && [ $linting_warnings -eq 0 ]; then
            print_metric "Erros de linting" "$linting_errors" "success"
            print_metric "Avisos de linting" "$linting_warnings" "success"
        elif [ $linting_errors -eq 0 ]; then
            print_metric "Erros de linting" "$linting_errors" "success"
            print_metric "Avisos de linting" "$linting_warnings" "warning"
        else
            print_metric "Erros de linting" "$linting_errors" "error"
            print_metric "Avisos de linting" "$linting_warnings" "warning"
        fi
        
        if [ "$DETAILED_OUTPUT" = true ] && [ $linting_errors -gt 0 ]; then
            echo ""
            echo "🔍 Principais erros de linting:"
            echo "$lint_output" | grep ": error " | head -5
            if [ $linting_errors -gt 5 ]; then
                echo "  ... e mais $((linting_errors - 5)) erros"
            fi
        fi
    else
        print_metric "Configuração ESLint" "Não encontrada" "warning"
        print_metric "Configurar" "Copie de .kiro/patterns/linting/ se existir" "info"
    fi
    
    # Verificar Prettier
    if [ -f ".prettierrc" ] || [ -f ".prettierrc.js" ] || [ -f ".prettierrc.json" ]; then
        print_metric "Configuração Prettier" "Encontrada" "success"
    else
        print_metric "Configuração Prettier" "Não encontrada" "warning"
    fi
else
    print_metric "Linting" "NPM não disponível ou package.json ausente" "error"
fi

# Verificar cobertura de testes
print_header "COBERTURA DE TESTES"

# Verificar diferentes formatos de coverage
coverage_files=("coverage/lcov.info" "coverage/coverage-summary.json" "coverage/clover.xml")
coverage_found=false

for coverage_file in "${coverage_files[@]}"; do
    if [ -f "$coverage_file" ]; then
        coverage_found=true
        test_coverage_available=true
        
        case "$coverage_file" in
            */lcov.info)
                # Extrair coverage do LCOV
                if command -v awk >/dev/null 2>&1; then
                    lines_found=$(grep -o "LF:[0-9]*" "$coverage_file" | cut -d: -f2 | awk '{s+=$1} END {print s+0}')
                    lines_hit=$(grep -o "LH:[0-9]*" "$coverage_file" | cut -d: -f2 | awk '{s+=$1} END {print s+0}')
                    
                    if [ $lines_found -gt 0 ]; then
                        test_coverage=$((lines_hit * 100 / lines_found))
                    fi
                fi
                ;;
            */coverage-summary.json)
                # Extrair coverage do JSON (se jq estiver disponível)
                if command -v jq >/dev/null 2>&1; then
                    test_coverage=$(jq -r '.total.lines.pct // 0' "$coverage_file" 2>/dev/null | cut -d. -f1)
                fi
                ;;
        esac
        
        break
    fi
done

if [ "$test_coverage_available" = true ]; then
    if [ $test_coverage -ge 80 ]; then
        print_metric "Cobertura de testes" "$test_coverage%" "success"
    elif [ $test_coverage -ge 60 ]; then
        print_metric "Cobertura de testes" "$test_coverage%" "warning"
    else
        print_metric "Cobertura de testes" "$test_coverage%" "error"
    fi
else
    print_metric "Cobertura de testes" "Não disponível" "warning"
    print_metric "Gerar coverage" "Execute: npm test -- --coverage" "info"
fi

# Verificar dependências
print_header "ANÁLISE DE DEPENDÊNCIAS"

if [ -f "package.json" ] && command -v npm >/dev/null 2>&1; then
    dependency_check_available=true
    
    # Verificar dependências desatualizadas
    outdated_output=$(npm outdated --json 2>/dev/null || echo "{}")
    
    if command -v jq >/dev/null 2>&1; then
        outdated_dependencies=$(echo "$outdated_output" | jq 'length' 2>/dev/null || echo "0")
    else
        # Fallback sem jq
        outdated_dependencies=$(echo "$outdated_output" | grep -c '"current"' 2>/dev/null || echo "0")
    fi
    
    if [ $outdated_dependencies -eq 0 ]; then
        print_metric "Dependências desatualizadas" "$outdated_dependencies" "success"
    elif [ $outdated_dependencies -le 5 ]; then
        print_metric "Dependências desatualizadas" "$outdated_dependencies" "warning"
    else
        print_metric "Dependências desatualizadas" "$outdated_dependencies" "error"
    fi
    
    # Verificar vulnerabilidades (se npm audit estiver disponível)
    audit_output=$(npm audit --json 2>/dev/null || echo '{"vulnerabilities":{}}')
    
    if command -v jq >/dev/null 2>&1; then
        security_vulnerabilities=$(echo "$audit_output" | jq '.metadata.vulnerabilities.total // 0' 2>/dev/null || echo "0")
        critical_vulns=$(echo "$audit_output" | jq '.metadata.vulnerabilities.critical // 0' 2>/dev/null || echo "0")
        high_vulns=$(echo "$audit_output" | jq '.metadata.vulnerabilities.high // 0' 2>/dev/null || echo "0")
    else
        # Fallback simples
        security_vulnerabilities=$(echo "$audit_output" | grep -c "vulnerability" 2>/dev/null || echo "0")
        critical_vulns=0
        high_vulns=0
    fi
    
    security_check_available=true
    
    if [ $security_vulnerabilities -eq 0 ]; then
        print_metric "Vulnerabilidades de segurança" "$security_vulnerabilities" "success"
    elif [ $critical_vulns -gt 0 ] || [ $high_vulns -gt 0 ]; then
        print_metric "Vulnerabilidades de segurança" "$security_vulnerabilities (críticas: $critical_vulns, altas: $high_vulns)" "error"
    else
        print_metric "Vulnerabilidades de segurança" "$security_vulnerabilities" "warning"
    fi
    
    if [ "$DETAILED_OUTPUT" = true ] && [ $outdated_dependencies -gt 0 ]; then
        echo ""
        echo "🔍 Dependências desatualizadas:"
        npm outdated 2>/dev/null | head -6 | tail -5 || echo "  (Execute 'npm outdated' para detalhes)"
    fi
else
    print_metric "Análise de dependências" "package.json não encontrado ou npm não disponível" "error"
fi

# Verificar complexidade (se há ferramentas disponíveis)
print_header "COMPLEXIDADE DO CÓDIGO"

# Verificar se há ferramentas de análise de complexidade
complexity_tools=("plato" "jscpd" "complexity-report")
complexity_available=false

for tool in "${complexity_tools[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        complexity_available=true
        break
    fi
done

if [ "$complexity_available" = true ]; then
    print_metric "Ferramentas de complexidade" "Disponíveis" "success"
    print_metric "Análise detalhada" "Execute ferramentas específicas conforme necessário" "info"
else
    print_metric "Ferramentas de complexidade" "Não instaladas" "warning"
    print_metric "Instalar" "npm install -g plato jscpd" "info"
fi

# Verificar configurações de qualidade
print_header "CONFIGURAÇÕES DE QUALIDADE"

quality_configs=0
quality_total=6

# TypeScript
if [ -f "tsconfig.json" ]; then
    quality_configs=$((quality_configs + 1))
    print_metric "TypeScript configurado" "Sim" "success"
else
    print_metric "TypeScript configurado" "Não" "warning"
fi

# Husky (pre-commit hooks)
if [ -f ".husky/pre-commit" ] || [ -d ".husky" ]; then
    quality_configs=$((quality_configs + 1))
    print_metric "Pre-commit hooks" "Configurados" "success"
else
    print_metric "Pre-commit hooks" "Não configurados" "warning"
fi

# EditorConfig
if [ -f ".editorconfig" ]; then
    quality_configs=$((quality_configs + 1))
    print_metric "EditorConfig" "Configurado" "success"
else
    print_metric "EditorConfig" "Não configurado" "warning"
fi

# Gitignore
if [ -f ".gitignore" ]; then
    quality_configs=$((quality_configs + 1))
    print_metric "Gitignore" "Configurado" "success"
else
    print_metric "Gitignore" "Não configurado" "error"
fi

# CI/CD
if [ -f ".github/workflows/ci.yml" ] || [ -f ".gitlab-ci.yml" ] || [ -f "Jenkinsfile" ]; then
    quality_configs=$((quality_configs + 1))
    print_metric "CI/CD" "Configurado" "success"
else
    print_metric "CI/CD" "Não configurado" "warning"
fi

# Package.json scripts
if [ -f "package.json" ]; then
    test_script=$(grep -q '"test"' package.json && echo "true" || echo "false")
    build_script=$(grep -q '"build"' package.json && echo "true" || echo "false")
    lint_script=$(grep -q '"lint"' package.json && echo "true" || echo "false")
    
    scripts_count=0
    [ "$test_script" = "true" ] && scripts_count=$((scripts_count + 1))
    [ "$build_script" = "true" ] && scripts_count=$((scripts_count + 1))
    [ "$lint_script" = "true" ] && scripts_count=$((scripts_count + 1))
    
    if [ $scripts_count -eq 3 ]; then
        quality_configs=$((quality_configs + 1))
        print_metric "Scripts NPM" "Configurados (test, build, lint)" "success"
    elif [ $scripts_count -gt 0 ]; then
        print_metric "Scripts NPM" "Parcialmente configurados ($scripts_count/3)" "warning"
    else
        print_metric "Scripts NPM" "Não configurados" "warning"
    fi
fi

# Saída dos resultados
if [ "$JSON_OUTPUT" = true ]; then
    # Saída em JSON
    cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "project": "$(basename "$(pwd)")",
  "metrics": {
    "patterns": {
      "available": $pattern_check_available,
      "violations": $pattern_violations
    },
    "linting": {
      "available": $linting_available,
      "errors": $linting_errors,
      "warnings": $linting_warnings
    },
    "testing": {
      "coverage_available": $test_coverage_available,
      "coverage_percentage": $test_coverage
    },
    "dependencies": {
      "check_available": $dependency_check_available,
      "outdated": $outdated_dependencies,
      "security_vulnerabilities": $security_vulnerabilities
    },
    "quality_configs": {
      "configured": $quality_configs,
      "total": $quality_total,
      "percentage": $((quality_configs * 100 / quality_total))
    }
  },
  "status": {
    "patterns_ok": $([ $pattern_violations -eq 0 ] && echo "true" || echo "false"),
    "linting_ok": $([ $linting_errors -eq 0 ] && echo "true" || echo "false"),
    "coverage_ok": $([ $test_coverage -ge 80 ] && echo "true" || echo "false"),
    "dependencies_ok": $([ $outdated_dependencies -le 5 ] && [ $security_vulnerabilities -eq 0 ] && echo "true" || echo "false"),
    "configs_ok": $([ $quality_configs -ge 4 ] && echo "true" || echo "false")
  }
}
EOF
else
    # Saída em texto com score
    print_header "SCORE DE QUALIDADE DO CÓDIGO"
    
    # Calcular score geral (0-100)
    score=0
    max_score=100
    
    # Peso das métricas
    pattern_weight=25
    linting_weight=25
    testing_weight=20
    security_weight=20
    config_weight=10
    
    # Score de patterns
    if [ "$pattern_check_available" = true ]; then
        if [ $pattern_violations -eq 0 ]; then
            pattern_score=$pattern_weight
        elif [ $pattern_violations -le 5 ]; then
            pattern_score=$((pattern_weight * 70 / 100))
        else
            pattern_score=$((pattern_weight * 30 / 100))
        fi
    else
        pattern_score=$((pattern_weight / 2))  # 50% se não disponível
    fi
    
    # Score de linting
    if [ "$linting_available" = true ]; then
        if [ $linting_errors -eq 0 ]; then
            linting_score=$linting_weight
        elif [ $linting_errors -le 10 ]; then
            linting_score=$((linting_weight * 60 / 100))
        else
            linting_score=$((linting_weight * 20 / 100))
        fi
    else
        linting_score=0
    fi
    
    # Score de testes
    if [ "$test_coverage_available" = true ]; then
        testing_score=$((test_coverage * testing_weight / 100))
    else
        testing_score=0
    fi
    
    # Score de segurança
    security_score=$security_weight
    if [ $security_vulnerabilities -gt 0 ]; then
        security_score=$((security_weight * 50 / 100))
    fi
    if [ $outdated_dependencies -gt 10 ]; then
        security_score=$((security_score * 80 / 100))
    fi
    
    # Score de configuração
    config_score=$((quality_configs * config_weight / quality_total))
    
    total_score=$((pattern_score + linting_score + testing_score + security_score + config_score))
    
    echo ""
    echo "📊 Breakdown do score:"
    print_metric "Padrões" "$pattern_score/$pattern_weight pontos" "info"
    print_metric "Linting" "$linting_score/$linting_weight pontos" "info"
    print_metric "Testes" "$testing_score/$testing_weight pontos" "info"
    print_metric "Segurança" "$security_score/$security_weight pontos" "info"
    print_metric "Configuração" "$config_score/$config_weight pontos" "info"
    
    echo ""
    if [ $total_score -ge 85 ]; then
        print_metric "Score geral" "$total_score/100" "success"
        echo -e "${GREEN}🏆 Excelente! Código com alta qualidade.${NC}"
    elif [ $total_score -ge 70 ]; then
        print_metric "Score geral" "$total_score/100" "warning"
        echo -e "${YELLOW}👍 Bom! Algumas melhorias podem elevar ainda mais a qualidade.${NC}"
    elif [ $total_score -ge 50 ]; then
        print_metric "Score geral" "$total_score/100" "warning"
        echo -e "${YELLOW}⚠️  Moderado. Foque em linting e testes.${NC}"
    else
        print_metric "Score geral" "$total_score/100" "error"
        echo -e "${RED}🔧 Baixo. Implemente práticas básicas de qualidade.${NC}"
    fi
    
    # Recomendações
    echo ""
    print_header "RECOMENDAÇÕES PRIORITÁRIAS"
    
    if [ $linting_errors -gt 0 ]; then
        echo "🔧 Corrija erros de linting (prioridade alta)"
    fi
    
    if [ $security_vulnerabilities -gt 0 ]; then
        echo "🔒 Resolva vulnerabilidades de segurança (prioridade alta)"
    fi
    
    if [ $test_coverage -lt 60 ]; then
        echo "🧪 Aumente cobertura de testes para pelo menos 60%"
    fi
    
    if [ "$pattern_check_available" = false ]; then
        echo "📐 Configure verificação de padrões (.kiro/scripts)"
    fi
    
    if [ $quality_configs -lt 4 ]; then
        echo "⚙️ Configure mais ferramentas de qualidade (TypeScript, Husky, etc.)"
    fi
fi 