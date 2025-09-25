# reset_database.py
import os
import sys
from pathlib import Path


def reset_database():
    # Удаляем файл базы данных
    db_path = Path('instance/ozon_warehouse')
    if db_path.exists():
        db_path.unlink()
        print("✓ База данных удалена")

    # Удаляем папку миграций
    migrations_path = Path('migrations')
    if migrations_path.exists():
        import shutil
        shutil.rmtree(migrations_path)
        print("✓ Папка миграций удалена")

    # Удаляем другие возможные файлы БД
    for db_file in Path('.').glob('*.db'):
        db_file.unlink()
        print(f"✓ Файл {db_file} удален")

    print("✓ База данных полностью очищена")


if __name__ == '__main__':
    reset_database()