import json
import os
import uuid
from datetime import datetime, timedelta

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from slugify import slugify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Sistema de Backup
try:
    from backup_system import backup_system, init_backup_system

    BACKUP_SYSTEM_AVAILABLE = True
except ImportError:
    BACKUP_SYSTEM_AVAILABLE = False
    print("⚠️ Sistema de backup não disponível")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "veloz-fibra-secret-key-2024")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)  # Sessão de 8 horas

# Configurações para upload de arquivos
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt", "jpg", "jpeg", "png", "gif"}

# Criar pasta de uploads se não existir
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Por favor, faça login para acessar esta página."

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
        with open("data/users.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_users(users):
    """Salva usuários no arquivo JSON"""
    os.makedirs("data", exist_ok=True)
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def create_default_admin():
    """Cria o usuário administrador padrão (Matheus Gallina)"""
    users = load_users()

    # Verificar se já existe um admin
    admin_exists = any(user["role"] == "admin" for user in users)

    if not admin_exists:
        admin_user = {
            "id": "admin-001",
            "username": "admin",
            "name": "Matheus Gallina",
            "email": "matheus@velozfibra.com",
            "password_hash": generate_password_hash("B@rcelona1998"),
            "role": "admin",
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True,
        }
        users.append(admin_user)
        save_users(users)
        print("✅ Usuário administrador criado: Matheus Gallina")
    else:
        # Apenas atualizar a senha se for o usuário específico
        for user in users:
            if user["role"] == "admin" and user["username"] == "admin":
                # Só atualizar se a senha for diferente
                if not check_password_hash(user["password_hash"], "B@rcelona1998"):
                    user["password_hash"] = generate_password_hash("B@rcelona1998")
                    user["updated_at"] = datetime.now().isoformat()
                save_users(users)
                print("✅ Senha do administrador atualizada: B@rcelona1998")
                break


def log_activity(user_id, action, details=None):
    """Registra atividade do usuário"""
    log_entry = {
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": datetime.now().isoformat(),
        "ip_address": request.remote_addr,
    }

    try:
        with open("data/activity_log.json", encoding="utf-8") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)

    # Manter apenas os últimos 1000 logs
    if len(logs) > 1000:
        logs = logs[-1000:]

    with open("data/activity_log.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


@login_manager.user_loader
def load_user(user_id):
    """Carrega usuário para o Flask-Login"""
    users = load_users()
    user_data = next((u for u in users if u["id"] == user_id), None)
    if user_data and user_data.get("is_active", True):
        return User(
            user_data["id"],
            user_data["username"],
            user_data["name"],
            user_data["role"],
            user_data["created_at"],
        )
    return None


# Funções para gerenciar páginas (mantidas do código original)
def load_pages():
    """Carrega páginas do arquivo JSON"""
    try:
        with open("data/pages.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_pages(pages):
    """Salva páginas no arquivo JSON"""
    os.makedirs("data", exist_ok=True)
    with open("data/pages.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)


# Funções para gerenciar notificações
def load_notifications():
    """Carrega notificações do arquivo JSON"""
    try:
        with open("data/notifications.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_notifications(notifications):
    """Salva notificações no arquivo JSON"""
    os.makedirs("data", exist_ok=True)
    with open("data/notifications.json", "w", encoding="utf-8") as f:
        json.dump(notifications, f, ensure_ascii=False, indent=2)


def create_notification(
    user_id,
    title,
    message,
    notification_type="info",
    priority="normal",
    expires_at=None,
):
    """Cria uma nova notificação"""
    notification = {
        "id": f'notif-{datetime.now().strftime("%Y%m%d%H%M%S")}-{user_id}',
        "user_id": user_id,
        "title": title,
        "message": message,
        "type": notification_type,  # info, success, warning, error
        "priority": priority,  # low, normal, high, urgent
        "is_read": False,
        "created_at": datetime.now().isoformat(),
        "expires_at": expires_at,
        "action_url": None,
        "action_text": None,
    }

    notifications = load_notifications()
    notifications.append(notification)
    save_notifications(notifications)

    return notification


def get_user_notifications(user_id, include_read=False, limit=50):
    """Obtém notificações de um usuário"""
    notifications = load_notifications()
    user_notifications = []

    for notif in notifications:
        if notif["user_id"] == user_id:
            # Verificar se a notificação não expirou
            if notif.get("expires_at"):
                expires_at = datetime.fromisoformat(notif["expires_at"])
                if datetime.now() > expires_at:
                    continue

            if include_read or not notif["is_read"]:
                user_notifications.append(notif)

    # Ordenar por prioridade e data de criação
    user_notifications.sort(
        key=lambda x: (
            {"urgent": 4, "high": 3, "normal": 2, "low": 1}[x["priority"]],
            x["created_at"],
        ),
        reverse=True,
    )

    return user_notifications[:limit]


def mark_notification_as_read(notification_id):
    """Marca uma notificação como lida"""
    notifications = load_notifications()

    for notif in notifications:
        if notif["id"] == notification_id:
            notif["is_read"] = True
            notif["read_at"] = datetime.now().isoformat()
            save_notifications(notifications)
            return True

    return False


def mark_all_notifications_as_read(user_id):
    """Marca todas as notificações de um usuário como lidas"""
    notifications = load_notifications()
    updated = False

    for notif in notifications:
        if notif["user_id"] == user_id and not notif["is_read"]:
            notif["is_read"] = True
            notif["read_at"] = datetime.now().isoformat()
            updated = True

    if updated:
        save_notifications(notifications)

    return updated


def delete_notification(notification_id):
    """Deleta uma notificação"""
    notifications = load_notifications()

    for i, notif in enumerate(notifications):
        if notif["id"] == notification_id:
            del notifications[i]
            save_notifications(notifications)
            return True

    return False


def get_unread_count(user_id):
    """Obtém o número de notificações não lidas de um usuário"""
    notifications = get_user_notifications(user_id, include_read=False)
    return len(notifications)


def create_sample_data():
    """Cria dados de exemplo se não existirem"""
    # Criar setores padrão
    create_default_sectors()

    pages = load_pages()
    if not pages:
        sample_pages = [
            {
                "id": "visao-empresa",
                "title": "Visão da Empresa",
                "category": "visao-empresa",
                "content": "# Visão da Veloz Fibra\n\n## Nossa Missão\nFornecer internet de alta velocidade e qualidade para conectar pessoas e transformar comunidades.\n\n## Nossos Valores\n- **Qualidade**: Sempre entregar o melhor serviço possível\n- **Inovação**: Buscar constantemente novas tecnologias e soluções\n- **Confiança**: Construir relacionamentos duradouros com nossos clients\n- **Comunidade**: Contribuir para o desenvolvimento das regiões onde atuamos\n\n## Objetivos Estratégicos\n1. Expandir nossa cobertura de fibra óptica\n2. Manter a qualidade do atendimento ao cliente\n3. Investir em tecnologia e inovação\n4. Crescer de forma sustentável",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00",
            },
            {
                "id": "ferramentas-utilizadas",
                "title": "Ferramentas Utilizadas",
                "category": "ferramentas",
                "content": "# Ferramentas da Veloz Fibra\n\n## Gestão de Clients\n- **CRM**: Sistema próprio para gestão de clients\n- **WhatsApp Business**: Comunicação com clients\n- **Google Workspace**: Email e colaboração\n\n## Operational\n- **Sistema de Monitoramento**: Acompanhamento de rede\n- **App de Campo**: Para técnicos em campo\n- **Planilhas Google**: Controle de processors\n\n## Financeiro\n- **Sistema de Cobrança**: Integrado com CRM\n- **Controle de Caixa**: Gestão financeira\n- **Relatórios**: Análise de performance\n\n## Marketing\n- **Redes Sociais**: Instagram, Facebook\n- **Google Ads**: Publicidade online\n- **Site Institucional**: WordPress",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00",
            },
            {
                "id": "processors-internos",
                "title": "Processors Internos",
                "category": "processors",
                "content": "# Processors Internos\n\n## Atendimento ao Cliente\n1. **Recebimento da Solicitação**: Via WhatsApp, telefone ou presencial\n2. **Análise de Viabilidade**: Verificar cobertura na região\n3. **Agendamento**: Marcar instalação ou visita técnica\n4. **Execução**: Técnico realiza instalação\n5. **Acompanhamento**: Monitorar qualidade do serviço\n\n## Instalação de Novos Clients\n1. **Cadastro no Sistema**: Dados completos do cliente\n2. **Verificação de Cobertura**: Confirmar disponibilidade\n3. **Agendamento**: Definir data e horário\n4. **Instalação**: Técnico realiza conexão\n5. **Teste**: Verificar velocidade e estabilidade\n6. **Ativação**: Liberar acesso à internet\n\n## Manutenção\n1. **Identificação do Problema**: Cliente reporta ou sistema detecta\n2. **Análise**: Verificar se é problema de rede ou equipamento\n3. **Agendamento**: Marcar visita técnica se necessário\n4. **Resolução**: Técnico resolve o problema\n5. **Teste**: Confirmar funcionamento\n6. **Fechamento**: Registrar solução no sistema",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00",
            },
            {
                "id": "onboarding",
                "title": "Onboarding de Novos Colaboradores",
                "category": "onboarding",
                "content": "# Onboarding - Bem-vindo à Veloz Fibra!\n\n## Primeiro Dia\n1. **Apresentação**: Conhecer a equipe e a empresa\n2. **Acesso aos Sistemas**: Configurar logins e senhas\n3. **Tour pela Empresa**: Conhecer as instalações\n4. **Documentação**: Receber manual de procedimentos\n\n## Primeira Semana\n1. **Treinamento Técnico**: Aprender sobre produtos e serviços\n2. **Processors**: Entender fluxos de trabalho\n3. **Ferramentas**: Dominar sistemas utilizados\n4. **Expectativas**: Alinhar objetivos e metas\n\n## Primeiro Mês\n1. **Acompanhamento**: Mentor designado para dúvidas\n2. **Feedback**: Avaliação de desempenho\n3. **Integração**: Participar de reuniões e eventos\n4. **Independência**: Assumir responsabilidades\n\n## Recursos Disponíveis\n- Esta wiki para consulta\n- Manual de procedimentos\n- Contatos da equipe\n- Treinamentos online",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00",
            },
            {
                "id": "historico-mudancas",
                "title": "Histórico de Mudanças",
                "category": "historico",
                "content": "# Histórico de Mudanças e Decisões\n\n## Janeiro 2024\n- **15/01**: Implementação da wiki interna\n- **10/01**: Nova política de atendimento ao cliente\n- **05/01**: Atualização do sistema de monitoramento\n\n## Dezembro 2023\n- **20/12**: Expansão da cobertura para bairro novo\n- **15/12**: Contratação de 2 novos técnicos\n- **10/12**: Melhoria no sistema de cobrança\n\n## Novembro 2023\n- **25/11**: Implementação de nova ferramenta de CRM\n- **15/11**: Treinamento da equipe em novas tecnologias\n- **05/11**: Reestruturação do processo de instalação\n\n## Outubro 2023\n- **30/10**: Lançamento do novo plano de internet\n- **20/10**: Parceria com fornecedor de equipamentos\n- **10/10**: Melhoria na infraestrutura de rede",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00",
            },
            {
                "id": "novas-regras-comerciais",
                "title": "Novas Regras Comerciais",
                "category": "comercial",
                "content": "# Novas Regras Comerciais - Veloz Fibra\n\n## Vigência\n**A partir de 16/07/2025**\n\n## Equipe Responsável\nEquipe Comercial Veloz Fibra\n\n## Índice\n1. [Tipo de Consulta de CPF](#tipo-de-consulta-de-cpf)\n2. [Pontuação, Desconto e Elegibilidade](#pontuacao-desconto-e-elegibilidade)\n3. [Custo Comercial](#custo-comercial)\n4. [Prazo para Compromises](#prazo-para-compromises)\n5. [Tabela com Quantidade Desconto](#tabela-com-quantidade-desconto)\n6. [Novas Regras Base Pessoal](#novas-regras-base-pessoal)\n\n---\n\n### Tipo de Consulta de CPF\n*[Conteúdo a set adicionado]*\n\n### Pontuação, Desconto e Elegibilidade\n*[Conteúdo a set adicionado]*\n\n### Custo Comercial\n*[Conteúdo a set adicionado]*\n\n### Prazo para Compromises\n*[Conteúdo a set adicionado]*\n\n### Tabela com Quantidade Desconto\n*[Conteúdo a set adicionado]*\n\n### Novas Regras Base Pessoal\n*[Conteúdo a set adicionado]*\n\n---\n\n> **Nota**: Esta página será atualizada conforme o conteúdo da apresentação for disponibilizado.\n\n**Última atualização**: 15/01/2024",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00",
            },
        ]
        save_pages(sample_pages)
        return sample_pages
    return pages


# Funções para gerenciar PDFs e arquivos
def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_pdfs():
    """Carrega PDFs do arquivo JSON"""
    try:
        with open("data/pdfs.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_pdfs(pdfs):
    """Salva PDFs no arquivo JSON"""
    os.makedirs("data", exist_ok=True)
    with open("data/pdfs.json", "w", encoding="utf-8") as f:
        json.dump(pdfs, f, ensure_ascii=False, indent=2)


# Funções para gerenciar setores/áreas da empresa
def load_sectors():
    """Carrega setores do arquivo JSON"""
    try:
        with open("data/sectors.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_sectors(sectors):
    """Salva setores no arquivo JSON"""
    os.makedirs("data", exist_ok=True)
    with open("data/sectors.json", "w", encoding="utf-8") as f:
        json.dump(sectors, f, ensure_ascii=False, indent=2)


def create_default_sectors():
    """Cria setores padrão da empresa"""
    sectors = load_sectors()

    if not sectors:
        default_sectors = [
            {
                "id": "comercial",
                "name": "Comercial",
                "description": "Setor responsável por vendas e relacionamento com clients",
                "color": "blue",
                "icon": "fas fa-handshake",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "tecnico",
                "name": "Técnico",
                "description": "Setor responsável por instalação e manutenção técnica",
                "color": "green",
                "icon": "fas fa-tools",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "financeiro",
                "name": "Financeiro",
                "description": "Setor responsável por contabilidade e finanças",
                "color": "yellow",
                "icon": "fas fa-calculator",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "rh",
                "name": "Recursos Humanos",
                "description": "Setor responsável por gestão de pessoas",
                "color": "purple",
                "icon": "fas fa-users",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "administration",
                "name": "Administration",
                "description": "Setor responsável por administração geral",
                "color": "gray",
                "icon": "fas fa-building",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "marketing",
                "name": "Marketing",
                "description": "Setor responsável por marketing e comunicação",
                "color": "pink",
                "icon": "fas fa-bullhorn",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "ti",
                "name": "Tecnologia da Informação",
                "description": "Setor responsável por sistemas e tecnologia",
                "color": "indigo",
                "icon": "fas fa-laptop-code",
                "created_at": datetime.now().isoformat(),
            },
        ]

        sectors = default_sectors
        save_sectors(sectors)
        print("✅ Setores padrão criados")


def create_pdf_entry(
    filename,
    original_filename,
    sector_id=None,
    page_id=None,
    description="",
    training_date=None,
    trainer="",
):
    """Cria uma entrada de PDF com informações de setor e treinamento"""
    return {
        "id": str(uuid.uuid4()),
        "filename": filename,
        "original_filename": original_filename,
        "sector_id": sector_id,
        "page_id": page_id,
        "description": description,
        "training_date": training_date,
        "trainer": trainer,
        "uploaded_by": current_user.id,
        "uploaded_at": datetime.now().isoformat(),
        "file_size": os.path.getsize(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        ),
        "download_count": 0,
    }


def get_pdfs_by_sector(sector_id):
    """Retorna PDFs associados a um setor"""
    pdfs = load_pdfs()
    return [pdf for pdf in pdfs if pdf.get("sector_id") == sector_id]


def get_pdfs_by_page(page_id):
    """Retorna PDFs associados a uma página"""
    pdfs = load_pdfs()
    return [pdf for pdf in pdfs if pdf.get("page_id") == page_id]


def delete_pdf_file(pdf_id):
    """Remove arquivo PDF do sistema"""
    pdfs = load_pdfs()
    pdf = next((p for p in pdfs if p["id"] == pdf_id), None)
    if pdf:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf["filename"])
        if os.path.exists(file_path):
            os.remove(file_path)
        pdfs.remove(pdf)
        save_pdfs(pdfs)
        return True
    return False


# Rotas de autenticação
@app.route("/login", methods=["GET", "POST"])
def login():
    """Página de login"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()
        user_data = next((u for u in users if u["username"] == username), None)

        if user_data and check_password_hash(user_data["password_hash"], password):
            user = User(
                user_data["id"],
                user_data["username"],
                user_data["name"],
                user_data["role"],
                user_data["created_at"],
            )
            login_user(user)

            # Atualizar último login
            user_data["last_login"] = datetime.now().isoformat()
            save_users(users)

            # Registrar atividade
            log_activity(
                user_data["id"],
                "login",
                f'Login realizado por {user_data["name"]}',
            )

            flash(f'Bem-vindo, {user_data["name"]}!', "success")
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha incorretos.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Logout do usuário"""
    if current_user.is_authenticated:
        log_activity(
            current_user.id,
            "logout",
            f"Logout realizado por {current_user.name}",
        )
    logout_user()
    flash("Você foi desconectado.", "info")
    return redirect(url_for("login"))


@app.route("/admin/users")
@login_required
def admin_users():
    """Página de administração de usuários (apenas para admins)"""
    if not current_user.is_authenticated or current_user.role != "admin":
        flash(
            "Acesso negado. Apenas administradores podem acessar esta página.",
            "error",
        )
        return redirect(url_for("index"))

    users = load_users()
    return render_template("admin_users.html", users=users)


# Rotas para gerenciamento de usuários
@app.route("/api/users", methods=["POST"])
@login_required
def create_user():
    """Cria um novo usuário (apenas para admins)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()
    username = data.get("username")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not all([username, name, email, password]):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    users = load_users()

    # Verificar se username já existe
    if any(u["username"] == username for u in users):
        return jsonify({"error": "Nome de usuário já existe"}), 400

    # Verificar se email já existe
    if any(u.get("email") == email for u in users):
        return jsonify({"error": "Email já existe"}), 400

    # Criar novo usuário
    new_user = {
        "id": f"user-{len(users) + 1:03d}",
        "username": username,
        "name": name,
        "email": email,
        "password_hash": generate_password_hash(password),
        "role": role,
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "is_active": True,
    }

    users.append(new_user)
    save_users(users)

    log_activity(current_user.id, "create_user", f"Criou usuário: {name} ({username})")

    return (
        jsonify(
            {
                "message": "Usuário criado com sucesso",
                "user": {
                    "id": new_user["id"],
                    "username": new_user["username"],
                    "name": new_user["name"],
                    "email": new_user["email"],
                    "role": new_user["role"],
                    "created_at": new_user["created_at"],
                    "is_active": new_user["is_active"],
                },
            }
        ),
        201,
    )


@app.route("/api/users/<user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    """Atualiza um usuário (apenas para admins)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()
    users = load_users()

    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Atualizar campos
    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        # Verificar se email já existe em outro usuário
        if any(u.get("email") == data["email"] and u["id"] != user_id for u in users):
            return jsonify({"error": "Email já existe"}), 400
        user["email"] = data["email"]
    if "role" in data:
        user["role"] = data["role"]
    if "is_active" in data:
        user["is_active"] = data["is_active"]
    if "password" in data and data["password"]:
        user["password_hash"] = generate_password_hash(data["password"])

    user["updated_at"] = datetime.now().isoformat()
    save_users(users)

    log_activity(
        current_user.id,
        "update_user",
        f'Atualizou usuário: {user["name"]} ({user["username"]})',
    )

    return jsonify(
        {
            "message": "Usuário atualizado com sucesso",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "created_at": user["created_at"],
                "is_active": user["is_active"],
            },
        }
    )


@app.route("/api/users/<user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    """Deleta um usuário (apenas para admins)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    # Não permitir deletar o próprio usuário
    if current_user.id == user_id:
        return (
            jsonify({"error": "Não é possível deletar sua própria conta"}),
            400,
        )

    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Não permitir deletar o último admin
    if (
        user["role"] == "admin"
        and sum(1 for u in users if u["role"] == "admin" and u["is_active"]) <= 1
    ):
        return (
            jsonify({"error": "Não é possível deletar o último administrador"}),
            400,
        )

    user_name = user["name"]
    user_username = user["username"]

    users.remove(user)
    save_users(users)

    log_activity(
        current_user.id,
        "delete_user",
        f"Deletou usuário: {user_name} ({user_username})",
    )

    return jsonify({"message": "Usuário deletado com sucesso"})


@app.route("/api/users")
@login_required
def get_users():
    """Lista todos os usuários (apenas para admins)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    users = load_users()
    # Retornar dados sem senhas
    safe_users = []
    for user in users:
        safe_users.append(
            {
                "id": user["id"],
                "username": user["username"],
                "name": user["name"],
                "email": user.get("email", ""),
                "role": user["role"],
                "created_at": user["created_at"],
                "last_login": user.get("last_login"),
                "is_active": user.get("is_active", True),
            }
        )

    return jsonify(safe_users)


@app.route("/admin/activity")
@login_required
def admin_activity():
    """Página de log de atividades (apenas para admins)"""
    if not current_user.is_authenticated or current_user.role != "admin":
        flash(
            "Acesso negado. Apenas administradores podem acessar esta página.",
            "error",
        )
        return redirect(url_for("index"))

    try:
        with open("data/activity_log.json", encoding="utf-8") as f:
            activities = json.load(f)
    except FileNotFoundError:
        activities = []

    # Ordenar por timestamp (mais recente primeiro)
    activities.sort(key=lambda x: x["timestamp"], reverse=True)

    return render_template("admin_activity.html", activities=activities)


# Rotas da API (protegidas)
@app.route("/")
@login_required
def index():
    """Página principal (protegida)"""
    return render_template("index.html")


@app.route("/api/pages")
@login_required
def get_pages():
    """Retorna todas as páginas (protegida)"""
    pages = load_pages()
    log_activity(current_user.id, "api_access", "Acesso à API de páginas")
    return jsonify(pages)


@app.route("/api/pages/<page_id>")
@login_required
def get_page(page_id):
    """Retorna uma página específica (protegida)"""
    pages = load_pages()
    page = next((p for p in pages if p["id"] == page_id), None)
    if page:
        log_activity(
            current_user.id, "page_view", f'Visualizou página: {page["title"]}'
        )
        return jsonify(page)
    return jsonify({"error": "Página não encontrada"}), 404


@app.route("/api/pages", methods=["POST"])
@login_required
def create_page():
    """Cria uma nova página (protegida)"""
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Título é obrigatório"}), 400

    pages = load_pages()

    # Gerar ID único baseado no título
    page_id = slugify(data["title"])

    # Verificar se já existe
    if any(p["id"] == page_id for p in pages):
        page_id = f"{page_id}-{len(pages) + 1}"

    new_page = {
        "id": page_id,
        "title": data["title"],
        "category": data.get("category", "geral"),
        "content": data.get("content", ""),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "created_by": current_user.id,
        "created_by_name": current_user.name,
    }

    pages.append(new_page)
    save_pages(pages)

    log_activity(current_user.id, "page_create", f'Criou página: {data["title"]}')
    return jsonify(new_page), 201


@app.route("/api/pages/<page_id>", methods=["PUT"])
@login_required
def update_page(page_id):
    """Atualiza uma página existente (protegida)"""
    data = request.get_json()
    pages = load_pages()

    page_index = next((i for i, p in enumerate(pages) if p["id"] == page_id), None)

    if page_index is None:
        return jsonify({"error": "Página não encontrada"}), 404

    old_title = pages[page_index]["title"]
    pages[page_index].update(
        {
            "title": data.get("title", pages[page_index]["title"]),
            "category": data.get("category", pages[page_index]["category"]),
            "content": data.get("content", pages[page_index]["content"]),
            "updated_at": datetime.now().isoformat(),
            "updated_by": current_user.id,
            "updated_by_name": current_user.name,
        }
    )

    save_pages(pages)
    log_activity(current_user.id, "page_update", f"Atualizou página: {old_title}")
    return jsonify(pages[page_index])


@app.route("/api/pages/<page_id>", methods=["DELETE"])
@login_required
def delete_page(page_id):
    """Deleta uma página (protegida)"""
    pages = load_pages()
    page_to_delete = next((p for p in pages if p["id"] == page_id), None)

    if page_to_delete:
        log_activity(
            current_user.id,
            "page_delete",
            f'Deletou página: {page_to_delete["title"]}',
        )

    pages = [p for p in pages if p["id"] != page_id]
    save_pages(pages)
    return jsonify({"message": "Página deletada com sucesso"})


@app.route("/api/search")
@login_required
def search_pages():
    """Pesquisa páginas por thermo (protegida)"""
    query = request.args.get("q", "").lower()
    pages = load_pages()

    if not query:
        return jsonify(pages)

    results = []
    for page in pages:
        if (
            query in page["title"].lower()
            or query in page["content"].lower()
            or query in page["category"].lower()
        ):
            results.append(page)

    log_activity(current_user.id, "search", f"Pesquisou por: {query}")
    return jsonify(results)


@app.route("/api/categories")
@login_required
def get_categories():
    """Retorna todas as categorias (protegida)"""
    pages = load_pages()
    categories = list({page["category"] for page in pages})
    return jsonify(categories)


# Rotas para analytics e relatórios
@app.route("/admin/analytics")
@login_required
def admin_analytics():
    """Página de analytics para administradores"""
    if current_user.role != "admin":
        return redirect(url_for("index"))
    return render_template("admin_analytics.html")


@app.route("/admin/notifications")
@login_required
def admin_notifications():
    """Página de gerenciamento de notificações para administradores"""
    if current_user.role != "admin":
        return redirect(url_for("index"))
    return render_template("admin_notifications.html")


@app.route("/admin/pdfs")
@login_required
def admin_pdfs():
    """Página de gerenciamento de PDFs"""
    return render_template("admin_pdfs.html")


@app.route("/api/analytics/overview")
@login_required
def get_analytics_overview():
    """Retorna dados gerais de analytics"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    try:
        # Carregar dados
        pages = load_pages()
        users = load_users()

        # Tentar carregar logs de atividade
        try:
            with open("data/activity_log.json", encoding="utf-8") as f:
                activities = json.load(f)
        except FileNotFoundError:
            activities = []

        # Estatísticas gerais
        total_pages = len(pages)
        total_users = len(users)
        active_users = sum(1 for user in users if user.get("is_active", True))
        admin_users = sum(1 for user in users if user["role"] == "admin")

        # Atividades dos últimos 30 dias
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_activities = [
            activity
            for activity in activities
            if datetime.fromisoformat(activity["timestamp"]) > thirty_days_ago
        ]

        # Páginas mais acessadas (simulado baseado em visualizações)
        page_views = {}
        for activity in activities:
            if activity["action"] == "page_view":
                page_title = (
                    activity["details"].split(": ")[-1]
                    if ": " in activity["details"]
                    else "Página"
                )
                page_views[page_title] = page_views.get(page_title, 0) + 1

        top_pages = sorted(page_views.items(), key=lambda x: x[1], reverse=True)[:5]

        # Atividades por tipo
        activity_types = {}
        for activity in recent_activities:
            action = activity["action"]
            activity_types[action] = activity_types.get(action, 0) + 1

        # Usuários mais ativos
        user_activity = {}
        for activity in recent_activities:
            user_id = activity["user_id"]
            user_activity[user_id] = user_activity.get(user_id, 0) + 1

        # Encontrar gnomes dos usuários mais ativos
        top_users = []
        for user_id, count in sorted(
            user_activity.items(), key=lambda x: x[1], reverse=True
        )[:5]:
            user = next((u for u in users if u["id"] == user_id), None)
            if user:
                top_users.append(
                    {
                        "name": user["name"],
                        "username": user["username"],
                        "activity_count": count,
                    }
                )

        # Crescimento de páginas por mês
        pages_by_month = {}
        for page in pages:
            created_date = datetime.fromisoformat(page["created_at"])
            month_key = created_date.strftime("%Y-%m")
            pages_by_month[month_key] = pages_by_month.get(month_key, 0) + 1

        # Últimas atividades
        latest_activities = sorted(
            activities, key=lambda x: x["timestamp"], reverse=True
        )[:10]

        return jsonify(
            {
                "overview": {
                    "total_pages": total_pages,
                    "total_users": total_users,
                    "active_users": active_users,
                    "admin_users": admin_users,
                    "recent_activities": len(recent_activities),
                },
                "top_pages": [
                    {"title": title, "views": views} for title, views in top_pages
                ],
                "activity_types": activity_types,
                "top_users": top_users,
                "pages_by_month": pages_by_month,
                "latest_activities": latest_activities,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analytics/page-details")
@login_required
def get_page_analytics():
    """Retorna analytics detalhados das páginas"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    pages = load_pages()

    # Estatísticas por categoria
    categories = {}
    for page in pages:
        category = page["category"]
        if category not in categories:
            categories[category] = {"count": 0, "pages": []}
        categories[category]["count"] += 1
        categories[category]["pages"].append(
            {
                "id": page["id"],
                "title": page["title"],
                "created_at": page["created_at"],
                "updated_at": page["updated_at"],
            }
        )

    # Páginas mais recentes
    recent_pages = sorted(pages, key=lambda x: x["updated_at"], reverse=True)[:10]

    # Páginas por tamanho (aproximado)
    pages_by_size = []
    for page in pages:
        content_length = len(page["content"])
        size_category = (
            "Pequena"
            if content_length < 1000
            else "Média"
            if content_length < 5000
            else "Grande"
        )
        pages_by_size.append(
            {
                "title": page["title"],
                "size": size_category,
                "length": content_length,
            }
        )

    return jsonify(
        {
            "categories": categories,
            "recent_pages": recent_pages,
            "pages_by_size": pages_by_size,
        }
    )


@app.route("/api/analytics/user-details")
@login_required
def get_user_analytics():
    """Retorna analytics detalhados dos usuários"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    users = load_users()

    try:
        with open("data/activity_log.json", encoding="utf-8") as f:
            activities = json.load(f)
    except FileNotFoundError:
        activities = []

    # Atividade por usuário
    user_activity = {}
    for activity in activities:
        user_id = activity["user_id"]
        if user_id not in user_activity:
            user_activity[user_id] = {
                "total_actions": 0,
                "actions": {},
                "last_activity": None,
            }

        user_activity[user_id]["total_actions"] += 1
        action = activity["action"]
        user_activity[user_id]["actions"][action] = (
            user_activity[user_id]["actions"].get(action, 0) + 1
        )

        if (
            not user_activity[user_id]["last_activity"]
            or activity["timestamp"] > user_activity[user_id]["last_activity"]
        ):
            user_activity[user_id]["last_activity"] = activity["timestamp"]

    # Enriquecer com dados dos usuários
    detailed_users = []
    for user in users:
        user_id = user["id"]
        activity_data = user_activity.get(
            user_id, {"total_actions": 0, "actions": {}, "last_activity": None}
        )

        detailed_users.append(
            {
                "id": user["id"],
                "name": user["name"],
                "username": user["username"],
                "role": user["role"],
                "is_active": user.get("is_active", True),
                "created_at": user["created_at"],
                "last_login": user.get("last_login"),
                "total_actions": activity_data["total_actions"],
                "last_activity": activity_data["last_activity"],
                "actions": activity_data["actions"],
            }
        )

    # Usuários por função
    users_by_role = {}
    for user in users:
        role = user["role"]
        if role not in users_by_role:
            users_by_role[role] = {"count": 0, "users": []}
        users_by_role[role]["count"] += 1
        users_by_role[role]["users"].append(user["name"])

    return jsonify({"users": detailed_users, "users_by_role": users_by_role})


@app.route("/api/analytics/export")
@login_required
def export_analytics():
    """Exporta dados de analytics em CSV"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    try:
        pages = load_pages()
        users = load_users()

        with open("data/activity_log.json", encoding="utf-8") as f:
            activities = json.load(f)
    except FileNotFoundError:
        activities = []

    # Criar dados para exportação
    export_data = {
        "pages": pages,
        "users": users,
        "activities": activities,
        "export_date": datetime.now().isoformat(),
    }

    return jsonify(export_data)


# Rotas para o sistema de notificações
@app.route("/api/notifications")
@login_required
def get_notifications():
    """Retorna notificações do usuário atual"""
    try:
        include_read = request.args.get("include_read", "false").lower() == "true"
        limit = int(request.args.get("limit", 50))

        notifications = get_user_notifications(current_user.id, include_read, limit)

        return jsonify(
            {
                "notifications": notifications,
                "unread_count": get_unread_count(current_user.id),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/notifications/<notification_id>/read", methods=["POST"])
@login_required
def mark_notification_read(notification_id):
    """Marca uma notificação como lida"""
    try:
        success = mark_notification_as_read(notification_id)
        if success:
            return jsonify(
                {"success": True, "message": "Notificação marcada como lida"}
            )
        else:
            return jsonify({"error": "Notificação não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/notifications/read-all", methods=["POST"])
@login_required
def mark_all_notifications_read():
    """Marca todas as notificações do usuário como lidas"""
    try:
        mark_all_notifications_as_read(current_user.id)
        return jsonify(
            {
                "success": True,
                "message": "Todas as notificações foram marcadas como lidas",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/notifications/<notification_id>", methods=["DELETE"])
@login_required
def delete_notification_route(notification_id):
    """Deleta uma notificação"""
    try:
        success = delete_notification(notification_id)
        if success:
            return jsonify({"success": True, "message": "Notificação deletada"})
        else:
            return jsonify({"error": "Notificação não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/notifications/unread-count")
@login_required
def get_unread_count_route():
    """Retorna o número de notificações não lidas"""
    try:
        count = get_unread_count(current_user.id)
        return jsonify({"unread_count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para criar notificações (apenas admin)
@app.route("/api/notifications", methods=["POST"])
@login_required
def create_notification_route():
    """Cria uma nova notificação (apenas admin)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    try:
        data = request.get_json()
        user_id = data.get("user_id")
        title = data.get("title")
        message = data.get("message")
        notification_type = data.get("type", "info")
        priority = data.get("priority", "normal")
        expires_at = data.get("expires_at")
        action_url = data.get("action_url")
        action_text = data.get("action_text")

        if not user_id or not title or not message:
            return (
                jsonify({"error": "user_id, title e message são obrigatórios"}),
                400,
            )

        notification = create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            expires_at=expires_at,
        )

        # Adicionar action_url e action_text se fornecidos
        if action_url or action_text:
            notifications = load_notifications()
            for notif in notifications:
                if notif["id"] == notification["id"]:
                    notif["action_url"] = action_url
                    notif["action_text"] = action_text
                    save_notifications(notifications)
                    break

        return jsonify(
            {
                "success": True,
                "notification": notification,
                "message": "Notificação criada com sucesso",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Função para criar notificações automáticas
def create_automatic_notifications():
    """Cria notificações automáticas baseadas em eventos"""
    users = load_users()

    # Notificação de boas-vindas para novos usuários
    for user in users:
        if user.get("is_active", True):
            # Verificar se é um usuário novo (criado nas últimas 24h)
            created_at = datetime.fromisoformat(user["created_at"])
            if datetime.now() - created_at < timedelta(hours=24):
                # Verificar se já existe notificação de boas-vindas
                existing_notifications = get_user_notifications(
                    user["id"], include_read=True
                )
                welcome_exists = any(
                    "Bem-vindo" in notif["title"] for notif in existing_notifications
                )

                if not welcome_exists:
                    create_notification(
                        user_id=user["id"],
                        title="Bem-vindo à Wiki Veloz Fibra!",
                        message=f'Olá {user["name"]}! Bem-vindo à nossa central de conhecimento. Explore as páginas e descubra tudo sobre a Veloz Fibra.',
                        notification_type="success",
                        priority="normal",
                    )


# ============================================================================
# SISTEMA DE BACKUP E RESTAURAÇÃO
# ============================================================================


@app.route("/admin/backup")
@login_required
def admin_backup():
    """Página administrativa de backup"""
    if current_user.role != "admin":
        flash(
            "Acesso negado. Apenas administradores podem acessar esta página.", "error"
        )
        return redirect(url_for("index"))

    return render_template("admin_backup.html")


@app.route("/api/backup/create", methods=["POST"])
@login_required
def create_backup_route():
    """Cria um novo backup"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    if not BACKUP_SYSTEM_AVAILABLE:
        return jsonify({"error": "Sistema de backup não disponível"}), 500

    try:
        data = request.get_json() or {}
        description = data.get("description", "")

        result = backup_system.create_backup(description)

        if "error" in result:
            return jsonify({"error": result["error"]}), 500

        # Registrar atividade
        log_activity(
            current_user.id, "backup_created", f"Backup criado: {result['name']}"
        )

        return jsonify(
            {"success": True, "message": "Backup criado com sucesso", "backup": result}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/backup/list")
@login_required
def list_backups_route():
    """Lista todos os backups"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    if not BACKUP_SYSTEM_AVAILABLE:
        return jsonify({"error": "Sistema de backup não disponível"}), 500

    try:
        backups = backup_system.get_backups_list()
        return jsonify({"backups": backups})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/backup/<backup_id>/restore", methods=["POST"])
@login_required
def restore_backup_route(backup_id):
    """Restaura um backup"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    if not BACKUP_SYSTEM_AVAILABLE:
        return jsonify({"error": "Sistema de backup não disponível"}), 500

    try:
        result = backup_system.restore_backup(backup_id)

        if "error" in result:
            return jsonify({"error": result["error"]}), 500

        # Registrar atividade
        log_activity(
            current_user.id,
            "backup_restored",
            f"Backup restaurado: {result['backup_info']['name']}",
        )

        return jsonify(
            {
                "success": True,
                "message": "Backup restaurado com sucesso",
                "result": result,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/backup/<backup_id>/delete", methods=["DELETE"])
@login_required
def delete_backup_route(backup_id):
    """Remove um backup"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    if not BACKUP_SYSTEM_AVAILABLE:
        return jsonify({"error": "Sistema de backup não disponível"}), 500

    try:
        result = backup_system.delete_backup(backup_id)

        if "error" in result:
            return jsonify({"error": result["error"]}), 500

        # Registrar atividade
        log_activity(current_user.id, "backup_deleted", f"Backup removido: {backup_id}")

        return jsonify({"success": True, "message": "Backup removido com sucesso"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/backup/stats")
@login_required
def backup_stats_route():
    """Retorna estatísticas dos backups"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    if not BACKUP_SYSTEM_AVAILABLE:
        return jsonify({"error": "Sistema de backup não disponível"}), 500

    try:
        stats = backup_system.get_backup_stats()
        config = backup_system.config
        return jsonify({"stats": stats, "config": config})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/backup/config", methods=["GET", "PUT"])
@login_required
def backup_config_route():
    """Gerencia configurações do backup"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    if not BACKUP_SYSTEM_AVAILABLE:
        return jsonify({"error": "Sistema de backup não disponível"}), 500

    try:
        if request.method == "GET":
            return jsonify({"config": backup_system.config})

        elif request.method == "PUT":
            data = request.get_json()

            # Atualizar configurações
            for key, value in data.items():
                if key in backup_system.config:
                    backup_system.config[key] = value

            backup_system.save_config()

            return jsonify(
                {
                    "success": True,
                    "message": "Configurações atualizadas",
                    "config": backup_system.config,
                }
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/backup/google-drive/setup", methods=["POST"])
@login_required
def setup_google_drive_route():
    """Configura integração com Google Drive"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    if not BACKUP_SYSTEM_AVAILABLE:
        return jsonify({"error": "Sistema de backup não disponível"}), 500

    try:
        data = request.get_json() or {}
        credentials_file = data.get("credentials_file", "credentials.json")

        # Verificar se o arquivo de credenciais existe
        if not os.path.exists(credentials_file):
            error_msg = (
                f"Arquivo de credenciais '{credentials_file}' não encontrado. "
                f"Baixe o arquivo credentials.json do Google Cloud Console e "
                f"coloque na raiz do projeto. Veja o arquivo "
                f"CREDENCIAIS_GOOGLE_DRIVE.md para instruções."
            )
            return jsonify({"error": error_msg}), 400

        success = backup_system.setup_google_drive(credentials_file)

        if success:
            # Registrar atividade
            log_activity(
                current_user.id,
                "google_drive_configured",
                "Google Drive configurado com sucesso",
            )

            success_msg = (
                "Google Drive configurado com sucesso! "
                "Os próximos backups serão enviados automaticamente para o Google Drive."
            )
            return jsonify({"success": True, "message": success_msg})
        else:
            error_msg = (
                "Error ao configurar Google Drive. "
                "Verifique se o arquivo credentials.json está correto e se a "
                "Google Drive API está ativada."
            )
            return jsonify({"error": error_msg}), 500

    except Exception as e:
        return jsonify({"error": f"Error ao configurar Google Drive: {str(e)}"}), 500


# Rotas para gerenciamento de setores
@app.route("/api/sectors", methods=["GET"])
@login_required
def get_sectors():
    """Retorna lista de setores"""
    sectors = load_sectors()
    return jsonify({"sectors": sectors})


@app.route("/api/sectors", methods=["POST"])
@login_required
def create_sector():
    """Cria um novo setor (apenas para admins)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    color = data.get("color", "gray")
    icon = data.get("icon", "fas fa-folder")

    if not name:
        return jsonify({"error": "Nome do setor é obrigatório"}), 400

    sectors = load_sectors()

    # Verificar se já existe um setor com este nome
    if any(s["name"].lower() == name.lower() for s in sectors):
        return jsonify({"error": "Setor já existe"}), 400

    # Criar novo setor
    new_sector = {
        "id": slugify(name),
        "name": name,
        "description": description,
        "color": color,
        "icon": icon,
        "created_at": datetime.now().isoformat(),
        "created_by": current_user.id,
    }

    sectors.append(new_sector)
    save_sectors(sectors)

    log_activity(current_user.id, "create_sector", f"Criou setor: {name}")

    return (
        jsonify(
            {
                "success": True,
                "message": "Setor criado com sucesso",
                "sector": new_sector,
            }
        ),
        201,
    )


@app.route("/api/sectors/<sector_id>", methods=["PUT"])
@login_required
def update_sector(sector_id):
    """Atualiza um setor (apenas para admins)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()
    sectors = load_sectors()

    sector = next((s for s in sectors if s["id"] == sector_id), None)
    if not sector:
        return jsonify({"error": "Setor não encontrado"}), 404

    # Atualizar campos
    if "name" in data:
        sector["name"] = data["name"]
    if "description" in data:
        sector["description"] = data["description"]
    if "color" in data:
        sector["color"] = data["color"]
    if "icon" in data:
        sector["icon"] = data["icon"]

    sector["updated_at"] = datetime.now().isoformat()
    sector["updated_by"] = current_user.id

    save_sectors(sectors)

    log_activity(current_user.id, "update_sector", f"Atualizou setor: {sector['name']}")

    return jsonify(
        {"success": True, "message": "Setor atualizado com sucesso", "sector": sector}
    )


@app.route("/api/sectors/<sector_id>", methods=["DELETE"])
@login_required
def delete_sector(sector_id):
    """Remove um setor (apenas para admins)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    sectors = load_sectors()
    sector = next((s for s in sectors if s["id"] == sector_id), None)

    if not sector:
        return jsonify({"error": "Setor não encontrado"}), 404

    # Verificar se há PDFs associados a este setor
    pdfs = load_pdfs()
    sector_pdfs = [pdf for pdf in pdfs if pdf.get("sector_id") == sector_id]

    if sector_pdfs:
        return (
            jsonify(
                {
                    "error": f"Não é possível excluir o setor. Existem {len(sector_pdfs)} PDFs associados."
                }
            ),
            400,
        )

    sectors.remove(sector)
    save_sectors(sectors)

    log_activity(current_user.id, "delete_sector", f"Removeu setor: {sector['name']}")

    return jsonify({"success": True, "message": "Setor removido com sucesso"})


# Rotas para gerenciamento de PDFs (modificadas para incluir setores)
@app.route("/api/pdfs", methods=["GET"])
@login_required
def get_pdfs():
    """Retorna lista de PDFs com filtros por setor e página"""
    sector_id = request.args.get("sector_id")
    page_id = request.args.get("page_id")
    pdfs = load_pdfs()

    if sector_id:
        pdfs = [pdf for pdf in pdfs if pdf.get("sector_id") == sector_id]

    if page_id:
        pdfs = [pdf for pdf in pdfs if pdf.get("page_id") == page_id]

    return jsonify({"pdfs": pdfs})


@app.route("/api/pdfs", methods=["POST"])
@login_required
def upload_pdf():
    """Faz upload de um PDF com informações de setor e treinamento"""
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Tipo de arquivo não permitido"}), 400

    # Gerar nome único para o arquivo
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    # Salvar arquivo
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    file.save(file_path)

    # Obter dados do formulário
    sector_id = request.form.get("sector_id")
    page_id = request.form.get("page_id")
    description = request.form.get("description", "")
    training_date = request.form.get("training_date")
    trainer = request.form.get("trainer", "")

    # Validar setor se fornecido
    if sector_id:
        sectors = load_sectors()
        sector = next((s for s in sectors if s["id"] == sector_id), None)
        if not sector:
            return jsonify({"error": "Setor inválido"}), 400

    # Criar entrada no banco
    pdf_entry = create_pdf_entry(
        unique_filename,
        filename,
        sector_id,
        page_id,
        description,
        training_date,
        trainer,
    )

    pdfs = load_pdfs()
    pdfs.append(pdf_entry)
    save_pdfs(pdfs)

    # Registrar atividade
    sector_name = "Sem setor"
    if sector_id:
        sectors = load_sectors()
        sector = next((s for s in sectors if s["id"] == sector_id), None)
        if sector:
            sector_name = sector["name"]

    log_activity(
        current_user.id,
        "pdf_uploaded",
        f"PDF enviado: {filename} para setor: {sector_name}",
    )

    return jsonify(
        {"success": True, "message": "PDF enviado com sucesso", "pdf": pdf_entry}
    )


@app.route("/api/pdfs/<pdf_id>", methods=["DELETE"])
@login_required
def delete_pdf(pdf_id):
    """Remove um PDF"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403

    success = delete_pdf_file(pdf_id)

    if success:
        # Registrar atividade
        log_activity(current_user.id, "pdf_deleted", f"PDF removido: {pdf_id}")

        return jsonify({"success": True, "message": "PDF removido com sucesso"})
    else:
        return jsonify({"error": "PDF não encontrado"}), 404


@app.route("/uploads/<filename>")
@login_required
def download_file(filename):
    """Download de arquivo"""
    try:
        # Verificar se o arquivo existe
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "Arquivo não encontrado"}), 404

        # Incrementar contador de downloads
        pdfs = load_pdfs()
        pdf = next((p for p in pdfs if p["filename"] == filename), None)
        if pdf:
            pdf["download_count"] += 1
            save_pdfs(pdfs)

        return send_from_directory(
            app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pdfs/<pdf_id>/view")
@login_required
def view_pdf(pdf_id):
    """Visualiza um PDF"""
    pdfs = load_pdfs()
    pdf = next((p for p in pdfs if p["id"] == pdf_id), None)

    if not pdf:
        return jsonify({"error": "PDF não encontrado"}), 404

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf["filename"])
    if not os.path.exists(file_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404

    return send_from_directory(
        app.config["UPLOAD_FOLDER"], pdf["filename"], mimetype="application/pdf"
    )


@app.route("/api/editor/upload", methods=["POST"])
@login_required
def upload_editor_file():
    """Faz upload de arquivos para o editor de páginas"""
    try:
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Nenhum arquivo selecionado"}), 400

        # Verificar extensão do arquivo
        allowed_extensions = {
            "png",
            "jpg",
            "jpeg",
            "gif",
            "webp",  # Imagens
            "pdf",
            "doc",
            "docx",
            "txt",
            "md",  # Documentos
            "mp4",
            "avi",
            "mov",
            "wmv",  # Vídeos
            "mp3",
            "wav",
            "ogg",  # Áudios
        }

        file_ext = (
            file.filename.rsplit(".", 1)[1].lower() if "." in file.filename else ""
        )
        if file_ext not in allowed_extensions:
            return (
                jsonify(
                    {
                        "error": f"Tipo de arquivo não permitido. Permitidos: {', '.join(allowed_extensions)}"
                    }
                ),
                400,
            )

        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"editor_{timestamp}_{secure_filename(file.filename)}"

        # Salvar arquivo
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        file.save(file_path)

        # Retornar informações do arquivo
        file_info = {
            "filename": unique_filename,
            "original_name": file.filename,
            "url": f"/uploads/{unique_filename}",
            "size": os.path.getsize(file_path),
            "type": file_ext,
            "uploaded_at": datetime.now().isoformat(),
        }

        # Log da atividade
        log_activity(
            current_user.id,
            "file_uploaded",
            f"Arquivo enviado via editor: {file.filename}",
            {"filename": unique_filename, "type": file_ext},
        )

        return jsonify(file_info), 200

    except Exception as e:
        app.logger.error(f"Error no upload do editor: {str(e)}")
        return jsonify({"error": "Error interno do servidor"}), 500


if __name__ == "__main__":
    # Criar dados de exemplo e usuário admin na primeira execução
    create_sample_data()
    create_default_admin()
    create_automatic_notifications()

    # Inicializar sistema de backup se disponível
    if BACKUP_SYSTEM_AVAILABLE:
        init_backup_system()

    app.run(debug=True, host="0.0.0.0", port=8000)
