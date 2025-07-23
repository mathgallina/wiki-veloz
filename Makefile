# CDD v2.0 - Wiki Veloz Makefile

.PHONY: help dev test lint lint-fix cdd-scan cdd-status cdd-health cdd-complete setup

help: ## Mostrar ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Rodar aplicação em desenvolvimento
	python app.py

test: ## Rodar testes
	python -m pytest tests/ -v

lint: ## Verificar linting
	flake8 .
	black --check .
	isort --check-only .

lint-fix: ## Corrigir problemas de linting
	black .
	isort .

cdd-scan: ## Escanear tasks CDD
	cd .kiro/scripts && npm run scan

cdd-status: ## Status do projeto CDD
	cd .kiro/scripts && npm run status

cdd-health: ## Health dashboard CDD
	cd .kiro/scripts && npm run health

cdd-complete: ## Marcar task como concluída (uso: make cdd-complete TASK=feature-1.1)
	cd .kiro/scripts && npm run complete $(TASK)

setup: ## Setup inicial do projeto
	pip install -r requirements.txt
	npm install
	cd .kiro/scripts && npm install
	make cdd-scan

deploy: ## Deploy para produção
	git push heroku main

backup: ## Backup manual
	cd .kiro/scripts && npm run backup

cleanup: ## Limpeza semanal
	cd .kiro/scripts && npm run cleanup
