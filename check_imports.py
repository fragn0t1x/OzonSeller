# check_imports.py
try:
    from app.models.category import ProductCategory, CategorySize, CategoryColor

    print("✓ Модели категорий импортированы правильно")

    from app.models.product import Product, ProductVariation, ProductPackage

    print("✓ Модели товаров импортированы правильно")

    from app.controllers.products import bp as products_bp

    print("✓ Контроллер товаров импортирован правильно")

    from app.controllers.categories import bp as categories_bp

    print("✓ Контроллер категорий импортирован правильно")

    from app.controllers.shipments import bp as shipments_bp

    print("✓ Контроллер отправок импортирован правильно")

    # Проверяем что старые модели не импортируются
    try:
        from app.models.size import Size

        print("✗ Старая модель Size все еще импортируется!")
    except ImportError:
        print("✓ Старая модель Size удалена")

    try:
        from app.models.color import Color

        print("✗ Старая модель Color все еще импортируется!")
    except ImportError:
        print("✓ Старая модель Color удалена")

    print("✓ Все импорты проверены успешно!")

except Exception as e:
    print(f"✗ Ошибка импорта: {e}")