# update_database.py
from app import create_app, db
from app.models.category import ProductCategory, CategorySize, CategoryColor


def update_database():
    app = create_app()

    with app.app_context():
        # Создаем таблицы
        db.create_all()
        print("База данных обновлена!")


if __name__ == '__main__':
    update_database()