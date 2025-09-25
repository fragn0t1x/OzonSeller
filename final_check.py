# final_check.py
from app import create_app, db
from app.models.category import CategorySize


def check_database():
    app = create_app()

    with app.app_context():
        try:
            # Проверяем что поле package_quantity существует
            sizes = CategorySize.query.limit(1).all()
            if sizes:
                size = sizes[0]
                if hasattr(size, 'package_quantity'):
                    print("✓ Поле package_quantity существует в CategorySize")
                else:
                    print("✗ Поле package_quantity отсутствует в CategorySize")

            # Проверяем связи
            from sqlalchemy.engine import reflection
            inspector = reflection.Inspector.from_engine(db.engine)

            # Проверяем foreign keys
            fks = inspector.get_foreign_keys('product_variations')
            size_fk_exists = any(fk['referred_table'] == 'category_sizes' for fk in fks)
            color_fk_exists = any(fk['referred_table'] == 'category_colors' for fk in fks)

            if size_fk_exists:
                print("✓ Foreign key на category_sizes существует")
            else:
                print("✗ Foreign key на category_sizes отсутствует")

            if color_fk_exists:
                print("✓ Foreign key на category_colors существует")
            else:
                print("✗ Foreign key на category_colors отсутствует")

        except Exception as e:
            print(f"✗ Ошибка проверки базы данных: {e}")


if __name__ == '__main__':
    check_database()