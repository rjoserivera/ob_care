import os
import glob

def clean_migrations():
    print("🚀 LIMPIANDO MIGRACIONES Y BASE DE DATOS...")
    
    # 1. Eliminar db.sqlite3
    if os.path.exists("db.sqlite3"):
        try:
            os.remove("db.sqlite3")
            print("  ✅ Base de datos (db.sqlite3) eliminada.")
        except Exception as e:
            print(f"  ❌ Error eliminando db.sqlite3: {e}")
            
    # 2. Buscar carpetas de migraciones
    root_dir = os.getcwd()
    migration_count = 0
    for root, dirs, files in os.walk(root_dir):
        # 🛡️ EXCLUIR CARPETAS DE SISTEMA Y ENTORNO VIRTUAL
        if 'venv' in dirs:
            dirs.remove('venv')
        if '.git' in dirs:
            dirs.remove('.git')
        if '.idea' in dirs:
            dirs.remove('.idea')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')

        if "migrations" in dirs:
            migrations_dir = os.path.join(root, "migrations")
            
            # Listar archivos en migraciones
            for filename in os.listdir(migrations_dir):
                if filename != "__init__.py" and filename.endswith(".py"):
                    file_path = os.path.join(migrations_dir, filename)
                    try:
                        os.remove(file_path)
                        print(f"  🗑️ Eliminado: {file_path}")
                        migration_count += 1
                    except Exception as e:
                        print(f"  ❌ Error eliminando {filename}: {e}")
                        
                # Eliminar pycache si existe
                if filename == "__pycache__":
                    import shutil
                    shutil.rmtree(os.path.join(migrations_dir, filename))

    print(f"\n✨ LIMPIEZA COMPLETA: {migration_count} archivos de migración eliminados.")
    print("⚠️ Recuerda ejecutar 'makemigrations' antes de 'migrate'.")

if __name__ == "__main__":
    clean_migrations()
