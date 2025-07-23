// Funcionalidades de Anexos Melhoradas
function attachmentManager() {
  return {
    selectedFile: null,
    documentAttachments: [],
    showUploadModal: false,
    showPreviewModal: false,
    previewAttachment: null,
    uploadForm: {
      description: '',
    },

    // Detectar tema do sistema
    isDarkMode: false,

    init() {
      this.detectTheme();
      // Observar mudanças no tema do sistema
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        this.detectTheme();
      });
    },

    detectTheme() {
      // Verificar se o usuário tem preferência salva
      const savedTheme = localStorage.getItem('wiki-theme');
      if (savedTheme) {
        this.isDarkMode = savedTheme === 'dark';
      } else {
        // Detectar preferência do sistema
        this.isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
      }
    },

    async loadDocumentAttachments(documentId) {
      try {
        const response = await fetch(`/documents/api/documents/${documentId}/attachments`);
        const data = await response.json();
        if (data.success) {
          this.documentAttachments = data.data.map(att => ({
            ...att,
            icon_class: this.getAttachmentIconClass(att),
            file_size_mb: this.formatFileSize(att.file_size),
          }));
        }
      } catch (error) {
        console.error('Error ao carregar anexos:', error);
        this.documentAttachments = [];
      }
    },

    getAttachmentIconClass(attachment) {
      if (attachment.mime_type === 'application/pdf') {
        return 'fas fa-file-pdf text-red-600 dark:text-red-400';
      } else if (attachment.mime_type.startsWith('image/')) {
        return 'fas fa-file-image text-green-600 dark:text-green-400';
      } else if (
        attachment.mime_type.includes('word') ||
        attachment.mime_type.includes('document')
      ) {
        return 'fas fa-file-word text-blue-600 dark:text-blue-400';
      } else if (
        attachment.mime_type.includes('excel') ||
        attachment.mime_type.includes('spreadsheet')
      ) {
        return 'fas fa-file-excel text-green-600 dark:text-green-400';
      } else if (
        attachment.mime_type.includes('powerpoint') ||
        attachment.mime_type.includes('presentation')
      ) {
        return 'fas fa-file-powerpoint text-orange-600 dark:text-orange-400';
      } else {
        return 'fas fa-file text-gray-600 dark:text-gray-400';
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    handleFileSelect(event) {
      this.selectedFile = event.target.files[0];
    },

    async uploadAttachment() {
      if (!this.selectedFile || !this.selectedDocument) return;

      try {
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        formData.append('description', this.uploadForm.description);

        const response = await fetch(
          `/documents/api/documents/${this.selectedDocument.id}/attachments`,
          {
            method: 'POST',
            body: formData,
          }
        );

        const data = await response.json();

        if (data.success) {
          this.closeUploadModal();
          await this.loadDocumentAttachments(this.selectedDocument.id);
          this.showNotification('Anexo enviado com sucesso!', 'success');
        } else {
          this.showNotification('Error ao enviar anexo: ' + data.message, 'error');
        }
      } catch (error) {
        console.error('Error ao enviar anexo:', error);
        this.showNotification('Error ao enviar anexo', 'error');
      }
    },

    async deleteAttachment(attachment) {
      if (!confirm('Tem certeza que deseja deletar este anexo?')) return;

      try {
        const response = await fetch(`/documents/api/documents/attachments/${attachment.id}`, {
          method: 'DELETE',
        });

        const data = await response.json();

        if (data.success) {
          await this.loadDocumentAttachments(this.selectedDocument.id);
          this.showNotification('Anexo deletado com sucesso!', 'success');
        } else {
          this.showNotification('Error ao deletar anexo: ' + data.message, 'error');
        }
      } catch (error) {
        console.error('Error ao deletar anexo:', error);
        this.showNotification('Error ao deletar anexo', 'error');
      }
    },

    // Preview de PDF antes do download
    async previewAttachment(attachment) {
      if (attachment.mime_type === 'application/pdf') {
        this.previewAttachment = attachment;
        this.showPreviewModal = true;
      } else {
        // Para outros tipos, fazer download direto
        this.downloadAttachment(attachment);
      }
    },

    downloadAttachment(attachment) {
      window.open(`/documents/api/documents/attachments/${attachment.id}/download`, '_blank');
    },

    closeUploadModal() {
      this.showUploadModal = false;
      this.selectedFile = null;
      this.uploadForm.description = '';
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },

    closePreviewModal() {
      this.showPreviewModal = false;
      this.previewAttachment = null;
    },

    showNotification(message, type = 'info') {
      // Criar notificação temporária
      const notification = document.createElement('div');
      notification.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full ${
        type === 'success'
          ? 'bg-green-500 text-white'
          : type === 'error'
          ? 'bg-red-500 text-white'
          : 'bg-blue-500 text-white'
      }`;
      notification.textContent = message;

      document.body.appendChild(notification);

      // Animar entrada
      setTimeout(() => {
        notification.classList.remove('translate-x-full');
      }, 100);

      // Remover após 3 segundos
      setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
          document.body.removeChild(notification);
        }, 300);
      }, 3000);
    },
  };
}
