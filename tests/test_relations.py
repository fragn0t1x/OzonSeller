#!/usr/bin/env python3
"""
Тест отношений между моделями
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product, ProductVariation, OzonCategory


def test_relations():
    app = create_app()

    with app.app_context():
        print("Testing database relations...")

        try:
            # Создаем тестовую категорию
            category = OzonCategory(
                category_id=999999,
                category_name="Тестовая категория",
                disabled=False
            )
            db.session.add(category)
            db.session.flush()

            print(f"Created category: {category.id}")

            # Создаем тестовый товар
            product = Product(
                name="Тестовый товар",
                category_id=category.id
            )
            db.session.add(product)
            db.session.flush()

            print(f"Created product: {product.id}")
            print(f"Product category: {product.category.category_name if product.category else 'None'}")

            # Создаем вариации
            variations = [
                ProductVariation(product_id=product.id, sku="TEST-001", size="M", color="черный", package_quantity=1),
                ProductVariation(product_id=product.id, sku="TEST-002", size="L", color="белый", package_quantity=1),
            ]

            for variation in variations:
                db.session.add(variation)

            db.session.flush()

            print(f"Created variations: {[v.sku for v in variations]}")

            # Используем правильные методы вместо отношений
            print(f"Product variations count: {product.variations_count}")
            print(f"Product variations: {[v.sku for v in product.get_variations()]}")

            # Проверяем обратную связь через метод
            print(f"Category products count: {len(category.get_products())}")

            # Проверяем работу с остатками
            for variation in variations:
                stock = variation.get_stock()
                print(f"Variation {variation.sku} stock: {stock}")

            # Очищаем
            db.session.rollback()
            print("Test completed successfully!")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


if __name__ == '__main__':
    test_relations()