"""
Script de inicialização completa do banco de dados
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from database.create_database import DatabaseCreator
from database.seed_data import DataSeeder


def main() -> bool:
    print("🚀 INICIALIZANDO SISTEMA DE BIBLIOTECA")
    print("=" * 60)
    print("\n1️⃣ Criando banco de dados...")
    creator = DatabaseCreator()
    if not creator.create_database():
        print("❌ Falha ao criar banco de dados!")
        return False
    print("\n2️⃣ Populando com dados de exemplo...")
    seeder = DataSeeder()
    response = input("Deseja adicionar dados de exemplo? (S/n): ").lower()
    if response != 'n':
        if not seeder.seed_all():
            print("❌ Falha ao popular banco de dados!")
            return False
    print("\n3️⃣ Verificando instalação...")
    info = creator.get_database_info()
    if info:
        print("✅ Sistema inicializado com sucesso!")
        print(f"\n📊 Resumo:")
        print(f"  📁 Banco: {info['path']}")
        print(f"  📏 Tamanho: {info['size']} bytes")
        print(f"  📅 Criado: {info['created'].strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  📋 Dados:")
        for table, count in info['tables'].items():
            print(f"    - {table}: {count} registros")
        print(f"\n🎉 Pronto! Execute 'python main.py' para começar a usar.")
        return True
    return False


if __name__ == "__main__":
    main()


