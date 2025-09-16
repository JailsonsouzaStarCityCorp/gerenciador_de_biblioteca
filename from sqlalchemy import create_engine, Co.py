from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamento
    loans = relationship("Loan", back_populates="book")
    
    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}')>"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamento
    loans = relationship("Loan", back_populates="user")
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

class Loan(Base):
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    loan_date = Column(DateTime, default=datetime.now)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")
    
    def __repr__(self):
        return f"<Loan(user_id={self.user_id}, book_id={self.book_id})>"
