"""
Serviço de negócio para documentos corporations
"""
import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import (
    Document,
    DocumentCategory,
    DocumentPriority,
    DocumentStatus,
    DocumentType,
    DocumentVersion,
)
from .repositories import (
    DocumentCategoryRepository,
    DocumentRepository,
    DocumentVersionRepository,
)


class DocumentService:
    """Serviço de negócio para documentos corporations"""

    def __init__(self):
        self.repository = DocumentRepository()
        self.category_repository = DocumentCategoryRepository()
        self.version_repository = DocumentVersionRepository()
        self.analytics_file = "data/document_analytics.json"
        self._load_analytics()

    def _load_analytics(self):
        """Carrega dados de analytics do arquivo JSON"""
        try:
            with open(self.analytics_file, encoding="utf-8") as f:
                self.analytics = json.load(f)
        except FileNotFoundError:
            self.analytics = {
                "views": {},
                "downloads": {},
                "daily_stats": {},
                "category_stats": {},
                "type_stats": {},
                "user_activity": {},
            }
            self._save_analytics()

    def _save_analytics(self):
        """Salva dados de analytics no arquivo JSON"""
        with open(self.analytics_file, "w", encoding="utf-8") as f:
            json.dump(self.analytics, f, indent=2, ensure_ascii=False, default=str)

    def create_document(self, data: dict[str, Any]) -> Document:
        """Cria um novo documento"""
        document = Document(
            id=str(uuid.uuid4()),
            title=data["title"],
            description=data.get("description", ""),
            category_id=data["category_id"],
            type=data["type"],
            status=data.get("status", "ativo"),
            priority=data.get("priority", "media"),
            content=data.get("content", ""),
            author=data.get("author", "Sistema"),
            version=1,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        # Criar versão inicial
        version = DocumentVersion(
            id=str(uuid.uuid4()),
            document_id=document.id,
            version=1,
            changes="Versão inicial",
            author=document.author,
            created_at=document.created_at,
        )

        self.repository.create(document)
        self.version_repository.create(version)

        # Inicializar analytics
        self.analytics["views"][document.id] = 0
        self.analytics["downloads"][document.id] = 0
        self._save_analytics()

        return document

    def update_document(
        self, document_id: str, data: dict[str, Any]
    ) -> Optional[Document]:
        """Atualiza um documento existente"""
        document = self.repository.get_by_id(document_id)
        if not document:
            return None

        # Criar nova versão se houver mudanças
        has_changes = any(
            getattr(document, field) != data.get(field, getattr(document, field))
            for field in ["title", "description", "content", "status", "priority"]
        )

        if has_changes:
            # Incrementar versão
            latest_version = self.version_repository.get_latest_version(document_id)
            new_version_number = (latest_version.version + 1) if latest_version else 1

            version = DocumentVersion(
                id=str(uuid.uuid4()),
                document_id=document_id,
                version=new_version_number,
                changes=data.get("changes", "Atualização de documento"),
                author=data.get("author", "Sistema"),
                created_at=datetime.now().isoformat(),
            )

            self.version_repository.create(version)
            document.version = new_version_number

        # Atualizar documento
        for field, value in data.items():
            if hasattr(document, field):
                setattr(document, field, value)

        document.updated_at = datetime.now().isoformat()
        self.repository.update(document)

        return document

    def delete_document(self, document_id: str) -> bool:
        """Exclui um documento"""
        # Remover analytics
        if document_id in self.analytics["views"]:
            del self.analytics["views"][document_id]
        if document_id in self.analytics["downloads"]:
            del self.analytics["downloads"][document_id]
        self._save_analytics()

        return self.repository.delete(document_id)

    def get_document(self, document_id: str) -> Optional[Document]:
        """Obtém um documento por ID"""
        return self.repository.get_by_id(document_id)

    def get_all_documents(self) -> list[Document]:
        """Obtém todos os documentos"""
        return self.repository.get_all()

    def get_documents_by_category(self, category_id: str) -> list[Document]:
        """Obtém documentos por categoria"""
        return self.repository.get_by_category(category_id)

    def get_documents_by_type(self, document_type: str) -> list[Document]:
        """Obtém documentos por tipo"""
        return self.repository.get_by_type(document_type)

    def get_documents_by_status(self, status: str) -> list[Document]:
        """Obtém documentos por status"""
        return self.repository.get_by_status(status)

    def search_documents(self, query: str) -> list[Document]:
        """Busca documentos por texto"""
        return self.repository.search(query)

    def get_document_versions(self, document_id: str) -> list[DocumentVersion]:
        """Obtém todas as versões de um documento"""
        return self.version_repository.get_by_document_id(document_id)

    def get_latest_version(self, document_id: str) -> Optional[DocumentVersion]:
        """Obtém a versão mais recente de um documento"""
        return self.version_repository.get_latest_version(document_id)

    def create_category(self, data: dict[str, Any]) -> DocumentCategory:
        """Cria uma nova categoria"""
        category = DocumentCategory(
            id=str(uuid.uuid4()),
            name=data["name"],
            description=data.get("description", ""),
            color=data.get("color", "#3b82f6"),
            created_at=datetime.now().isoformat(),
        )
        self.category_repository.create(category)
        return category

    def get_all_categories(self) -> list[DocumentCategory]:
        """Obtém todas as categorias"""
        return self.category_repository.get_all()

    def get_category(self, category_id: str) -> Optional[DocumentCategory]:
        """Obtém uma categoria por ID"""
        return self.category_repository.get_by_id(category_id)

    def update_category(
        self, category_id: str, data: dict[str, Any]
    ) -> Optional[DocumentCategory]:
        """Atualiza uma categoria"""
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return None

        for field, value in data.items():
            if hasattr(category, field):
                setattr(category, field, value)

        self.category_repository.update(category)
        return category

    def delete_category(self, category_id: str) -> bool:
        """Exclui uma categoria"""
        return self.category_repository.delete(category_id)

    # Métricas e Analytics
    def record_view(self, document_id: str, user_id: str = None) -> None:
        """Registra uma visualização de documento"""
        if document_id not in self.analytics["views"]:
            self.analytics["views"][document_id] = 0
        self.analytics["views"][document_id] += 1

        # Registrar atividade diária
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.analytics["daily_stats"]:
            self.analytics["daily_stats"][today] = {"views": 0, "downloads": 0}
        self.analytics["daily_stats"][today]["views"] += 1

        # Registrar atividade do usuário
        if user_id:
            if user_id not in self.analytics["user_activity"]:
                self.analytics["user_activity"][user_id] = {
                    "views": {},
                    "downloads": {},
                }
            if document_id not in self.analytics["user_activity"][user_id]["views"]:
                self.analytics["user_activity"][user_id]["views"][document_id] = 0
            self.analytics["user_activity"][user_id]["views"][document_id] += 1

        self._save_analytics()

    def record_download(self, document_id: str, user_id: str = None) -> None:
        """Registra um download de documento"""
        if document_id not in self.analytics["downloads"]:
            self.analytics["downloads"][document_id] = 0
        self.analytics["downloads"][document_id] += 1

        # Registrar atividade diária
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.analytics["daily_stats"]:
            self.analytics["daily_stats"][today] = {"views": 0, "downloads": 0}
        self.analytics["daily_stats"][today]["downloads"] += 1

        # Registrar atividade do usuário
        if user_id:
            if user_id not in self.analytics["user_activity"]:
                self.analytics["user_activity"][user_id] = {
                    "views": {},
                    "downloads": {},
                }
            if document_id not in self.analytics["user_activity"][user_id]["downloads"]:
                self.analytics["user_activity"][user_id]["downloads"][document_id] = 0
            self.analytics["user_activity"][user_id]["downloads"][document_id] += 1

        self._save_analytics()

    def get_document_analytics(self, document_id: str) -> dict[str, Any]:
        """Obtém analytics de um documento específico"""
        views = self.analytics["views"].get(document_id, 0)
        downloads = self.analytics["downloads"].get(document_id, 0)

        return {
            "document_id": document_id,
            "views": views,
            "downloads": downloads,
            "engagement_rate": (downloads / views * 100) if views > 0 else 0,
        }

    def get_dashboard_stats(self) -> dict[str, Any]:
        """Obtém estatísticas para o dashboard"""
        documents = self.get_all_documents()
        categories = self.get_all_categories()

        # Estatísticas básicas
        total_documents = len(documents)
        total_views = sum(self.analytics["views"].values())
        total_downloads = sum(self.analytics["downloads"].values())

        # Estatísticas por status
        status_stats = {}
        for status in DocumentStatus:
            status_docs = [d for d in documents if d.status == status.value]
            status_stats[status.value] = len(status_docs)

        # Estatísticas por categoria
        category_stats = {}
        for category in categories:
            category_docs = [d for d in documents if d.category_id == category.id]
            category_stats[category.name] = {
                "count": len(category_docs),
                "views": sum(
                    self.analytics["views"].get(d.id, 0) for d in category_docs
                ),
                "downloads": sum(
                    self.analytics["downloads"].get(d.id, 0) for d in category_docs
                ),
            }

        # Estatísticas por tipo
        type_stats = {}
        for doc_type in DocumentType:
            type_docs = [d for d in documents if d.type == doc_type.value]
            type_stats[doc_type.value] = {
                "count": len(type_docs),
                "views": sum(self.analytics["views"].get(d.id, 0) for d in type_docs),
                "downloads": sum(
                    self.analytics["downloads"].get(d.id, 0) for d in type_docs
                ),
            }

        # Documentos mais populares
        popular_documents = []
        for doc in documents:
            views = self.analytics["views"].get(doc.id, 0)
            downloads = self.analytics["downloads"].get(doc.id, 0)
            if views > 0 or downloads > 0:
                popular_documents.append(
                    {
                        "id": doc.id,
                        "title": doc.title,
                        "views": views,
                        "downloads": downloads,
                        "engagement_rate": (downloads / views * 100)
                        if views > 0
                        else 0,
                    }
                )

        # Ordenar por engajamento
        popular_documents.sort(key=lambda x: x["engagement_rate"], reverse=True)

        # Atividade recente (últimos 7 dias)
        recent_activity = {}
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            if date in self.analytics["daily_stats"]:
                recent_activity[date] = self.analytics["daily_stats"][date]

        return {
            "total_documents": total_documents,
            "total_views": total_views,
            "total_downloads": total_downloads,
            "status_stats": status_stats,
            "category_stats": category_stats,
            "type_stats": type_stats,
            "popular_documents": popular_documents[:10],  # Top 10
            "recent_activity": recent_activity,
        }

    def get_user_analytics(self, user_id: str) -> dict[str, Any]:
        """Obtém analytics de um usuário específico"""
        if user_id not in self.analytics["user_activity"]:
            return {
                "user_id": user_id,
                "total_views": 0,
                "total_downloads": 0,
                "viewed_documents": [],
                "downloaded_documents": [],
            }

        user_data = self.analytics["user_activity"][user_id]
        total_views = sum(user_data["views"].values())
        total_downloads = sum(user_data["downloads"].values())

        # Documentos visualizados
        viewed_documents = []
        for doc_id, views in user_data["views"].items():
            doc = self.get_document(doc_id)
            if doc:
                viewed_documents.append(
                    {
                        "id": doc_id,
                        "title": doc.title,
                        "views": views,
                        "last_viewed": datetime.now().isoformat(),  # Simplificado
                    }
                )

        # Documentos baixados
        downloaded_documents = []
        for doc_id, downloads in user_data["downloads"].items():
            doc = self.get_document(doc_id)
            if doc:
                downloaded_documents.append(
                    {
                        "id": doc_id,
                        "title": doc.title,
                        "downloads": downloads,
                        "last_downloaded": datetime.now().isoformat(),  # Simplificado
                    }
                )

        return {
            "user_id": user_id,
            "total_views": total_views,
            "total_downloads": total_downloads,
            "viewed_documents": viewed_documents,
            "downloaded_documents": downloaded_documents,
        }

    def generate_report(
        self, report_type: str, filters: dict[str, Any] = None
    ) -> dict[str, Any]:
        """Gera relatórios personalizados"""
        if report_type == "daily":
            return self._generate_daily_report(filters)
        elif report_type == "category":
            return self._generate_category_report(filters)
        elif report_type == "user":
            return self._generate_user_report(filters)
        elif report_type == "popular":
            return self._generate_popular_report(filters)
        else:
            return {"error": "Tipo de relatório não suportado"}

    def _generate_daily_report(self, filters: dict[str, Any] = None) -> dict[str, Any]:
        """Gera relatório diário"""
        days = filters.get("days", 30) if filters else 30
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        daily_data = []
        for i in range(days):
            date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            if date in self.analytics["daily_stats"]:
                daily_data.append({"date": date, **self.analytics["daily_stats"][date]})
            else:
                daily_data.append({"date": date, "views": 0, "downloads": 0})

        return {"report_type": "daily", "period": f"{days} dias", "data": daily_data}

    def _generate_category_report(
        self, filters: dict[str, Any] = None
    ) -> dict[str, Any]:
        """Gera relatório por categoria"""
        categories = self.get_all_categories()
        category_data = []

        for category in categories:
            category_docs = self.get_documents_by_category(category.id)
            total_views = sum(
                self.analytics["views"].get(d.id, 0) for d in category_docs
            )
            total_downloads = sum(
                self.analytics["downloads"].get(d.id, 0) for d in category_docs
            )

            category_data.append(
                {
                    "category_id": category.id,
                    "category_name": category.name,
                    "document_count": len(category_docs),
                    "total_views": total_views,
                    "total_downloads": total_downloads,
                    "avg_views_per_doc": total_views / len(category_docs)
                    if category_docs
                    else 0,
                    "avg_downloads_per_doc": total_downloads / len(category_docs)
                    if category_docs
                    else 0,
                }
            )

        return {"report_type": "category", "data": category_data}

    def _generate_user_report(self, filters: dict[str, Any] = None) -> dict[str, Any]:
        """Gera relatório por usuário"""
        user_data = []

        for user_id, activity in self.analytics["user_activity"].items():
            total_views = sum(activity["views"].values())
            total_downloads = sum(activity["downloads"].values())

            user_data.append(
                {
                    "user_id": user_id,
                    "total_views": total_views,
                    "total_downloads": total_downloads,
                    "unique_documents_viewed": len(activity["views"]),
                    "unique_documents_downloaded": len(activity["downloads"]),
                }
            )

        # Ordenar por atividade
        user_data.sort(
            key=lambda x: x["total_views"] + x["total_downloads"], reverse=True
        )

        return {"report_type": "user", "data": user_data}

    def _generate_popular_report(
        self, filters: dict[str, Any] = None
    ) -> dict[str, Any]:
        """Gera relatório de documentos populares"""
        documents = self.get_all_documents()
        popular_data = []

        for doc in documents:
            views = self.analytics["views"].get(doc.id, 0)
            downloads = self.analytics["downloads"].get(doc.id, 0)

            if views > 0 or downloads > 0:
                popular_data.append(
                    {
                        "document_id": doc.id,
                        "title": doc.title,
                        "category": self.get_category(doc.category_id).name
                        if self.get_category(doc.category_id)
                        else "N/A",
                        "type": doc.type,
                        "status": doc.status,
                        "views": views,
                        "downloads": downloads,
                        "engagement_rate": (downloads / views * 100)
                        if views > 0
                        else 0,
                        "created_at": doc.created_at,
                        "updated_at": doc.updated_at,
                    }
                )

        # Ordenar por engajamento
        popular_data.sort(key=lambda x: x["engagement_rate"], reverse=True)

        return {"report_type": "popular", "data": popular_data}
