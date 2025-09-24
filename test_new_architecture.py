from app import create_app, db
from app.models import Product, Size, Color, ProductVariation, ProductPackage, StockUnpackaged, StockPackaged


def test_architecture():
    app = create_app()

    with app.app_context():
        print("=== ТЕСТИРОВАНИЕ НОВОЙ АРХИТЕКТУРЫ ===")

        # 1. Проверяем справочники
        sizes = Size.query.all()
        colors = Color.query.all()
        print(f"Размеры: {[s.name for s in sizes]}")
        print(f"Цвета: {[c.name for c in colors]}")

        # 2. Проверяем товары
        products = Product.query.all()
        for product in products:
            print(f"\nТовар: {product.name}")

            for variation in product.variations:
                # Получаем остаток неупакованного
                unpackaged_stock = StockUnpackaged.query.filter_by(variation_id=variation.id).first()

                print(f"  Вариация: {variation.size.name} - {variation.color.name}")
                print(f"    Неупаковано: {unpackaged_stock.quantity_pieces if unpackaged_stock else 0} шт.")

                for package in variation.packages:
                    # Получаем остаток упакованного
                    packaged_stock = StockPackaged.query.filter_by(package_id=package.id).first()

                    print(
                        f"    Упаковка: {package.sku} - {packaged_stock.quantity_packages if packaged_stock else 0} уп.")

        print("\n=== ТЕСТ ЗАВЕРШЕН ===")


if __name__ == '__main__':
    test_architecture()