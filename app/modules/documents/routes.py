"""
Rotas para documentos corporativos
"""
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from .models import DocumentPriority, DocumentStatus, DocumentType
from .services import DocumentService

# Criar blueprint
documents_bp = Blueprint('documents', __name__, url_prefix='/documents')
service = DocumentService()


@documents_bp.route('/')
@login_required
def documents_index():
    """Página principal de documentos"""
    return render_template('documents/index.html')


@documents_bp.route('/create')
@login_required
def documents_create():
    """Página de criação de documento"""
    categories = service.get_categories()
    return render_template('documents/create.html', categories=categories)


@documents_bp.route('/<document_id>')
@login_required
def documents_view(document_id):
    """Página de visualização de documento"""
    document = service.get_document(document_id)
    if not document:
        return jsonify({'error': 'Documento não encontrado'}), 404
    
    category = service.get_category(document.category_id)
    versions = service.get_document_versions(document_id)
    
    return render_template('documents/view.html', 
                         document=document, 
                         category=category,
                         versions=versions)


@documents_bp.route('/<document_id>/edit')
@login_required
def documents_edit(document_id):
    """Página de edição de documento"""
    document = service.get_document(document_id)
    if not document:
        return jsonify({'error': 'Documento não encontrado'}), 404
    
    categories = service.get_categories()
    return render_template('documents/edit.html', 
                         document=document, 
                         categories=categories)


# API Routes
@documents_bp.route('/api/documents', methods=['GET'])
@login_required
def get_documents():
    """API: Lista documentos com filtros"""
    try:
        filters = {}
        
        # Filtros opcionais
        if request.args.get('category_id'):
            filters['category_id'] = request.args.get('category_id')
        
        if request.args.get('document_type'):
            filters['document_type'] = request.args.get('document_type')
        
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        
        if request.args.get('priority'):
            filters['priority'] = request.args.get('priority')
        
        if request.args.get('featured'):
            filters['featured'] = request.args.get('featured') == 'true'
        
        if request.args.get('author_id'):
            filters['author_id'] = request.args.get('author_id')
        
        # Ordenação
        if request.args.get('sort_by'):
            filters['sort_by'] = request.args.get('sort_by')
        
        if request.args.get('reverse'):
            filters['reverse'] = request.args.get('reverse') == 'true'
        
        documents = service.get_all_documents(filters)
        
        return jsonify({
            'success': True,
            'data': [doc.to_dict() for doc in documents]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@documents_bp.route('/api/documents', methods=['POST'])
@login_required
def create_document():
    """API: Cria novo documento"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        document = service.create_document(
            data=data,
            author_id=current_user.id,
            author_name=current_user.name
        )
        
        return jsonify({
            'success': True,
            'data': document.to_dict(),
            'message': 'Documento criado com sucesso'
        }), 201
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/<document_id>', methods=['GET'])
@login_required
def get_document(document_id):
    """API: Busca documento por ID"""
    try:
        document = service.get_document(document_id)
        
        if not document:
            return jsonify({
                'success': False,
                'message': 'Documento não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': document.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/<document_id>', methods=['PUT'])
@login_required
def update_document(document_id):
    """API: Atualiza documento"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        document = service.update_document(
            document_id=document_id,
            data=data,
            user_id=current_user.id
        )
        
        return jsonify({
            'success': True,
            'data': document.to_dict(),
            'message': 'Documento atualizado com sucesso'
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/<document_id>', methods=['DELETE'])
@login_required
def delete_document(document_id):
    """API: Remove documento"""
    try:
        success = service.delete_document(document_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Documento não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Documento removido com sucesso'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/search', methods=['GET'])
@login_required
def search_documents():
    """API: Busca documentos por texto"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Query de busca não fornecida'
            }), 400
        
        documents = service.search_documents(query)
        
        return jsonify({
            'success': True,
            'data': [doc.to_dict() for doc in documents]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/featured', methods=['GET'])
@login_required
def get_featured_documents():
    """API: Busca documentos em destaque"""
    try:
        documents = service.get_featured_documents()
        
        return jsonify({
            'success': True,
            'data': [doc.to_dict() for doc in documents]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/recent', methods=['GET'])
@login_required
def get_recent_documents():
    """API: Busca documentos recentes"""
    try:
        limit = int(request.args.get('limit', 10))
        documents = service.get_recent_documents(limit)
        
        return jsonify({
            'success': True,
            'data': [doc.to_dict() for doc in documents]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/<document_id>/versions', methods=['GET'])
@login_required
def get_document_versions(document_id):
    """API: Busca versões de um documento"""
    try:
        versions = service.get_document_versions(document_id)
        
        return jsonify({
            'success': True,
            'data': [version.to_dict() for version in versions]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/<document_id>/toggle-featured', methods=['POST'])
@login_required
def toggle_featured(document_id):
    """API: Alterna status de destaque"""
    try:
        document = service.toggle_featured(document_id)
        
        return jsonify({
            'success': True,
            'data': document.to_dict(),
            'message': 'Status de destaque alterado'
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/<document_id>/publish', methods=['POST'])
@login_required
def publish_document(document_id):
    """API: Publica documento"""
    try:
        document = service.publish_document(document_id)
        
        return jsonify({
            'success': True,
            'data': document.to_dict(),
            'message': 'Documento publicado com sucesso'
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/documents/<document_id>/archive', methods=['POST'])
@login_required
def archive_document(document_id):
    """API: Arquiva documento"""
    try:
        document = service.archive_document(document_id)
        
        return jsonify({
            'success': True,
            'data': document.to_dict(),
            'message': 'Documento arquivado com sucesso'
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    """API: Lista categorias"""
    try:
        categories = service.get_categories()
        
        return jsonify({
            'success': True,
            'data': [cat.to_dict() for cat in categories]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/categories', methods=['POST'])
@login_required
def create_category():
    """API: Cria nova categoria"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        category = service.create_category(data)
        
        return jsonify({
            'success': True,
            'data': category.to_dict(),
            'message': 'Categoria criada com sucesso'
        }), 201
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@documents_bp.route('/api/stats', methods=['GET'])
@login_required
def get_document_stats():
    """API: Estatísticas dos documentos"""
    try:
        stats = service.get_document_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500 