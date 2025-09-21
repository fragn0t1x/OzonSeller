from app import create_app, db

app = create_app()

with app.app_context():
    # Создаем все таблицы
    db.create_all()
    print("Все таблицы созданы успешно!")

    # Помечаем миграцию как примененную
    from alembic.util import CommandError

    try:
        from alembic.config import Config
        from alembic import command

        alembic_cfg = Config("migrations/alembic.ini")
        alembic_cfg.set_main_option("script_location", "migrations")
        command.stamp(alembic_cfg, "initial")
        print("Миграция помечена как примененная")
    except Exception as e:
        print(f"Не удалось пометить миграцию: {e}")