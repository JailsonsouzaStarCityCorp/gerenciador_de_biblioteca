"""
Script para resetar completamente o banco de dados
"""
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from database.create_database import DatabaseCreator
from database.seed_data import DataSeeder
from database.backup_restore import DatabaseBackup


def main() -> None:
    print("🔄 RESET DO BANCO DE DADOS")
    print("=" * 40)
    db_path = "database/biblioteca.db"
    if not os.path.exists(db_path):
        print("ℹ️ Banco de dados não existe. Use init_db.py para criar.")
        return
    print("⚠️ ATENÇÃO: Isso irá remover todos os dados!")
    print("Um backup será criado automaticamente.")
    response = input("\nConfirma o reset? (s/N): ").lower()
    if response != 's':
        print("Operação cancelada.")
        return
    print("\n💾 Criando backup de segurança...")
    backup_manager = DatabaseBackup(db_path)
    backup_path = backup_manager.create_backup()
    if backup_path:
        print(f"✅ Backup salvo: {backup_path}")
    else:
        response = input("❌ Falha no backup. Continuar mesmo assim? (s/N): ").lower()
        if response != 's':
            print("Operação cancelada.")
            return
    print("\n🔄 Resetando banco...")
    creator = DatabaseCreator(db_path)
    if creator.create_database():
        print("✅ Banco resetado com sucesso!")
        response = input("\nDeseja adicionar dados de exemplo? (S/n): ").lower()
        if response != 'n':
            print("\n🌱 Adicionando dados de exemplo...")
            seeder = DataSeeder(db_path)
            seeder.seed_all()
        print("\n🎉 Reset concluído!")
    else:
        print("❌ Falha ao resetar banco!")


if __name__ == "__main__":
    main()


