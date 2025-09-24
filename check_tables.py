from app import create_app, db
from sqlalchemy import inspect


def check_tables():
    app = create_app()

    with app.app_context():
        print("Проверяем существующие таблицы...")

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        print("Таблицы в базе данных:")
        required_tables = [
            'product_categories', 'products', 'sizes', 'colors',
            'product_variations', 'product_packages',
            'stock_unpackaged', 'stock_packaged',
            'shipments', 'shipment_items'
        ]

        for table in required_tables:
            if table in tables:
                print(f"  ✅ {table}")
            else:
                print(f"  ❌ {table} - ОТСУТСТВУЕТ")

        # Проверяем структуру ключевых таблиц
        if 'stock_unpackaged' in tables:
            print("\nСтруктура stock_unpackaged:")
            columns = inspector.get_columns('stock_unpackaged')
            for col in columns:
                print(f"  - {col['name']} ({col['type']})")


if __name__ == '__main__':
    check_tables()