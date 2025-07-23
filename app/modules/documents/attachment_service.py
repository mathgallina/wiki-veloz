"""
Serviço para gerenciamento de anexos de documentos
"""
import os
import uuid
import mimetypes
from datetime import datetime
from werkzeug.utils import secure_filename


class AttachmentService:
    """Serviço para gerenciar anexos de documentos"""
    
    def __init__(self):
        self.upload_folder = "static/uploads/attachments"
        self.allowed_extensions = {
            'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff',
            'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'
        }
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        
        # Criar pasta de uploads se não existir
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def upload_attachment(self, file, document_id, description="", uploaded_by="Sistema"):
        """Faz upload de um anexo"""
        try:
            if not file or file.filename == '':
                return None
            
            # Validar extensão
            if '.' not in file.filename or \
               file.filename.rsplit('.', 1)[1].lower() not in self.allowed_extensions:
                return None
            
            # Verificar tamanho
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > self.max_file_size:
                return None
            
            # Gerar nome único
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit('.', 1)[1].lower()
            filename = f"{str(uuid.uuid4())}.{extension}"
            file_path = os.path.join(self.upload_folder, filename)
            
            # Salvar arquivo
            file.save(file_path)
            
            # Determinar MIME type
            mime_type, _ = mimetypes.guess_type(original_filename)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            # Criar anexo
            attachment = {
                'id': str(uuid.uuid4()),
                'document_id': document_id,
                'original_filename': original_filename,
                'filename': filename,
                'file_path': file_path,
                'file_size': file_size,
                'mime_type': mime_type,
                'description': description,
                'uploaded_by': uploaded_by,
                'uploaded_at': datetime.now().isoformat()
            }
            
            # Salvar no JSON
            self._save_attachment(attachment)
            
            return attachment
            
        except Exception as e:
            print(f"Erro ao fazer upload: {e}")
            return None
    
    def get_document_attachments(self, document_id):
        """Obtém todos os anexos de um documento"""
        try:
            attachments = self._load_attachments()
            return [att for att in attachments if att['document_id'] == document_id]
        except Exception as e:
            print(f"Erro ao buscar anexos: {e}")
            return []
    
    def get_attachment(self, attachment_id):
        """Obtém um anexo específico"""
        try:
            attachments = self._load_attachments()
            for att in attachments:
                if att['id'] == attachment_id:
                    return att
            return None
        except Exception as e:
            print(f"Erro ao buscar anexo: {e}")
            return None
    
    def delete_attachment(self, attachment_id):
        """Deleta um anexo"""
        try:
            attachment = self.get_attachment(attachment_id)
            if not attachment:
                return False
            
            # Deletar arquivo físico
            if os.path.exists(attachment['file_path']):
                os.remove(attachment['file_path'])
            
            # Remover do JSON
            attachments = self._load_attachments()
            attachments = [att for att in attachments if att['id'] != attachment_id]
            self._save_attachments(attachments)
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar anexo: {e}")
            return False
    
    def _load_attachments(self):
        """Carrega anexos do arquivo JSON"""
        try:
            import json
            file_path = "data/attachments.json"
            
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
            
        except Exception as e:
            print(f"Erro ao carregar anexos: {e}")
            return []
    
    def _save_attachment(self, attachment):
        """Salva um anexo no arquivo JSON"""
        try:
            import json
            import os
            
            file_path = "data/attachments.json"
            os.makedirs("data", exist_ok=True)
            
            attachments = self._load_attachments()
            attachments.append(attachment)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(attachments, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Erro ao salvar anexo: {e}")
    
    def _save_attachments(self, attachments):
        """Salva lista de anexos no arquivo JSON"""
        try:
            import json
            import os
            
            file_path = "data/attachments.json"
            os.makedirs("data", exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(attachments, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Erro ao salvar anexos: {e}")

    def update_attachment_description(self, attachment_id, description):
        """Atualiza a descrição de um anexo"""
        try:
            attachments = self._load_attachments()
            
            for att in attachments:
                if att['id'] == attachment_id:
                    att['description'] = description
                    self._save_attachments(attachments)
                    return att
            
            return None
        except Exception as e:
            print(f"Erro ao atualizar descrição: {e}")
            return None
    
    def get_attachment_stats(self, document_id):
        """Obtém estatísticas dos anexos de um documento"""
        try:
            attachments = self.get_document_attachments(document_id)
            
            total_size = sum(att['file_size'] for att in attachments)
            file_types = {}
            
            for att in attachments:
                ext = att['original_filename'].rsplit('.', 1)[1].lower()
                file_types[ext] = file_types.get(ext, 0) + 1
            
            return {
                'total_attachments': len(attachments),
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'file_types': file_types
            }
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {
                'total_attachments': 0,
                'total_size_bytes': 0,
                'total_size_mb': 0,
                'file_types': {}
            }
