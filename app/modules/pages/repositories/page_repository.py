"""
Page repository for Wiki Veloz
CDD v2.0 - Page data management
"""

import uuid
from datetime import datetime
from typing import List, Optional

from app.core.database import DatabaseManager


class PageRepository:
    """Repository for page operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.filename = "pages.json"
    
    def load_pages(self) -> List[dict]:
        """Load all pages"""
        return self.db_manager.load_data(self.filename)
    
    def save_pages(self, pages: List[dict]) -> bool:
        """Save all pages"""
        return self.db_manager.save_data(self.filename, pages)
    
    def get_page_by_id(self, page_id: str) -> Optional[dict]:
        """Get page by ID"""
        return self.db_manager.get_by_id(self.filename, page_id)
    
    def get_page_by_slug(self, slug: str) -> Optional[dict]:
        """Get page by slug"""
        pages = self.load_pages()
        return next((p for p in pages if p.get('slug') == slug), None)
    
    def create_page(self, page_data: dict) -> bool:
        """Create new page"""
        pages = self.load_pages()
        
        # Generate ID if not provided
        if 'id' not in page_data:
            page_data['id'] = f"page-{uuid.uuid4().hex[:8]}"
        
        # Generate slug if not provided
        if 'slug' not in page_data and 'title' in page_data:
            from slugify import slugify
            page_data['slug'] = slugify(page_data['title'])
        
        # Add timestamps
        page_data['created_at'] = datetime.now().isoformat()
        page_data['updated_at'] = datetime.now().isoformat()
        page_data['version'] = 1
        
        pages.append(page_data)
        return self.save_pages(pages)
    
    def update_page(self, page_id: str, updates: dict) -> bool:
        """Update page"""
        pages = self.load_pages()
        
        for page in pages:
            if page.get('id') == page_id:
                # Update version
                current_version = page.get('version', 1)
                updates['version'] = current_version + 1
                updates['updated_at'] = datetime.now().isoformat()
                
                # Update slug if title changed
                if 'title' in updates and 'slug' not in updates:
                    from slugify import slugify
                    updates['slug'] = slugify(updates['title'])
                
                page.update(updates)
                return self.save_pages(pages)
        
        return False
    
    def delete_page(self, page_id: str) -> bool:
        """Delete page"""
        return self.db_manager.delete_item(self.filename, page_id)
    
    def get_pages_by_category(self, category: str) -> List[dict]:
        """Get pages by category"""
        pages = self.load_pages()
        return [p for p in pages if p.get('category') == category]
    
    def get_pages_by_author(self, author_id: str) -> List[dict]:
        """Get pages by author"""
        pages = self.load_pages()
        return [p for p in pages if p.get('author_id') == author_id]
    
    def search_pages(self, query: str) -> List[dict]:
        """Search pages by title, content, or tags"""
        pages = self.load_pages()
        query_lower = query.lower()
        
        results = []
        for page in pages:
            # Search in title
            if query_lower in page.get('title', '').lower():
                results.append(page)
                continue
            
            # Search in content
            if query_lower in page.get('content', '').lower():
                results.append(page)
                continue
            
            # Search in tags
            tags = page.get('tags', [])
            if any(query_lower in tag.lower() for tag in tags):
                results.append(page)
                continue
        
        return results
    
    def get_recent_pages(self, limit: int = 10) -> List[dict]:
        """Get recent pages"""
        pages = self.load_pages()
        sorted_pages = sorted(
            pages, 
            key=lambda x: x.get('updated_at', ''), 
            reverse=True
        )
        return sorted_pages[:limit]
    
    def get_popular_pages(self, limit: int = 10) -> List[dict]:
        """Get popular pages by views"""
        pages = self.load_pages()
        sorted_pages = sorted(
            pages, 
            key=lambda x: x.get('views', 0), 
            reverse=True
        )
        return sorted_pages[:limit]
    
    def increment_views(self, page_id: str) -> bool:
        """Increment page views"""
        pages = self.load_pages()
        
        for page in pages:
            if page.get('id') == page_id:
                current_views = page.get('views', 0)
                page['views'] = current_views + 1
                return self.save_pages(pages)
        
        return False
    
    def create_page_version(self, page_id: str, version_data: dict) -> bool:
        """Create a new version of a page"""
        pages = self.load_pages()
        
        for page in pages:
            if page.get('id') == page_id:
                # Store current version in versions array
                if 'versions' not in page:
                    page['versions'] = []
                
                current_version = {
                    'version': page.get('version', 1),
                    'content': page.get('content', ''),
                    'title': page.get('title', ''),
                    'created_at': page.get('updated_at', ''),
                    'author_id': page.get('author_id', '')
                }
                
                page['versions'].append(current_version)
                
                # Update with new version
                page.update(version_data)
                page['version'] = current_version['version'] + 1
                page['updated_at'] = datetime.now().isoformat()
                
                return self.save_pages(pages)
        
        return False
    
    def get_page_versions(self, page_id: str) -> List[dict]:
        """Get all versions of a page"""
        page = self.get_page_by_id(page_id)
        if page and 'versions' in page:
            return page['versions']
        return []
    
    def restore_page_version(self, page_id: str, version: int) -> bool:
        """Restore a specific version of a page"""
        page = self.get_page_by_id(page_id)
        if not page or 'versions' not in page:
            return False
        
        # Find the version to restore
        for version_data in page['versions']:
            if version_data.get('version') == version:
                # Create new version with restored content
                return self.create_page_version(page_id, {
                    'content': version_data.get('content', ''),
                    'title': version_data.get('title', ''),
                    'author_id': page.get('author_id', '')
                })
        
        return False 