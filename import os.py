import os
from colorama import Fore, Style, init
from tabulate import tabulate
from ..services.book_service import BookService
from ..services.user_service import UserService
from ..services.loan_service import LoanService

# Inicializa colorama
init()

class LibraryInterface:
    def __init__(self):
        self.book_service = BookService()
        self.user_service = UserService()
        self.loan_service = LoanService()
    
    def clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Imprime cabeçalho estilizado"""
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{' ' * ((60 - len(title)) // 2)}{title}")
        print(f"{'=' * 60}{Style.RESET_ALL}\n")
    
    def print_success(self, message: str):
        """Imprime mensagem de sucesso"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Imprime mensagem de erro"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Imprime mensagem de aviso"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    def wait_for_enter(self):
        """Aguarda Enter para continuar"""
        input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def get_valid_integer(self, prompt: str, min_value: int = None, max_value: int = None) -> int:
        """Obtém um número inteiro válido do usuário"""
        while True:
            try:
                value = int(input(prompt))
                if min_value is not None and value < min_value:
                    self.print_error(f"Valor deve ser maior ou igual a {min_value}")
                    continue
                if max_value is not None and value > max_value:
                    self.print_error(f"Valor deve ser menor ou igual a {max_value}")
                    continue
                return value
            except ValueError:
                self.print_error("Por favor, digite um número válido")
    
    def main_menu(self):
        """Menu principal"""
        while True:
            self.clear_screen()
            self.print_header("SISTEMA DE GERENCIAMENTO DE BIBLIOTECA")
            
            print(f"{Fore.YELLOW}1. 📚 Gerenciar Livros")
            print(f"2. 👥 Gerenciar Usuários")
            print(f"3. 📖 Gerenciar Empréstimos")
            print(f"4. 📊 Relatórios")
            print(f"5. ❌ Sair{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Escolha uma opção: {Style.RESET_ALL}")
            
            if choice == '1':
                self.books_menu()
            elif choice == '2':
                self.users_menu()
            elif choice == '3':
                self.loans_menu()
            elif choice == '4':
                self.reports_menu()
            elif choice == '5':
                self.print_success("Obrigado por usar o sistema!")
                break
            else:
                self.print_error("Opção inválida!")
                self.wait_for_enter()
    
    def books_menu(self):
        """Menu de gerenciamento de livros"""
        while True:
            self.clear_screen()
            self.print_header("GERENCIAR LIVROS")
            
            print(f"{Fore.YELLOW}1. ➕ Adicionar Livro")
            print(f"2. 📋 Listar Livros")
            print(f"3. 🔍 Buscar Livros")
            print(f"4. 🗑️  Remover Livro")
            print(f"5. ⬅️  Voltar{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Escolha uma opção: {Style.RESET_ALL}")
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.list_books()
            elif choice == '3':
                self.search_books()
            elif choice == '4':
                self.remove_book()
            elif choice == '5':
                break
            else:
                self.print_error("Opção inválida!")
                self.wait_for_enter()
    
    def add_book(self):
        """Adiciona um novo livro"""
        self.clear_screen()
        self.print_header("ADICIONAR LIVRO")
        
        try:
            title = input("Título: ").strip()
            if not title:
                self.print_error("Título não pode estar vazio!")
                self.wait_for_enter()
                return
            
            author = input("Autor: ").strip()
            if not author:
                self.print_error("Autor não pode estar vazio!")
                self.wait_for_enter()
                return
            
            year = self.get_valid_integer("Ano: ", 1000, 2024)
            category = input("Categoria: ").strip()
            if not category:
                self.print_error("Categoria não pode estar vazia!")
                self.wait_for_enter()
                return
            
            book = self.book_service.add_book(title, author, year, category)
            self.print_success(f"Livro '{book.title}' adicionado com sucesso! (ID: {book.id})")
            
        except Exception as e:
            self.print_error(f"Erro ao adicionar livro: {str(e)}")
        
        self.wait_for_enter()
    
    def list_books(self):
        """Lista todos os livros"""
        self.clear_screen()
        self.print_header("LISTA DE LIVROS")
        
        books = self.book_service.get_all_books()
        
        if not books:
            self.print_warning("Nenhum livro cadastrado")
        else:
            table_data = []
            for book in books:
                status = "✅ Disponível" if book.is_available else "❌ Emprestado"
                table_data.append([
                    book.id,
                    book.title,
                    book.author,
                    book.year,
                    book.category,
                    status
                ])
            
            headers = ["ID", "Título", "Autor", "Ano", "Categoria", "Status"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        self.wait_for_enter()
    
    def search_books(self):
        """Busca livros"""
        self.clear_screen()
        self.print_header("BUSCAR LIVROS")
        
        search_term = input("Digite o termo de busca (título ou autor): ").strip()
        
        if not search_term:
            self.print_error("Termo de busca não pode estar vazio!")
            self.wait_for_enter()
            return
        
        books = self.book_service.search_books(search_term)
        
        if not books:
            self.print_warning("Nenhum livro encontrado")
        else:
            table_data = []
            for book in books:
                status = "✅ Disponível" if book.is_available else "❌ Emprestado"
                table_data.append([
                    book.id,
                    book.title,
                    book.author,
                    book.year,
                    book.category,
                    status
                ])
            
            headers = ["ID", "Título", "Autor", "Ano", "Categoria", "Status"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        self.wait_for_enter()
    
    def remove_book(self):
        """Remove um livro"""
        self.clear_screen()
        self.print_header("REMOVER LIVRO")
        
        book_id = self.get_valid_integer("ID do livro a ser removido: ")
        
        book = self.book_service.get_book_by_id(book_id)
        if not book:
            self.print_error("Livro não encontrado!")
            self.wait_for_enter()
            return
        
        print(f"\nLivro encontrado: {book.title} - {book.author}")
        confirm = input("Tem certeza que deseja remover? (s/N): ").lower()
        
        if confirm == 's':
            try:
                if self.book_service.delete_book(book_id):
                    self.print_success("Livro removido com sucesso!")
                else:
                    self.print_error("Erro ao remover livro")
            except Exception as e:
                self.print_error(f"Erro ao remover livro: {str(e)}")
        else:
            self.print_warning("Operação cancelada")
        
        self.wait_for_enter()
    
    def users_menu(self):
        """Menu de gerenciamento de usuários"""
        while True:
            self.clear_screen()
            self.print_header("GERENCIAR USUÁRIOS")
            
            print(f"{Fore.YELLOW}1. ➕ Adicionar Usuário")
            print(f"2. 📋 Listar Usuários")
            print(f"3. 🔍 Buscar Usuários")
            print(f"4. ✏️  Editar Usuário")
            print(f"5. 🗑️  Remover Usuário")
            print(f"6. ⬅️  Voltar{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Escolha uma opção: {Style.RESET_ALL}")
            
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.list_users()
            elif choice == '3':
                self.search_users()
            elif choice == '4':
                self.edit_user()
            elif choice == '5':
                self.remove_user()
            elif choice == '6':
                break
            else:
                self.print_error("Opção inválida!")
                self.wait_for_enter()
    
    def add_user(self):
        """Adiciona um novo usuário"""
        self.clear_screen()
        self.print_header("ADICIONAR USUÁRIO")
        
        try:
            name = input("Nome: ").strip()
            if not name:
                self.print_error("Nome não pode estar vazio!")
                self.wait_for_enter()
                return
            
            email = input("Email: ").strip()
            if not email:
                self.print_error("Email não pode estar vazio!")
                self.wait_for_enter()
                return
            
            phone = input("Telefone: ").strip()
            if not phone:
                self.print_error("Telefone não pode estar vazio!")
                self.wait_for_enter()
                return
            
            user = self.user_service.add_user(name, email, phone)
            self.print_success(f"Usuário '{user.name}' adicionado com sucesso! (ID: {user.id})")
            
        except ValueError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Erro ao adicionar usuário: {str(e)}")
        
        self.wait_for_enter()
    
    def list_users(self):
        """Lista todos os usuários"""
        self.clear_screen()
        self.print_header("LISTA DE USUÁRIOS")
        
        users = self.user_service.get_all_users()
        
        if not users:
            self.print_warning("Nenhum usuário cadastrado")
        else:
            table_data = []
            for user in users:
                table_data.append([
                    user.id,
                    user.name,
                    user.email,
                    user.phone,
                    user.created_at.strftime("%d/%m/%Y")
                ])
            
            headers = ["ID", "Nome", "Email", "Telefone", "Cadastro"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        self.wait_for_enter()
    
    def search_users(self):
        """Busca usuários"""
        self.clear_screen()
        self.print_header("BUSCAR USUÁRIOS")
        
        search_term = input("Digite o termo de busca (nome ou email): ").strip()
        
        if not search_term:
            self.print_error("Termo de busca não pode estar vazio!")
            self.wait_for_enter()
            return
        
        users = self.user_service.search_users(search_term)
        
        if not users:
            self.print_warning("Nenhum usuário encontrado")
        else:
            table_data = []
            for user in users:
                table_data.append([
                    user.id,
                    user.name,
                    user.email,
                    user.phone,
                    user.created_at.strftime("%d/%m/%Y")
                ])
            
            headers = ["ID", "Nome", "Email", "Telefone", "Cadastro"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        self.wait_for_enter()
    
    def edit_user(self):
        """Edita um usuário"""
        self.clear_screen()
        self.print_header("EDITAR USUÁRIO")
        
        user_id = self.get_valid_integer("ID do usuário: ")
        
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            self.print_error("Usuário não encontrado!")
            self.wait_for_enter()
            return
        
        print(f"\nUsuário atual: {user.name} ({user.email})")
        print("Deixe em branco para manter o valor atual")
        
        try:
            name = input(f"Novo nome [{user.name}]: ").strip() or None
            email = input(f"Novo email [{user.email}]: ").strip() or None
            phone = input(f"Novo telefone [{user.phone}]: ").strip() or None
            
            if self.user_service.update_user(user_id, name, email, phone):
                self.print_success