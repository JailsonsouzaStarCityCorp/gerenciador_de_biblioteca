"""
Script para popular o banco com dados iniciais de exemplo
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Book, User, Loan


class DataSeeder:
    def __init__(self, db_path: str = "database/biblioteca.db") -> None:
        self.db_path = db_path
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            self.engine = create_engine(database_url, pool_pre_ping=True)
        else:
            self.engine = create_engine(f'sqlite:///{db_path}')
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def seed_books(self, session):
        books_data = [
            ("Dom Casmurro", "Machado de Assis", 1899, "Romance"),
            ("O Cortiço", "Aluísio Azevedo", 1890, "Romance"),
            ("1984", "George Orwell", 1949, "Ficção Científica"),
            ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", 1943, "Infantil"),
            ("Cem Anos de Solidão", "Gabriel García Márquez", 1967, "Romance"),
            ("O Alquimista", "Paulo Coelho", 1988, "Filosofia"),
            ("Harry Potter e a Pedra Filosofal", "J.K. Rowling", 1997, "Fantasy"),
            ("O Senhor dos Anéis", "J.R.R. Tolkien", 1954, "Fantasy"),
            ("Código Limpo", "Robert C. Martin", 2008, "Tecnologia"),
            ("Python Fluente", "Luciano Ramalho", 2015, "Tecnologia"),
            ("A Arte da Guerra", "Sun Tzu", -500, "Filosofia"),
            ("Sapiens", "Yuval Noah Harari", 2011, "História"),
            ("O Gene Egoísta", "Richard Dawkins", 1976, "Ciência"),
            ("Uma Breve História do Tempo", "Stephen Hawking", 1988, "Ciência"),
            ("O Poder do Hábito", "Charles Duhigg", 2012, "Autoajuda"),
            ("Mindset", "Carol S. Dweck", 2006, "Psicologia"),
            ("A Origem das Espécies", "Charles Darwin", 1859, "Ciência"),
            ("Orgulho e Preconceito", "Jane Austen", 1813, "Romance"),
            ("Crime e Castigo", "Fiódor Dostoiévski", 1866, "Romance"),
            ("O Hobbit", "J.R.R. Tolkien", 1937, "Fantasy"),
        ]
        books = []
        for title, author, year, category in books_data:
            book = Book(title=title, author=author, year=year, category=category, is_available=True)
            books.append(book)
            session.add(book)
        session.commit()
        print(f"✅ {len(books)} livros adicionados")
        return books
    
    def seed_users(self, session):
        users_data = [
            ("Ana Silva", "ana.silva@email.com", "(11) 98765-4321"),
            ("João Santos", "joao.santos@email.com", "(11) 99876-5432"),
            ("Maria Oliveira", "maria.oliveira@email.com", "(11) 98765-1234"),
            ("Pedro Costa", "pedro.costa@email.com", "(11) 97654-3210"),
            ("Carla Ferreira", "carla.ferreira@email.com", "(11) 96543-2109"),
            ("Lucas Almeida", "lucas.almeida@email.com", "(11) 95432-1098"),
            ("Julia Rodrigues", "julia.rodrigues@email.com", "(11) 94321-0987"),
            ("Rafael Martins", "rafael.martins@email.com", "(11) 93210-9876"),
            ("Fernanda Lima", "fernanda.lima@email.com", "(11) 92109-8765"),
            ("Diego Pereira", "diego.pereira@email.com", "(11) 91098-7654"),
        ]
        users = []
        for name, email, phone in users_data:
            user = User(name=name, email=email, phone=phone)
            users.append(user)
            session.add(user)
        session.commit()
        print(f"✅ {len(users)} usuários adicionados")
        return users
    
    def seed_loans(self, session, books, users):
        loans = []
        for _ in range(5):
            user = random.choice(users)
            available_books = [b for b in books if b.is_available]
            if available_books:
                book = random.choice(available_books)
                book.is_available = False
                loan_date = datetime.now() - timedelta(days=random.randint(1, 30))
                loan = Loan(user_id=user.id, book_id=book.id, loan_date=loan_date, is_returned=False)
                loans.append(loan)
                session.add(loan)
        for _ in range(8):
            user = random.choice(users)
            book = random.choice(books)
            loan_date = datetime.now() - timedelta(days=random.randint(30, 90))
            return_date = loan_date + timedelta(days=random.randint(1, 7))
            loan = Loan(user_id=user.id, book_id=book.id, loan_date=loan_date, return_date=return_date, is_returned=True)
            loans.append(loan)
            session.add(loan)
        session.commit()
        print(f"✅ {len(loans)} empréstimos adicionados")
        return loans
    
    def seed_all(self) -> bool:
        session = self.SessionLocal()
        try:
            print("🌱 Populando banco de dados...")
            if session.query(Book).count() > 0:
                print("⚠️ Dados já existem no banco!")
                response = input("Deseja limpar e recriar? (s/N): ").lower()
                if response != 's':
                    print("Operação cancelada.")
                    return False
                session.query(Loan).delete()
                session.query(Book).delete()
                session.query(User).delete()
                session.commit()
                print("🧹 Dados existentes removidos")
            books = self.seed_books(session)
            users = self.seed_users(session)
            loans = self.seed_loans(session, books, users)
            print(f"""
📊 Resumo dos dados criados:
  📚 Livros: {len(books)}
  👥 Usuários: {len(users)}
  📖 Empréstimos: {len(loans)}
            """)
            return True
        except Exception as e:
            print(f"❌ Erro ao popular banco: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_statistics(self):
        session = self.SessionLocal()
        try:
            stats = {
                'books': {
                    'total': session.query(Book).count(),
                    'available': session.query(Book).filter(Book.is_available == True).count(),
                    'borrowed': session.query(Book).filter(Book.is_available == False).count(),
                },
                'users': {'total': session.query(User).count()},
                'loans': {
                    'total': session.query(Loan).count(),
                    'active': session.query(Loan).filter(Loan.is_returned == False).count(),
                    'returned': session.query(Loan).filter(Loan.is_returned == True).count(),
                },
            }
            return stats
        finally:
            session.close()


if __name__ == "__main__":
    seeder = DataSeeder()
    print("🌱 Populando banco com dados de exemplo")
    print("=" * 50)
    if seeder.seed_all():
        print("\n📈 Estatísticas finais:")
        stats = seeder.get_statistics()
        print(f"📚 Livros:")
        print(f"  Total: {stats['books']['total']}")
        print(f"  Disponíveis: {stats['books']['available']}")
        print(f"  Emprestados: {stats['books']['borrowed']}")
        print(f"👥 Usuários: {stats['users']['total']}")
        print(f"📖 Empréstimos:")
        print(f"  Total: {stats['loans']['total']}")
        print(f"  Ativos: {stats['loans']['active']}")
        print(f"  Devolvidos: {stats['loans']['returned']}")


