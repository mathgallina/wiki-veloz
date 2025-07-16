from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime
from slugify import slugify
import markdown

app = Flask(__name__)
CORS(app)

# Configuração
DATA_FILE = 'data/pages.json'
UPLOADS_FOLDER = 'static/uploads'

# Criar diretórios se não existirem
os.makedirs('data', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('templates', exist_ok=True)

def load_pages():
    """Carrega as páginas do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_pages(pages):
    """Salva as páginas no arquivo JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

def create_sample_data():
    """Cria dados de exemplo se não existirem"""
    pages = load_pages()
    if not pages:
        sample_pages = [
            {
                "id": "visao-empresa",
                "title": "Visão da Empresa",
                "category": "visao-empresa",
                "content": """# Visão da Veloz Fibra

## Nossa Missão
Fornecer internet de alta velocidade e qualidade para conectar pessoas e transformar comunidades.

## Nossos Valores
- **Qualidade**: Sempre entregar o melhor serviço possível
- **Inovação**: Buscar constantemente novas tecnologias e soluções
- **Confiança**: Construir relacionamentos duradouros com nossos clientes
- **Comunidade**: Contribuir para o desenvolvimento das regiões onde atuamos

## Objetivos Estratégicos
1. Expandir nossa cobertura de fibra óptica
2. Manter a qualidade do atendimento ao cliente
3. Investir em tecnologia e inovação
4. Crescer de forma sustentável""",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "ferramentas-utilizadas",
                "title": "Ferramentas Utilizadas",
                "category": "ferramentas",
                "content": """# Ferramentas da Veloz Fibra

## Gestão de Clientes
- **CRM**: Sistema próprio para gestão de clientes
- **WhatsApp Business**: Comunicação com clientes
- **Google Workspace**: Email e colaboração

## Operacional
- **Sistema de Monitoramento**: Acompanhamento de rede
- **App de Campo**: Para técnicos em campo
- **Planilhas Google**: Controle de processos

## Financeiro
- **Sistema de Cobrança**: Integrado com CRM
- **Controle de Caixa**: Gestão financeira
- **Relatórios**: Análise de performance

## Marketing
- **Redes Sociais**: Instagram, Facebook
- **Google Ads**: Publicidade online
- **Site Institucional**: WordPress""",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "processos-internos",
                "title": "Processos Internos",
                "category": "processos",
                "content": """# Processos Internos

## Atendimento ao Cliente
1. **Recebimento da Solicitação**: Via WhatsApp, telefone ou presencial
2. **Análise de Viabilidade**: Verificar cobertura na região
3. **Agendamento**: Marcar instalação ou visita técnica
4. **Execução**: Técnico realiza instalação
5. **Acompanhamento**: Monitorar qualidade do serviço

## Instalação de Novos Clientes
1. **Cadastro no Sistema**: Dados completos do cliente
2. **Verificação de Cobertura**: Confirmar disponibilidade
3. **Agendamento**: Definir data e horário
4. **Instalação**: Técnico realiza conexão
5. **Teste**: Verificar velocidade e estabilidade
6. **Ativação**: Liberar acesso à internet

## Manutenção
1. **Identificação do Problema**: Cliente reporta ou sistema detecta
2. **Análise**: Verificar se é problema de rede ou equipamento
3. **Agendamento**: Marcar visita técnica se necessário
4. **Resolução**: Técnico resolve o problema
5. **Teste**: Confirmar funcionamento
6. **Fechamento**: Registrar solução no sistema""",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "onboarding",
                "title": "Onboarding de Novos Colaboradores",
                "category": "onboarding",
                "content": """# Onboarding - Bem-vindo à Veloz Fibra!

## Primeiro Dia
1. **Apresentação**: Conhecer a equipe e a empresa
2. **Acesso aos Sistemas**: Configurar logins e senhas
3. **Tour pela Empresa**: Conhecer as instalações
4. **Documentação**: Receber manual de procedimentos

## Primeira Semana
1. **Treinamento Técnico**: Aprender sobre produtos e serviços
2. **Processos**: Entender fluxos de trabalho
3. **Ferramentas**: Dominar sistemas utilizados
4. **Expectativas**: Alinhar objetivos e metas

## Primeiro Mês
1. **Acompanhamento**: Mentor designado para dúvidas
2. **Feedback**: Avaliação de desempenho
3. **Integração**: Participar de reuniões e eventos
4. **Independência**: Assumir responsabilidades

## Recursos Disponíveis
- Esta wiki para consulta
- Manual de procedimentos
- Contatos da equipe
- Treinamentos online""",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "historico-mudancas",
                "title": "Histórico de Mudanças",
                "category": "historico",
                "content": """# Histórico de Mudanças e Decisões

## Janeiro 2024
- **15/01**: Implementação da wiki interna
- **10/01**: Nova política de atendimento ao cliente
- **05/01**: Atualização do sistema de monitoramento

## Dezembro 2023
- **20/12**: Expansão da cobertura para bairro novo
- **15/12**: Contratação de 2 novos técnicos
- **10/12**: Melhoria no sistema de cobrança

## Novembro 2023
- **25/11**: Implementação de nova ferramenta de CRM
- **15/11**: Treinamento da equipe em novas tecnologias
- **05/11**: Reestruturação do processo de instalação

## Outubro 2023
- **30/10**: Lançamento do novo plano de internet
- **20/10**: Parceria com fornecedor de equipamentos
- **10/10**: Melhoria na infraestrutura de rede""",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        ]
        save_pages(sample_pages)
        return sample_pages
    return pages

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/pages')
def get_pages():
    """Retorna todas as páginas"""
    pages = load_pages()
    return jsonify(pages)

@app.route('/api/pages/<page_id>')
def get_page(page_id):
    """Retorna uma página específica"""
    pages = load_pages()
    page = next((p for p in pages if p['id'] == page_id), None)
    if page:
        return jsonify(page)
    return jsonify({"error": "Página não encontrada"}), 404

@app.route('/api/pages', methods=['POST'])
def create_page():
    """Cria uma nova página"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Título é obrigatório"}), 400
    
    pages = load_pages()
    
    # Gerar ID único baseado no título
    page_id = slugify(data['title'])
    
    # Verificar se já existe
    if any(p['id'] == page_id for p in pages):
        page_id = f"{page_id}-{len(pages) + 1}"
    
    new_page = {
        "id": page_id,
        "title": data['title'],
        "category": data.get('category', 'geral'),
        "content": data.get('content', ''),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    pages.append(new_page)
    save_pages(pages)
    
    return jsonify(new_page), 201

@app.route('/api/pages/<page_id>', methods=['PUT'])
def update_page(page_id):
    """Atualiza uma página existente"""
    data = request.get_json()
    pages = load_pages()
    
    page_index = next((i for i, p in enumerate(pages) if p['id'] == page_id), None)
    
    if page_index is None:
        return jsonify({"error": "Página não encontrada"}), 404
    
    pages[page_index].update({
        "title": data.get('title', pages[page_index]['title']),
        "category": data.get('category', pages[page_index]['category']),
        "content": data.get('content', pages[page_index]['content']),
        "updated_at": datetime.now().isoformat()
    })
    
    save_pages(pages)
    return jsonify(pages[page_index])

@app.route('/api/pages/<page_id>', methods=['DELETE'])
def delete_page(page_id):
    """Deleta uma página"""
    pages = load_pages()
    pages = [p for p in pages if p['id'] != page_id]
    save_pages(pages)
    return jsonify({"message": "Página deletada com sucesso"})

@app.route('/api/search')
def search_pages():
    """Pesquisa páginas por termo"""
    query = request.args.get('q', '').lower()
    pages = load_pages()
    
    if not query:
        return jsonify(pages)
    
    results = []
    for page in pages:
        if (query in page['title'].lower() or 
            query in page['content'].lower() or
            query in page['category'].lower()):
            results.append(page)
    
    return jsonify(results)

@app.route('/api/categories')
def get_categories():
    """Retorna todas as categorias"""
    pages = load_pages()
    categories = list(set(page['category'] for page in pages))
    return jsonify(categories)

if __name__ == '__main__':
    # Criar dados de exemplo na primeira execução
    create_sample_data()
    app.run(debug=True, host='0.0.0.0', port=8000)
