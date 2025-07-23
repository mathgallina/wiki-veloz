"""
Abstração de Dados
==================

Camada de abstração para operações de dados JSON.
Centraliza operações de leitura, escrita e validação.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DataManager:
    """Gerenciador centralizado de dados JSON."""
    
    def __init__(self, data_dir: str):
        """
        Inicializa o gerenciador de dados.
        
        Args:
            data_dir (str): Diretório onde estão os arquivos JSON
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self._cache = {}
        self._cache_timestamps = {}
    
    def _get_file_path(self, filename: str) -> Path:
        """
        Retorna o caminho completo do arquivo.
        
        Args:
            filename (str): Nome do arquivo
            
        Returns:
            Path: Caminho completo do arquivo
        """
        return self.data_dir / filename
    
    def _load_data(self, filename: str) -> List[Dict[str, Any]]:
        """
        Carrega dados de um arquivo JSON.
        
        Args:
            filename (str): Nome do arquivo
            
        Returns:
            List[Dict[str, Any]]: Lista de dados carregados
        """
        file_path = self._get_file_path(filename)
        
        # Verificar cache
        if filename in self._cache:
            cache_timestamp = self._cache_timestamps.get(filename, 0)
            if file_path.stat().st_mtime <= cache_timestamp:
                return self._cache[filename]
        
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
                    self._cache[filename] = data
                    self._cache_timestamps[filename] = file_path.stat().st_mtime
                    logger.debug(
                        f"Dados carregados de {filename}: {len(data)} registros"
                    )
                    return data
            else:
                # Criar arquivo vazio se não existir
                self._save_data(filename, [])
                return []
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Erro ao carregar {filename}: {e}")
            return []
    
    def _save_data(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """
        Salva dados em um arquivo JSON.
        
        Args:
            filename (str): Nome do arquivo
            data (List[Dict[str, Any]]): Dados a serem salvos
            
        Returns:
            bool: True se salvou com sucesso
        """
        file_path = self._get_file_path(filename)
        
        try:
            # Criar backup antes de salvar
            if file_path.exists():
                backup_path = file_path.with_suffix('.json.backup')
                file_path.rename(backup_path)
            
            # Salvar novos dados
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Atualizar cache
            self._cache[filename] = data
            self._cache_timestamps[filename] = file_path.stat().st_mtime
            
            logger.debug(
                f"Dados salvos em {filename}: {len(data)} registros"
            )
            return True
        except IOError as e:
            logger.error(f"Erro ao salvar {filename}: {e}")
            return False
    
    def get_all(self, filename: str) -> List[Dict[str, Any]]:
        """
        Retorna todos os registros de um arquivo.
        
        Args:
            filename (str): Nome do arquivo
            
        Returns:
            List[Dict[str, Any]]: Lista de todos os registros
        """
        return self._load_data(filename)
    
    def get_by_id(self, filename: str, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca um registro por ID.
        
        Args:
            filename (str): Nome do arquivo
            record_id (str): ID do registro
            
        Returns:
            Optional[Dict[str, Any]]: Registro encontrado ou None
        """
        data = self._load_data(filename)
        for record in data:
            if record.get('id') == record_id:
                return record
        return None
    
    def create(self, filename: str, record: Dict[str, Any]) -> bool:
        """
        Cria um novo registro.
        
        Args:
            filename (str): Nome do arquivo
            record (Dict[str, Any]): Dados do registro
            
        Returns:
            bool: True se criado com sucesso
        """
        data = self._load_data(filename)
        
        # Gerar ID se não existir
        if 'id' not in record:
            record['id'] = self._generate_id(data)
        
        # Adicionar timestamps
        record['created_at'] = datetime.now().isoformat()
        record['updated_at'] = datetime.now().isoformat()
        
        data.append(record)
        return self._save_data(filename, data)
    
    def update(self, filename: str, record_id: str, updates: Dict[str, Any]) -> bool:
        """
        Atualiza um registro existente.
        
        Args:
            filename (str): Nome do arquivo
            record_id (str): ID do registro
            updates (Dict[str, Any]): Dados a serem atualizados
            
        Returns:
            bool: True se atualizado com sucesso
        """
        data = self._load_data(filename)
        
        for i, record in enumerate(data):
            if record.get('id') == record_id:
                # Atualizar campos
                record.update(updates)
                record['updated_at'] = datetime.now().isoformat()
                data[i] = record
                return self._save_data(filename, data)
        
        return False
    
    def delete(self, filename: str, record_id: str) -> bool:
        """
        Remove um registro.
        
        Args:
            filename (str): Nome do arquivo
            record_id (str): ID do registro
            
        Returns:
            bool: True se removido com sucesso
        """
        data = self._load_data(filename)
        
        for i, record in enumerate(data):
            if record.get('id') == record_id:
                del data[i]
                return self._save_data(filename, data)
        
        return False
    
    def search(self, filename: str, query: str, fields: List[str] = None) -> List[Dict[str, Any]]:  # type: ignore
        """
        Busca registros por texto.
        
        Args:
            filename (str): Nome do arquivo
            query (str): Texto para busca
            fields (List[str]): Campos para buscar (None = todos)
            
        Returns:
            List[Dict[str, Any]]: Registros encontrados
        """
        data = self._load_data(filename)
        results = []
        query_lower = query.lower()
        
        for record in data:
            if fields:
                # Buscar apenas nos campos especificados
                for field in fields:
                    if field in record:
                        value = str(record[field]).lower()
                        if query_lower in value:
                            results.append(record)
                            break
            else:
                # Buscar em todos os campos
                for value in record.values():
                    if query_lower in str(value).lower():
                        results.append(record)
                        break
        
        return results
    
    def _generate_id(self, data: List[Dict[str, Any]]) -> str:
        """
        Gera um ID único para um novo registro.
        
        Args:
            data (List[Dict[str, Any]]): Dados existentes
            
        Returns:
            str: ID único gerado
        """
        if not data:
            return "1"
        
        # Encontrar o maior ID numérico
        max_id = 0
        for record in data:
            try:
                record_id = int(record.get('id', '0'))
                max_id = max(max_id, record_id)
            except (ValueError, TypeError):
                continue
        
        return str(max_id + 1)
    
    def clear_cache(self, filename: str = None):
        """
        Limpa o cache de dados.
        
        Args:
            filename (str): Nome do arquivo específico (None = todos)
        """
        if filename:
            self._cache.pop(filename, None)
            self._cache_timestamps.pop(filename, None)
        else:
            self._cache.clear()
            self._cache_timestamps.clear()
        
        logger.debug("Cache limpo")


# Instância global do gerenciador de dados
data_manager = None


def init_data_manager(data_dir: str):
    """
    Inicializa o gerenciador de dados global.
    
    Args:
        data_dir (str): Diretório dos dados
    """
    global data_manager
    data_manager = DataManager(data_dir)
    logger.info(f"DataManager inicializado com diretório: {data_dir}")


def get_data_manager() -> DataManager:
    """
    Retorna a instância global do gerenciador de dados.
    
    Returns:
        DataManager: Instância do gerenciador de dados
    """
    if data_manager is None:
        raise RuntimeError("DataManager não foi inicializado")
    return data_manager 