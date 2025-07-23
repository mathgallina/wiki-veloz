// Funcionalidades de Anexos
function attachmentManager() {
  return {
    selectedFile: null,
    documentAttachments: [],
    showUploadModal: false,
    uploadForm: {
      description: '',
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
        return 'fas fa-file-pdf text-red-600';
      } else if (attachment.mime_type.startsWith('image/')) {
        return 'fas fa-file-image text-green-600';
      } else {
        return 'fas fa-file text-blue-600';
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
          alert('Anexo enviado com sucesso!');
        } else {
          alert('Error ao enviar anexo: ' + data.message);
        }
      } catch (error) {
        console.error('Error ao enviar anexo:', error);
        alert('Error ao enviar anexo');
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
          alert('Anexo deletado com sucesso!');
        } else {
          alert('Error ao deletar anexo: ' + data.message);
        }
      } catch (error) {
        console.error('Error ao deletar anexo:', error);
        alert('Error ao deletar anexo');
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
  };
}
