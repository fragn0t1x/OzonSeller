from app import create_app, db
from sqlalchemy import text


def reset_database():
    app = create_app()

    with app.app_context():
        print("Полный сброс базы данных...")

        # Отключаем внешние ключи для PostgreSQL
        # db.session.execute(text('SET session_replication_role = replica;'))

        # Получаем все таблицы
        result = db.session.execute(text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """))

        tables = [row[0] for row in result]
        print(f"Найдено таблиц: {tables}")

        # Удаляем все таблицы
        for table in tables:
            if table != 'alembic_version':  # Пропускаем таблицу миграций
                print(f"Удаляем таблицу: {table}")
                db.session.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))

        # Удаляем таблицу миграций отдельно
        db.session.execute(text('DROP TABLE IF EXISTS alembic_version'))

        db.session.commit()
        print("Все таблицы удалены!")

        # Включаем внешние ключи обратно
        # db.session.execute(text('SET session_replication_role = origin;'))


if __name__ == '__main__':
    reset_database()