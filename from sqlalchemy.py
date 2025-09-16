from sqlalchemy.orm import Session
from ..database.models import User
from ..database.connection import db_connection
from typing import List, Optional
import re

class UserService:
    def __init__(self):
        self.session = db_connection.get_session()
    
    def add_user(self, name: str, email: str, phone: str) -> Optional[User]:
        """Adiciona um novo usuário"""
        # Verifica se email já existe
        if self.get_user_by_email(email):
            raise ValueError("Email já cadastrado no sistema")
        
        # Valida email
        if not self._validate_email(email):
            raise ValueError("Email inválido")
        
        user = User(
            name=name,
            email=email,
            phone=phone
        )
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_all_users(self) -> List[User]:
        """Retorna todos os usuários"""
        return self.session.query(User).all()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário pelo ID"""
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email"""
        return self.session.query(User).filter(User.email == email).first()
    
    def search_users(self, search_term: str) -> List[User]:
        """Busca usuários por nome ou email"""
        return self.session.query(User).filter(
            (User.name.ilike(f"%{search_term}%")) | 
            (User.email.ilike(f"%{search_term}%"))
        ).all()
    
    def update_user(self, user_id: int, name: str = None, email: str = None, phone: str = None) -> bool:
        """Atualiza dados do usuário"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        if name:
            user.name = name
        if email:
            if not self._validate_email(email):
                raise ValueError("Email inválido")
            # Verifica se o novo email já existe (e não é do mesmo usuário)
            existing_user = self.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email já cadastrado no sistema")
            user.email = email
        if phone:
            user.phone = phone
        
        self.session.commit()
        return True
    
    def delete_user(self, user_id: int) -> bool:
        """Remove um usuário"""
        user = self.get_user_by_id(user_id)
        if user:
            # Verifica se o usuário tem empréstimos ativos
            from ..services.loan_service import LoanService
            loan_service = LoanService()
            active_loans = loan_service.get_active_loans_by_user(user_id)
            if active_loans:
                raise ValueError("Não é possível excluir usuário com empréstimos ativos")
            
            self.session.delete(user)
            self.session.commit()
            return True
        return False
    
    def _validate_email(self, email: str) -> bool:
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __del__(self):
        """Fecha a sessão quando o objeto é destruído"""
        if hasattr(self, 'session'):
            self.session.close()
