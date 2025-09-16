"""
Script para criar o banco de dados e todas as tabelas
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.database.models import Base


class DatabaseCreator:
    def __init__(self, db_path: str = "database/biblioteca.db") -> None:
        self.db_path = db_path
        self.engine = None
        
    def create_database(self) -> bool:
        """Cria o banco de dados e todas as tabelas"""
        try:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            if not database_url and os.path.exists(self.db_path):
                print(f"⚠️ Banco existente encontrado em {self.db_path}")
                response = input("Deseja sobrescrever? (s/N): ").lower()
                if response != 's':
                    print("Operação cancelada.")
                    return False
                os.remove(self.db_path)
            
            if database_url:
                self.engine = create_engine(database_url, echo=True, pool_pre_ping=True)
            else:
                self.engine = create_engine(f'sqlite:///{self.db_path}', echo=True)
            print("🏗️ Criando tabelas...")
            Base.metadata.create_all(bind=self.engine)
            self._verify_tables()
            if database_url:
                print(f"✅ Conectado e sincronizado com banco remoto: {database_url}")
            else:
                print(f"✅ Banco de dados criado com sucesso em: {self.db_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar banco de dados: {str(e)}")
            return False
    
    def _verify_tables(self) -> None:
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            expected_tables = ['books', 'users', 'loans']
            print("\n📋 Tabelas criadas:")
            for table in tables:
                if table in expected_tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ℹ️ {table} (sistema)")
            missing_tables = set(expected_tables) - set(tables)
            if missing_tables:
                raise Exception(f"Tabelas não criadas: {missing_tables}")
    
    def get_database_info(self):
        database_url = os.getenv("DATABASE_URL")
        if not database_url and not os.path.exists(self.db_path):
            return None
        with self.engine.connect() as conn:
            tables_info = {}
            for table_name in ['books', 'users', 'loans']:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = result.scalar()
                    tables_info[table_name] = count
                except Exception:
                    tables_info[table_name] = 0
            file_size = os.path.getsize(self.db_path) if not database_url else 0
            return {
                'path': database_url or self.db_path,
                'size': file_size,
                'tables': tables_info,
                'created': datetime.now() if database_url else datetime.fromtimestamp(os.path.getctime(self.db_path))
            }


if __name__ == "__main__":
    creator = DatabaseCreator()
    print("🚀 Criando banco de dados para o Sistema de Biblioteca")
    print("=" * 60)
    if creator.create_database():
        print("\n📊 Informações do banco:")
        info = creator.get_database_info()
        if info:
            print(f"  📁 Caminho: {info['path']}")
            print(f"  📏 Tamanho: {info['size']} bytes")
            print(f"  📅 Criado em: {info['created'].strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"  📋 Tabelas:")
            for table, count in info['tables'].items():
                print(f"    - {table}: {count} registros")


