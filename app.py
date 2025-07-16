import os
import json
import bcrypt
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify
import markdown

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'veloz-fibra-secret-key-2024')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)  # Sessão de 8 horas

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

CORS(app)

# Classe de usuário
class User(UserMixin):
    def __init__(self, user_id, username, name, role, created_at):
        self.id = user_id
        self.username = username
        self.name = name
        self.role = role
        self.created_at = created_at

# Funções para gerenciar usuários
def load_users():
    """Carrega usuários do arquivo JSON"""
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    """Salva usuários no arquivo JSON"""
    os.makedirs('data', exist_ok=True)
    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def create_default_admin():
    """Cria o usuário administrador padrão (Matheus Gallina)"""
    users = load_users()

    # Verificar se já existe um admin
    if not any(user['role'] == 'admin' for user in users):
        admin_user = {
            'id': 'admin-001',
            'username': 'matheus.gallina',
            'name': 'Matheus Gallina',
            'email': 'matheus@velozfibra.com',
            'password_hash': generate_password_hash('Veloz2024!'),
            'role': 'admin',
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'is_active': True
        }
        users.append(admin_user)
        save_users(users)
        print("✅ Usuário administrador criado: Matheus Gallina")

def log_activity(user_id, action, details=None):
    """Registra atividade do usuário"""
    log_entry = {
        'user_id': user_id,
        'action': action,
        'details': details,
        'timestamp': datetime.now().isoformat(),
        'ip_address': request.remote_addr
    }

    try:
        with open('data/activity_log.json', 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)

    # Manter apenas os últimos 1000 logs
    if len(logs) > 1000:
        logs = logs[-1000:]

    with open('data/activity_log.json', 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

@login_manager.user_loader
def load_user(user_id):
    """Carrega usuário para o Flask-Login"""
    users = load_users()
    user_data = next((u for u in users if u['id'] == user_id), None)
    if user_data and user_data.get('is_active', True):
        return User(
            user_data['id'],
            user_data['username'],
            user_data['name'],
            user_data['role'],
            user_data['created_at']
        )
    return None

# Funções para gerenciar páginas (mantidas do código original)
def load_pages():
    """Carrega páginas do arquivo JSON"""
    try:
        with open('data/pages.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_pages(pages):
    """Salva páginas no arquivo JSON"""
    os.makedirs('data', exist_ok=True)
    with open('data/pages.json', 'w', encoding='utf-8') as f:
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
                "content": "# Visão da Veloz Fibra\n\n## Nossa Missão\nFornecer internet de alta velocidade e qualidade para conectar pessoas e transformar comunidades.\n\n## Nossos Valores\n- **Qualidade**: Sempre entregar o melhor serviço possível\n- **Inovação**: Buscar constantemente novas tecnologias e soluções\n- **Confiança**: Construir relacionamentos duradouros com nossos clientes\n- **Comunidade**: Contribuir para o desenvolvimento das regiões onde atuamos\n\n## Objetivos Estratégicos\n1. Expandir nossa cobertura de fibra óptica\n2. Manter a qualidade do atendimento ao cliente\n3. Investir em tecnologia e inovação\n4. Crescer de forma sustentável",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "ferramentas-utilizadas",
                "title": "Ferramentas Utilizadas",
                "category": "ferramentas",
                "content": "# Ferramentas da Veloz Fibra\n\n## Gestão de Clientes\n- **CRM**: Sistema próprio para gestão de clientes\n- **WhatsApp Business**: Comunicação com clientes\n- **Google Workspace**: Email e colaboração\n\n## Operacional\n- **Sistema de Monitoramento**: Acompanhamento de rede\n- **App de Campo**: Para técnicos em campo\n- **Planilhas Google**: Controle de processos\n\n## Financeiro\n- **Sistema de Cobrança**: Integrado com CRM\n- **Controle de Caixa**: Gestão financeira\n- **Relatórios**: Análise de performance\n\n## Marketing\n- **Redes Sociais**: Instagram, Facebook\n- **Google Ads**: Publicidade online\n- **Site Institucional**: WordPress",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "processos-internos",
                "title": "Processos Internos",
                "category": "processos",
                "content": "# Processos Internos\n\n## Atendimento ao Cliente\n1. **Recebimento da Solicitação**: Via WhatsApp, telefone ou presencial\n2. **Análise de Viabilidade**: Verificar cobertura na região\n3. **Agendamento**: Marcar instalação ou visita técnica\n4. **Execução**: Técnico realiza instalação\n5. **Acompanhamento**: Monitorar qualidade do serviço\n\n## Instalação de Novos Clientes\n1. **Cadastro no Sistema**: Dados completos do cliente\n2. **Verificação de Cobertura**: Confirmar disponibilidade\n3. **Agendamento**: Definir data e horário\n4. **Instalação**: Técnico realiza conexão\n5. **Teste**: Verificar velocidade e estabilidade\n6. **Ativação**: Liberar acesso à internet\n\n## Manutenção\n1. **Identificação do Problema**: Cliente reporta ou sistema detecta\n2. **Análise**: Verificar se é problema de rede ou equipamento\n3. **Agendamento**: Marcar visita técnica se necessário\n4. **Resolução**: Técnico resolve o problema\n5. **Teste**: Confirmar funcionamento\n6. **Fechamento**: Registrar solução no sistema",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "onboarding",
                "title": "Onboarding de Novos Colaboradores",
                "category": "onboarding",
                "content": "# Onboarding - Bem-vindo à Veloz Fibra!\n\n## Primeiro Dia\n1. **Apresentação**: Conhecer a equipe e a empresa\n2. **Acesso aos Sistemas**: Configurar logins e senhas\n3. **Tour pela Empresa**: Conhecer as instalações\n4. **Documentação**: Receber manual de procedimentos\n\n## Primeira Semana\n1. **Treinamento Técnico**: Aprender sobre produtos e serviços\n2. **Processos**: Entender fluxos de trabalho\n3. **Ferramentas**: Dominar sistemas utilizados\n4. **Expectativas**: Alinhar objetivos e metas\n\n## Primeiro Mês\n1. **Acompanhamento**: Mentor designado para dúvidas\n2. **Feedback**: Avaliação de desempenho\n3. **Integração**: Participar de reuniões e eventos\n4. **Independência**: Assumir responsabilidades\n\n## Recursos Disponíveis\n- Esta wiki para consulta\n- Manual de procedimentos\n- Contatos da equipe\n- Treinamentos online",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "historico-mudancas",
                "title": "Histórico de Mudanças",
                "category": "historico",
                "content": "# Histórico de Mudanças e Decisões\n\n## Janeiro 2024\n- **15/01**: Implementação da wiki interna\n- **10/01**: Nova política de atendimento ao cliente\n- **05/01**: Atualização do sistema de monitoramento\n\n## Dezembro 2023\n- **20/12**: Expansão da cobertura para bairro novo\n- **15/12**: Contratação de 2 novos técnicos\n- **10/12**: Melhoria no sistema de cobrança\n\n## Novembro 2023\n- **25/11**: Implementação de nova ferramenta de CRM\n- **15/11**: Treinamento da equipe em novas tecnologias\n- **05/11**: Reestruturação do processo de instalação\n\n## Outubro 2023\n- **30/10**: Lançamento do novo plano de internet\n- **20/10**: Parceria com fornecedor de equipamentos\n- **10/10**: Melhoria na infraestrutura de rede",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            },
            {
                "id": "novas-regras-comerciais",
                "title": "Novas Regras Comerciais",
                "category": "comercial",
                "content": "# Novas Regras Comerciais - Veloz Fibra\n\n## Vigência\n**A partir de 16/07/2025**\n\n## Equipe Responsável\nEquipe Comercial Veloz Fibra\n\n## Índice\n1. [Tipo de Consulta de CPF](#tipo-de-consulta-de-cpf)\n2. [Pontuação, Desconto e Elegibilidade](#pontuacao-desconto-e-elegibilidade)\n3. [Custo Comercial](#custo-comercial)\n4. [Prazo para Compromisso](#prazo-para-compromisso)\n5. [Tabela com Quantidade Desconto](#tabela-com-quantidade-desconto)\n6. [Novas Regras Base Pessoal](#novas-regras-base-pessoal)\n\n---\n\n### Tipo de Consulta de CPF\n*[Conteúdo a ser adicionado]*\n\n### Pontuação, Desconto e Elegibilidade\n*[Conteúdo a ser adicionado]*\n\n### Custo Comercial\n*[Conteúdo a ser adicionado]*\n\n### Prazo para Compromisso\n*[Conteúdo a ser adicionado]*\n\n### Tabela com Quantidade Desconto\n*[Conteúdo a ser adicionado]*\n\n### Novas Regras Base Pessoal\n*[Conteúdo a ser adicionado]*\n\n---\n\n> **Nota**: Esta página será atualizada conforme o conteúdo da apresentação for disponibilizado.\n\n**Última atualização**: 15/01/2024",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        ]
        save_pages(sample_pages)
        return sample_pages
    return pages

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        users = load_users()
        user_data = next((u for u in users if u['username'] == username), None)

        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(
                user_data['id'],
                user_data['username'],
                user_data['name'],
                user_data['role'],
                user_data['created_at']
            )
            login_user(user)

            # Atualizar último login
            user_data['last_login'] = datetime.now().isoformat()
            save_users(users)

            # Registrar atividade
            log_activity(user_data['id'], 'login', f'Login realizado por {user_data["name"]}')

            flash(f'Bem-vindo, {user_data["name"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    if current_user.is_authenticated:
        log_activity(current_user.id, 'logout', f'Logout realizado por {current_user.name}')
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

@app.route('/admin/users')
@login_required
def admin_users():
    """Página de administração de usuários (apenas para admins)"""
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
        return redirect(url_for('index'))

    users = load_users()
    return render_template('admin_users.html', users=users)

@app.route('/admin/activity')
@login_required
def admin_activity():
    """Página de log de atividades (apenas para admins)"""
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
        return redirect(url_for('index'))

    try:
        with open('data/activity_log.json', 'r', encoding='utf-8') as f:
            activities = json.load(f)
    except FileNotFoundError:
        activities = []

    # Ordenar por timestamp (mais recente primeiro)
    activities.sort(key=lambda x: x['timestamp'], reverse=True)

    return render_template('admin_activity.html', activities=activities)

# Rotas da API (protegidas)
@app.route('/')
@login_required
def index():
    """Página principal (protegida)"""
    return render_template('index.html')

@app.route('/api/pages')
@login_required
def get_pages():
    """Retorna todas as páginas (protegida)"""
    pages = load_pages()
    log_activity(current_user.id, 'api_access', 'Acesso à API de páginas')
    return jsonify(pages)

@app.route('/api/pages/<page_id>')
@login_required
def get_page(page_id):
    """Retorna uma página específica (protegida)"""
    pages = load_pages()
    page = next((p for p in pages if p['id'] == page_id), None)
    if page:
        log_activity(current_user.id, 'page_view', f'Visualizou página: {page["title"]}')
        return jsonify(page)
    return jsonify({"error": "Página não encontrada"}), 404

@app.route('/api/pages', methods=['POST'])
@login_required
def create_page():
    """Cria uma nova página (protegida)"""
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
        "updated_at": datetime.now().isoformat(),
        "created_by": current_user.id,
        "created_by_name": current_user.name
    }

    pages.append(new_page)
    save_pages(pages)

    log_activity(current_user.id, 'page_create', f'Criou página: {data["title"]}')
    return jsonify(new_page), 201

@app.route('/api/pages/<page_id>', methods=['PUT'])
@login_required
def update_page(page_id):
    """Atualiza uma página existente (protegida)"""
    data = request.get_json()
    pages = load_pages()

    page_index = next((i for i, p in enumerate(pages) if p['id'] == page_id), None)

    if page_index is None:
        return jsonify({"error": "Página não encontrada"}), 404

    old_title = pages[page_index]['title']
    pages[page_index].update({
        "title": data.get('title', pages[page_index]['title']),
        "category": data.get('category', pages[page_index]['category']),
        "content": data.get('content', pages[page_index]['content']),
        "updated_at": datetime.now().isoformat(),
        "updated_by": current_user.id,
        "updated_by_name": current_user.name
    })

    save_pages(pages)
    log_activity(current_user.id, 'page_update', f'Atualizou página: {old_title}')
    return jsonify(pages[page_index])

@app.route('/api/pages/<page_id>', methods=['DELETE'])
@login_required
def delete_page(page_id):
    """Deleta uma página (protegida)"""
    pages = load_pages()
    page_to_delete = next((p for p in pages if p['id'] == page_id), None)

    if page_to_delete:
        log_activity(current_user.id, 'page_delete', f'Deletou página: {page_to_delete["title"]}')

    pages = [p for p in pages if p['id'] != page_id]
    save_pages(pages)
    return jsonify({"message": "Página deletada com sucesso"})

@app.route('/api/search')
@login_required
def search_pages():
    """Pesquisa páginas por termo (protegida)"""
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

    log_activity(current_user.id, 'search', f'Pesquisou por: {query}')
    return jsonify(results)

@app.route('/api/categories')
@login_required
def get_categories():
    """Retorna todas as categorias (protegida)"""
    pages = load_pages()
    categories = list(set(page['category'] for page in pages))
    return jsonify(categories)

if __name__ == '__main__':
    # Criar dados de exemplo e usuário admin na primeira execução
    create_sample_data()
    create_default_admin()
    app.run(debug=True, host='0.0.0.0', port=8000)
