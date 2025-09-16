from sqlalchemy.orm import Session
from ..database.models import Book
from ..database.connection import db_connection
from typing import List, Optional

class BookService:
    def __init__(self):
        self.session = db_connection.get_session()
    
    def add_book(self, title: str, author: str, year: int, category: str) -> Book:
        """Adiciona um novo livro"""
        book = Book(
            title=title,
            author=author,
            year=year,
            category=category
        )
        
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book
    
    def get_all_books(self) -> List[Book]:
        """Retorna todos os livros"""
        return self.session.query(Book).all()
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Busca um livro pelo ID"""
        return self.session.query(Book).filter(Book.id == book_id).first()
    
    def get_available_books(self) -> List[Book]:
        """Retorna apenas livros disponíveis"""
        return self.session.query(Book).filter(Book.is_available == True).all()
    
    def get_books_by_category(self, category: str) -> List[Book]:
        """Retorna livros por categoria"""
        return self.session.query(Book).filter(Book.category.ilike(f"%{category}%")).all()
    
    def search_books(self, search_term: str) -> List[Book]:
        """Busca livros por título ou autor"""
        return self.session.query(Book).filter(
            (Book.title.ilike(f"%{search_term}%")) | 
            (Book.author.ilike(f"%{search_term}%"))
        ).all()
    
    def update_book_availability(self, book_id: int, is_available: bool) -> bool:
        """Atualiza disponibilidade do livro"""
        book = self.get_book_by_id(book_id)
        if book:
            book.is_available = is_available
            self.session.commit()
            return True
        return False
    
    def delete_book(self, book_id: int) -> bool:
        """Remove um livro"""
        book = self.get_book_by_id(book_id)
        if book:
            self.session.delete(book)
            self.session.commit()
            return True
        return False
    
    def get_books_count_by_status(self) -> dict:
        """Retorna contagem de livros por status"""
        total = self.session.query(Book).count()
        available = self.session.query(Book).filter(Book.is_available == True).count()
        borrowed = total - available
        
        return {
            'total': total,
            'available': available,
            'borrowed': borrowed
        }
    
    def get_books_count_by_category(self) -> dict:
        """Retorna contagem de livros por categoria"""
        from sqlalchemy import func
        
        result = self.session.query(
            Book.category, 
            func.count(Book.id).label('count')
        ).group_by(Book.category).all()
        
        return {category: count for category, count in result}
    
    def __del__(self):
        """Fecha a sessão quando o objeto é destruído"""
        if hasattr(self, 'session'):
            self.session.close()
