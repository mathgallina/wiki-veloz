.PHONY: help install dev test format lint clean docker-build docker-run docker-stop

# Variáveis
PYTHON = python3
PIP = pip3
NPM = npm
DOCKER = docker
DOCKER_COMPOSE = docker-compose

# Cores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Mostra esta ajuda
	@echo "$(GREEN)Wiki Veloz Fibra - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala todas as dependências
	@echo "$(GREEN)Instalando dependências Python...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Instalando dependências Node.js...$(NC)"
	$(NPM) install
	@echo "$(GREEN)Instalando pre-commit hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Instalação concluída!$(NC)"

dev: ## Inicia o servidor de desenvolvimento
	@echo "$(GREEN)Iniciando servidor de desenvolvimento...$(NC)"
	$(PYTHON) app.py

test: ## Executa todos os testes
	@echo "$(GREEN)Executando testes...$(NC)"
	pytest -v

test-cov: ## Executa testes com cobertura
	@echo "$(GREEN)Executando testes com cobertura...$(NC)"
	pytest --cov=app --cov-report=html --cov-report=term

format: ## Formata o código Python
	@echo "$(GREEN)Formatando código Python...$(NC)"
	black . --line-length=88
	isort . --profile=black --line-length=88

lint: ## Executa linting
	@echo "$(GREEN)Executando linting...$(NC)"
	flake8 . --max-line-length=88 --extend-ignore=E203,W503

check: ## Executa todas as verificações de qualidade
	@echo "$(GREEN)Executando verificações de qualidade...$(NC)"
	$(MAKE) format
	$(MAKE) lint
	@echo "$(GREEN)✅ Verificações concluídas!$(NC)"

clean: ## Limpa arquivos temporários
	@echo "$(GREEN)Limpando arquivos temporários...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

docker-build: ## Constrói a imagem Docker
	@echo "$(GREEN)Construindo imagem Docker...$(NC)"
	$(DOCKER) build -t wiki-veloz .

docker-run: ## Executa o container Docker
	@echo "$(GREEN)Executando container Docker...$(NC)"
	$(DOCKER_COMPOSE) up -d

docker-stop: ## Para o container Docker
	@echo "$(GREEN)Parando container Docker...$(NC)"
	$(DOCKER_COMPOSE) down

docker-logs: ## Mostra logs do Docker
	@echo "$(GREEN)Mostrando logs do Docker...$(NC)"
	$(DOCKER_COMPOSE) logs -f

backup: ## Cria backup manual
	@echo "$(GREEN)Criando backup manual...$(NC)"
	$(PYTHON) -c "from app import create_backup_route; create_backup_route()"

setup-dev: ## Configura ambiente de desenvolvimento
	@echo "$(GREEN)Configurando ambiente de desenvolvimento...$(NC)"
	$(MAKE) install
	$(MAKE) format
	@echo "$(GREEN)✅ Ambiente configurado!$(NC)"

deploy: ## Deploy para produção
	@echo "$(GREEN)Fazendo deploy...$(NC)"
	$(MAKE) test
	$(MAKE) check
	$(DOCKER) build -t wiki-veloz:prod .
	@echo "$(GREEN)✅ Deploy concluído!$(NC)"

logs: ## Mostra logs da aplicação
	@echo "$(GREEN)Mostrando logs...$(NC)"
	tail -f logs/app.log

status: ## Mostra status do sistema
	@echo "$(GREEN)Status do sistema:$(NC)"
	@echo "Python: $(shell which python3)"
	@echo "Node: $(shell which node)"
	@echo "Docker: $(shell which docker)"
	@echo "Porta 8000: $(shell lsof -ti:8000 2>/dev/null || echo 'Livre')"

reset: ## Reseta o ambiente (CUIDADO!)
	@echo "$(RED)⚠️  ATENÇÃO: Isso vai apagar todos os dados!$(NC)"
	@read -p "Tem certeza? (y/N): " confirm && [ "$$confirm" = "y" ]
	$(MAKE) clean
	rm -rf data/*.json
	rm -rf static/uploads/*
	rm -rf backups/*
	@echo "$(GREEN)✅ Reset concluído!$(NC)" 