"""
Script para backup e restore do banco de dados
"""
import os
import shutil
import sqlite3
from datetime import datetime


class DatabaseBackup:
    def __init__(self, db_path: str = "database/biblioteca.db") -> None:
        self.db_path = db_path
        self.backup_dir = "database/backups"
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, backup_name: str | None = None):
        if not os.path.exists(self.db_path):
            print("❌ Banco de dados não encontrado!")
            return False
        try:
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"biblioteca_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_name)
            with sqlite3.connect(self.db_path) as source:
                with sqlite3.connect(backup_path) as backup:
                    source.backup(backup)
            file_size = os.path.getsize(backup_path)
            print(f"✅ Backup criado: {backup_path}")
            print(f"📏 Tamanho: {file_size} bytes")
            return backup_path
        except Exception as e:
            print(f"❌ Erro ao criar backup: {str(e)}")
            return False
    
    def restore_backup(self, backup_path: str) -> bool:
        if not os.path.exists(backup_path):
            print("❌ Arquivo de backup não encontrado!")
            return False
        try:
            print("⚠️ Isso irá sobrescrever o banco atual!")
            print(f"Backup: {backup_path}")
            print(f"Destino: {self.db_path}")
            response = input("Confirma restauração? (s/N): ").lower()
            if response != 's':
                print("Operação cancelada.")
                return False
            current_backup = self.create_backup("before_restore_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".db")
            if current_backup:
                print(f"📋 Backup do banco atual salvo em: {current_backup}")
            shutil.copy2(backup_path, self.db_path)
            print("✅ Banco restaurado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {str(e)}")
            return False
    
    def list_backups(self):
        backups = []
        if not os.path.exists(self.backup_dir):
            return backups
        for file in os.listdir(self.backup_dir):
            if file.endswith('.db'):
                file_path = os.path.join(self.backup_dir, file)
                file_size = os.path.getsize(file_path)
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                backups.append({'name': file, 'path': file_path, 'size': file_size, 'date': file_date})
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups
    
    def cleanup_old_backups(self, keep_count: int = 5) -> None:
        backups = self.list_backups()
        if len(backups) <= keep_count:
            print(f"ℹ️ {len(backups)} backups encontrados (mantendo todos)")
            return
        to_remove = backups[keep_count:]
        removed_count = 0
        for backup in to_remove:
            try:
                os.remove(backup['path'])
                removed_count += 1
                print(f"🗑️ Removido: {backup['name']}")
            except Exception as e:
                print(f"❌ Erro ao remover {backup['name']}: {str(e)}")
        print(f"✅ {removed_count} backups antigos removidos")
        print(f"📋 {keep_count} backups mais recentes mantidos")


def backup_menu() -> None:
    backup_manager = DatabaseBackup()
    while True:
        print("\n" + "=" * 50)
        print("🗄️  GERENCIAMENTO DE BACKUP")
        print("=" * 50)
        print("1. 💾 Criar Backup")
        print("2. 📋 Listar Backups")
        print("3. ↩️  Restaurar Backup")
        print("4. 🧹 Limpar Backups Antigos")
        print("5. ❌ Sair")
        choice = input("\nEscolha uma opção: ").strip()
        if choice == '1':
            print("\n🔄 Criando backup...")
            backup_manager.create_backup()
        elif choice == '2':
            print("\n📋 Backups disponíveis:")
            backups = backup_manager.list_backups()
            if not backups:
                print("Nenhum backup encontrado.")
            else:
                for i, backup in enumerate(backups, 1):
                    print(f"{i}. {backup['name']}")
                    print(f"   📅 {backup['date'].strftime('%d/%m/%Y %H:%M:%S')}")
                    print(f"   📏 {backup['size']} bytes")
                    print()
        elif choice == '3':
            backups = backup_manager.list_backups()
            if not backups:
                print("❌ Nenhum backup disponível.")
                continue
            print("\n📋 Selecione um backup para restaurar:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['name']} ({backup['date'].strftime('%d/%m/%Y %H:%M:%S')})")
            try:
                choice_idx = int(input("\nNúmero do backup: ")) - 1
                if 0 <= choice_idx < len(backups):
                    backup_manager.restore_backup(backups[choice_idx]['path'])
                else:
                    print("❌ Opção inválida!")
            except ValueError:
                print("❌ Digite um número válido!")
        elif choice == '4':
            try:
                keep = int(input("Quantos backups manter? (padrão: 5): ") or "5")
                backup_manager.cleanup_old_backups(keep)
            except ValueError:
                print("❌ Digite um número válido!")
        elif choice == '5':
            break
        else:
            print("❌ Opção inválida!")
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    backup_menu()


