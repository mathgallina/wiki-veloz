# Prompt para Execução Direta - CDD Completo

## 🎯 Como Usar
Copie e cole o prompt abaixo para gerar automaticamente a estrutura `.kiro` completa em qualquer projeto:

---

## 📋 PROMPT DE EXECUÇÃO ROBUSTA

```
Analise completamente este projeto e construa toda a estrutura .kiro seguindo a metodologia Context-Driven Documentation (CDD) de forma robusta e completa.

FASE 1 - ANÁLISE PROFUNDA:
1. Explore todos os arquivos e diretórios recursivamente
2. Identifique stack tecnológico completo (package.json, dependencies, frameworks, configurações)
3. Analise arquitetura de código (componentes, módulos, padrões, estrutura de pastas)
4. Deduza propósito, funcionalidades principais e domínio de negócio
5. Examine configurações, scripts, testes e documentação existente
6. Identifique padrões de código já estabelecidos (naming, estrutura, imports)

FASE 2 - CRIAR ESTRUTURA COMPLETA:
Crie exatamente esta estrutura:

.kiro/
├── steering/
│   ├── product.md     # Visão de produto baseada na análise
│   ├── structure.md   # Organização atual documentada
│   └── tech.md        # Stack e decisões técnicas
├── patterns/
│   ├── README.md      # Índice de padrões
│   ├── conventions.md # Convenções gerais
│   ├── architecture.md # Padrões arquiteturais
│   ├── typescript.md  # Padrões TypeScript (se aplicável)
│   ├── frontend/      # Padrões frontend específicos
│   ├── backend/       # Padrões backend específicos
│   ├── examples/      # Código exemplo
│   └── linting/       # Configurações de linting
├── scripts/
│   ├── package.json   # Scripts de gerenciamento
│   ├── task-manager.js # Sistema de tracking
│   └── install.sh     # Setup automático
├── specs/
│   └── _template/
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
└── docs/
    ├── principles-and-best-practices.md
    ├── implementation-guide.md
    └── workflow-completo.md

FASE 3 - GERAR DOCUMENTAÇÃO STEERING:

product.md:
- Problema que o projeto resolve (baseado no código e estrutura)
- Solução proposta (funcionalidades identificadas)
- Objetivos mensuráveis
- Usuários-alvo (inferidos do domínio)
- Métricas de sucesso

structure.md:
- Estrutura atual de pastas explicada
- Convenções de nomenclatura identificadas
- Padrões de organização
- Fluxo de dados entre módulos
- Filosofia por trás da arquitetura

tech.md:
- Stack completo documentado
- Dependências principais e suas funções
- Decisões técnicas inferidas
- Comandos essenciais de desenvolvimento
- Configurações críticas

FASE 4 - CRIAR PATTERNS ESPECÍFICOS:

Baseado na stack identificada, crie patterns para:
- Convenções de nomenclatura específicas do projeto
- Estrutura de arquivos e imports
- Padrões de componentes (se frontend)
- Padrões de API (se backend)
- Configurações de linting personalizadas
- Exemplos práticos extraídos do código existente

FASE 5 - SCRIPTS DE AUTOMAÇÃO:

Crie scripts funcionais em .kiro/scripts/:

package.json:
```json
{
  "name": "kiro-management",
  "version": "1.0.0",
  "scripts": {
    "scan": "node task-manager.js scan",
    "status": "node task-manager.js status",
    "list": "node task-manager.js list",
    "complete": "node task-manager.js complete",
    "report": "node task-manager.js report",
    "watch": "node task-manager.js watch",
    "validate-docs": "node task-manager.js validate",
    "check-patterns": "node task-manager.js patterns"
  },
  "dependencies": {
    "chokidar": "^3.5.0",
    "glob": "^8.0.0"
  }
}
```

task-manager.js: Sistema completo de tracking de tasks com:
- Suporte ao formato feature-name-X.Y
- Validação automática de formato
- Relatórios de progresso
- Watch mode para monitoramento

install.sh: Script para setup inicial

FASE 6 - TEMPLATES ROBUSTOS:

requirements.md template:
- Formato "Como... eu quero... para que..."
- Acceptance criteria testáveis
- Regras de negócio específicas
- Casos extremos considerados

design.md template:
- Arquitetura técnica com diagramas
- Fluxo de dados
- Decisões de implementação
- Considerações de segurança e performance
- Referências aos patterns aplicáveis

tasks.md template:
- Formato obrigatório de task IDs: feature-name-X.Y
- Numeração hierárquica (1.1, 1.2, 2.1, 2.2)
- Estimativas de tempo
- Dependências explícitas
- Critérios de "pronto"

FASE 7 - FUNCIONALIDADES IDENTIFICADAS:

Para cada funcionalidade principal do código (2-4 máximo):
1. Crie pasta em .kiro/specs/[feature-name]/
2. Analise o código relacionado
3. Documente requirements baseado na implementação
4. Crie design técnico baseado na arquitetura atual
5. Gere tasks para melhorias ou completar implementação
6. Use IDs no formato: [feature-name]-X.Y

FASE 8 - VALIDAÇÃO E .CURSORRULES:

1. Valide toda a estrutura criada
2. Gere arquivo .cursorrules na raiz do projeto com:
   - Contexto completo do steering
   - Padrões específicos dos patterns/
   - Templates para criação rápida
   - Instruções para task tracking obrigatório
   - Guidelines para LLMs seguirem

REGRAS CRÍTICAS:
✅ Base tudo em evidências concretas do código
✅ Documente apenas o que existe ou está claramente indicado
✅ Crie patterns específicos da stack identificada
✅ Use task IDs no formato feature-name-X.Y
✅ Configure scripts funcionais de tracking
✅ Gere .cursorrules otimizado para LLMs
✅ Inclua validação automática
✅ Crie documentação actionable, não genérica

❌ Não especule sobre funcionalidades não implementadas
❌ Não crie documentação vaga ou genérica
❌ Não ignore padrões já estabelecidos no código
❌ Não criar task IDs em formato incorreto
❌ Não omitir scripts de automação essenciais

ORDEM DE EXECUÇÃO:
1. Análise completa → 2. Steering docs → 3. Patterns específicos → 4. Scripts funcionais → 5. Templates → 6. Specs das features → 7. .cursorrules → 8. Validação final

Comece a análise agora e construa toda a estrutura .kiro de forma completa e robusta.
```

---

## 🚀 Resultado Esperado

Após executar o prompt, você terá:

### ✅ **Estrutura Completa**
- **Estrutura .kiro robusta** com todas as pastas essenciais
- **Documentação steering** baseada na análise real e específica do projeto
- **Patterns específicos** da stack tecnológica identificada
- **Scripts funcionais** para automação e tracking

### ✅ **Automação Funcional**
- **Sistema de task tracking** com IDs no formato correto
- **Scripts de gerenciamento** prontos para uso
- **Validação automática** de estrutura e formato
- **Monitoramento em tempo real** de progresso

### ✅ **Otimização para LLMs**
- **Arquivo .cursorrules** gerado automaticamente
- **Contexto estruturado** para máxima compreensão
- **Templates consistentes** para desenvolvimento
- **Padrões específicos** documentados

### ✅ **Specs Iniciais**
- **Features principais** identificadas e documentadas
- **Requirements** baseados na implementação atual
- **Tasks** com formato e numeração corretos
- **Design técnico** alinhado com arquitetura existente

## 💡 Dicas de Uso Avançadas

### 📋 **Antes da Execução**
```bash
# 1. Certifique-se que não há pasta .kiro existente
rm -rf .kiro

# 2. Tenha o projeto em estado limpo
git status  # Verificar mudanças pendentes

# 3. Documente contexto adicional se necessário
echo "Contexto específico do projeto..." > project-context.txt
```

### 🔧 **Após a Execução**
```bash
# 1. Validar estrutura criada
./.kiro/scripts/install.sh
cd .kiro/scripts && npm run scan

# 2. Testar scripts
npm run status
npm run list

# 3. Validar task IDs
find .kiro/specs -name "tasks.md" -exec grep -H "^-\s\[" {} \;

# 4. Verificar .cursorrules
ls -la .cursorrules
head -20 .cursorrules
```

### 🎯 **Customização Pós-Geração**
1. **Refine patterns** - Ajuste padrões baseado em conhecimento específico
2. **Valide specs** - Confirme se features identificadas estão corretas
3. **Ajuste tasks** - Refine estimativas e dependências
4. **Teste automação** - Execute scripts para verificar funcionamento
5. **Otimize .cursorrules** - Adicione contexto específico do projeto

### ⚡ **Validação Completa**
```bash
# Script de validação final
#!/bin/bash
echo "🔍 Validating CDD setup..."

# Verificar estrutura obrigatória
required_dirs=(".kiro/steering" ".kiro/patterns" ".kiro/scripts" ".kiro/specs")
for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ Missing: $dir"
        exit 1
    fi
done

# Verificar scripts funcionais
cd .kiro/scripts
if npm run status >/dev/null 2>&1; then
    echo "✅ Scripts functional"
else
    echo "❌ Scripts not working"
    exit 1
fi

# Verificar task format
invalid_tasks=$(find ../specs -name "tasks.md" -exec grep -c "^-\s\[.*[^0-9\.]\s" {} \; | grep -v "^0$" | wc -l)
if [ $invalid_tasks -eq 0 ]; then
    echo "✅ Task format valid"
else
    echo "⚠️  Some tasks may have invalid format"
fi

# Verificar .cursorrules
if [ -f "../../.cursorrules" ]; then
    echo "✅ .cursorrules generated"
else
    echo "⚠️  .cursorrules missing"
fi

echo "🎉 CDD setup validation complete!"
```

## 🎯 **Para Diferentes Tipos de Projeto**

### **Frontend (React/Vue/Angular)**
O prompt automaticamente identificará e criará:
- Patterns para componentes
- Padrões de estado e props
- Configuração de linting específica
- Templates para features de UI

### **Backend (Node/Python/Java)**
O prompt automaticamente identificará e criará:
- Patterns para APIs e endpoints
- Padrões de modelo de dados
- Configuração de validação
- Templates para features de serviço

### **Fullstack**
O prompt automaticamente identificará e criará:
- Patterns para frontend e backend
- Integração entre camadas
- Fluxo de dados completo
- Templates para features end-to-end

---

> **Resultado**: Base sólida e completamente funcional para evolução do projeto com metodologia CDD, incluindo automação completa, tracking de progresso, patterns específicos e otimização para LLMs. 