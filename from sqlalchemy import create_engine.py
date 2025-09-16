from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

class DatabaseConnection:
    def __init__(self, db_path="biblioteca.db"):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        """Cria todas as tabelas no banco de dados"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Retorna uma nova sessão do banco de dados"""
        return self.SessionLocal()
    
    def close_connection(self):
        """Fecha a conexão com o banco"""
        self.engine.dispose()

# Instância global da conexão
db_connection = DatabaseConnection()
