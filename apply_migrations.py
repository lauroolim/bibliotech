import os
from glob import glob
from database import Database

def apply_migrations():
    migrations = sorted(glob("migrations/*.sql"))
    
    for migration in migrations:
        with open(migration, 'r') as f:
            sql = f.read()
            migration_name = os.path.basename(migration)
            print(f"aplicando {migration_name}...")
            
            try:
                Database.execute_query(sql)
                print(f"{migration_name} aplicada com sucesso")
            except Exception as e:
                print(f"erro ao aplicar {migration_name}: {str(e)}")

if __name__ == "__main__":
    apply_migrations()