🎯 Sobre o Projeto
O Sistema de Gerenciamento de Biblioteca é uma aplicação desenvolvida para facilitar o controle de acervos bibliográficos, permitindo o cadastro de livros, usuários e o gerenciamento completo de empréstimos e devoluções.

⭐ Principais Características
🖥️ Interface CLI amigável com cores e formatação
📚 Gerenciamento completo de livros (CRUD)
👥 Cadastro e controle de usuários
📖 Sistema de empréstimos e devoluções
📊 Relatórios e estatísticas detalhados
🗄️ Banco de dados SQLite integrado
💾 Sistema de backup e restore
🌱 Dados de exemplo para testes
✨ Funcionalidades
📚 Gerenciamento de Livros
✅ Cadastrar novos livros (título, autor, ano, categoria)
✅ Listar todos os livros com status
✅ Buscar livros por título ou autor
✅ Filtrar livros por categoria
✅ Controle de disponibilidade automático
✅ Remoção de livros
👥 Gerenciamento de Usuários
✅ Cadastrar usuários (nome, email, telefone)
✅ Listar e buscar usuários
✅ Editar informações dos usuários
✅ Validação de email
✅ Controle de usuários com empréstimos ativos
📖 Sistema de Empréstimos
✅ Registrar empréstimos
✅ Processar devoluções
✅ Listar empréstimos ativos
✅ Histórico completo de empréstimos
✅ Identificar empréstimos em atraso
✅ Controle automático de disponibilidade
📊 Relatórios e Estatísticas
✅ Quantidade de livros por status
✅ Livros por categoria
✅ Estatísticas de empréstimos
✅ Usuários mais ativos
✅ Livros mais emprestados
🛠️ Tecnologias
Core
Python 3.8+ - Linguagem principal
SQLAlchemy - ORM para banco de dados
SQLite - Banco de dados local
Interface e Apresentação
Colorama - Cores no terminal
Tabulate - Formatação de tabelas
CLI personalizada - Interface amigável
Estrutura e Organização
Arquitetura em camadas (Models, Services, CLI)
Padrão Repository para acesso aos dados
Separação de responsabilidades
📁 Estrutura do Projeto

biblioteca_sistema/
│
├── 📁 src/                          # Código fonte principal
│   ├── 📁 database/                 # Modelos e conexão
│   │   ├── __init__.py
│   │   ├── connection.py            # Configuração do banco
│   │   └── models.py                # Modelos SQLAlchemy
│   │
│   ├── 📁 services/                 # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── book_service.py          # Serviços de livros
│   │   ├── user_service.py          # Serviços de usuários
│   │   └── loan_service.py          # Serviços de empréstimos
│   │
│   ├── 📁 cli/                      # Interface de linha de comando
│   │   ├── __init__.py
│   │   └── interface.py             # Interface principal
│   │
│   └── 📁 utils/                    # Utilitários
│       ├── __init__.py
│       └── validators.py            # Validadores
│
├── 📁 database/                     # Scripts e arquivos do banco
│   ├── biblioteca.db                # Arquivo do banco SQLite
│   ├── create_database.py           # Criação do banco
│   ├── seed_data.py                 # Dados de exemplo
│   ├── backup_restore.py            # Backup e restore
│   └── 📁 backups/                  # Backups automáticos
│
├── 📁 scripts/                      # Scripts de manutenção
│   ├── init_db.py                   # Inicialização completa
│   └── reset_db.py                  # Reset do banco
│
├── 📁 tests/                        # Testes automatizados
├── 📄 requirements.txt              # Dependências
├── 📄 main.py                       # Ponto de entrada
└── 📄 README.md                     # Este arquivo

🚀 Instalação
Pré-requisitos
Python 3.8 ou superior
pip (gerenciador de pacotes do Python)
Passo a Passo
Clone o repositório
copy
git clone https://github.com/seu-usuario/biblioteca-sistema.git
cd biblioteca-sistema
Crie um ambiente virtual (recomendado)
copy
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
Instale as dependências
copy
pip install -r requirements.txt
Inicialize o banco de dados
copy
python scripts/init_db.py
Execute o sistema
copy
python main.py
🎮 Como Usar
Primeira Execução
Após a instalação, o sistema criará automaticamente:

📚 20 livros de exemplo (ficção, tecnologia, romance, etc.)
👥 10 usuários fictícios
📖 13 empréstimos (5 ativos, 8 devolvidos)
Navegação no Sistema
Menu Principal

Use os números (1-5) para navegar
As opções são auto-explicativas
Gerenciamento de Livros

copy
📚 GERENCIAR LIVROS
1. ➕ Adicionar Livro
2. 📋 Listar Livros  
3. 🔍 Buscar Livros
4. 🗑️ Remover Livro
5. ⬅️ Voltar
Gerenciamento de Usuários

copy
👥 GERENCIAR USUÁRIOS
1. ➕ Adicionar Usuário
2. 📋 Listar Usuários
3. 🔍 Buscar Usuários
4. ✏️ Editar Usuário
5. 🗑️ Remover Usuário
6. ⬅️ Voltar
Sistema de Empréstimos

copy
📖 GERENCIAR EMPRÉSTIMOS
1. 📚 Novo Empréstimo
2. 📥 Processar Devolução
3. 📋 Empréstimos Ativos
4. 📜 Histórico Completo
5. ⚠️ Empréstimos em Atraso
6. ⬅️ Voltar
Exemplos de Uso
Cadastrar um livro:

copy
Título: Clean Code
Autor: Robert C. Martin
Ano: 2008
Categoria: Tecnologia
Realizar um empréstimo:

copy
ID do usuário: 1
ID do livro: 5
Buscar livros:

copy
Termo de busca: python
// Retorna todos os livros com "python" no título ou autor
🔧 Scripts Disponíveis
Inicialização e Setup
copy
# Configuração inicial completa (primeira vez)
python scripts/init_db.py

# Apenas criar estrutura do banco
python database/create_database.py

# Apenas adicionar dados de exemplo
python database/seed_data.py
Manutenção do Banco
copy
# Reset completo do banco (com backup automático)
python scripts/reset_db.py

# Gerenciamento de backups
python database/backup_restore.py
Execução
copy
# Executar o sistema principal
python main.py
🗄️ Banco de Dados
Estrutura das Tabelas
📚 Tabela books

copy
- id (INTEGER, PRIMARY KEY)
- title (VARCHAR, NOT NULL)
- author (VARCHAR, NOT NULL) 
- year (INTEGER, NOT NULL)
- category (VARCHAR, NOT NULL)
- is_available (BOOLEAN, DEFAULT TRUE)
- created_at (DATETIME)
👥 Tabela users

copy
- id (INTEGER, PRIMARY KEY)
- name (VARCHAR, NOT NULL)
- email (VARCHAR, UNIQUE, NOT NULL)
- phone (VARCHAR, NOT NULL)
- created_at (DATETIME)
📖 Tabela loans

copy
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- book_id (INTEGER, FOREIGN KEY)
- loan_date (DATETIME)
- return_date (DATETIME, NULL)
- is_returned (BOOLEAN, DEFAULT FALSE)
Relacionamentos
User → Loans (1:N)
Book → Loans (1:N)
Loan → User (N:1)
Loan → Book (N:1)
Sistema de Backup
O sistema inclui funcionalidades completas de backup:

✅ Backup automático antes de operações críticas
✅ Restore de qualquer backup
✅ Limpeza automática de backups antigos
✅ Listagem de todos os backups disponíveis
📸 Capturas de Tela
Menu Principal
copy
============================================================
                SISTEMA DE GERENCIAMENTO DE BIBLIOTECA
============================================================

1. 📚 Gerenciar Livros
2. 👥 Gerenciar Usuários  
3. 📖 Gerenciar Empréstimos
4. 📊 Relatórios
5. ❌ Sair

Escolha uma opção: 
Lista de Livros
copy
╒══════╤═══════════════════════════════╤═══════════════════════╤════════╤═════════════╤═══════════════╕
│   ID │ Título                        │ Autor                 │    Ano │ Categoria   │ Status        │
╞══════╪═══════════════════════════════╪═══════════════════════╪════════╪═════════════╪═══════════════╡
│    1 │ Dom Casmurro                  │ Machado de Assis      │   1899 │ Romance     │ ✅ Disponível │
│    2 │ O Cortiço                     │ Aluísio Azevedo       │   1890 │ Romance     │ ❌ Emprestado │
│    3 │ 1984                          │ George Orwell         │   1949 │ Ficção      │ ✅ Disponível │
╘══════╧═══════════════════════════════╧═══════════════════════╧════════╧═════════════╧═══════════════╛
Relatórios
copy
📊 RELATÓRIOS E ESTATÍSTICAS

📚 Livros:
  Total: 20
  Disponíveis: 15  
  Emprestados: 5

👥 Usuários: 10

📖 Empréstimos:
  Total: 13
  Ativos: 5
  Devolvidos: 8

📈 Por Categoria:
  Romance: 6 livros
  Tecnologia: 4 livros
  Ficção: 3 livros
  Fantasy: 3 livros
🗺️ Roadmap
✅ Versão 1.0 (Atual)
[x] CRUD completo de livros, usuários e empréstimos
[x] Interface CLI com cores e formatação
[x] Sistema de relatórios básicos
[x] Banco de dados SQLite
[x] Sistema de backup/restore
[x] Dados de exemplo
🔄 Versão 1.1 (Em desenvolvimento)
[ ] Testes automatizados
[ ] Validações aprimoradas
[ ] Controle de multas por atraso
[ ] Reserva de livros
[ ] Logs de sistema
🎯 Versão 2.0 (Planejado)
[ ] Interface web com Flask/FastAPI
[ ] API REST completa
[ ] Autenticação de usuários
[ ] Dashboard com gráficos
[ ] Exportação de relatórios (PDF/Excel)
[ ] Sistema de notificações
🚀 Versão 3.0 (Futuro)
[ ] Interface gráfica (Tkinter/PyQt)
[ ] Multi-bibliotecas
[ ] Integração com ISBN
[ ] Código de barras
[ ] Mobile app
🤝 Contribuição
Contribuições são sempre bem-vindas!

Como Contribuir
Fork o projeto
Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)
Commit suas mudanças (git commit -m 'Add some AmazingFeature')
Push para a branch (git push origin feature/AmazingFeature)
Abra um Pull Request
Diretrizes
📝 Mantenha o código limpo e documentado
✅ Adicione testes para novas funcionalidades
📚 Atualize a documentação quando necessário
🎨 Siga os padrões de código existentes
🐛 Reporte bugs com detalhes
Tipos de Contribuição
🐛 Bug fixes
✨ Novas funcionalidades
📚 Documentação
🎨 Melhorias de UI/UX
⚡ Otimizações de performance
🧪 Testes
📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

copy
MIT License

Copyright (c) 2025 Jailson da Silva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
👤 Autor
Jailson da silva


💼 LinkedIn: https://www.linkedin.com/in/jailson-suporte-ti/
📧 Email: suporte@neteletronica.com.br
🐙 GitHub: JailsonsouzaStarCityCorp
🙏 Agradecimentos
📚 Python Software Foundation - Pela linguagem Python
🗄️ SQLAlchemy Team - Pelo excelente ORM
🎨 Colorama e Tabulate - Por tornar o CLI mais bonito
👥 Comunidade Python - Por todo o apoio e recursos
📈 Estatísticas do Projeto
GitHub starsGitHub forksGitHub issuesGitHub pull requests

<div align="center">

⭐ Se este projeto te ajudou, considere dar uma estrela!

📚 Happy Coding! 🐍

</div>