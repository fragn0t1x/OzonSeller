#!/usr/bin/env python3
"""
Скрипт для заполнения базы тестовыми данными
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import OzonCategory, Product, ProductVariation, OurWarehouseStock
from tests.test_data import TEST_CATEGORIES, TEST_PRODUCTS, TEST_VARIATIONS


def populate_test_data():
    """Заполнение базы тестовыми данными"""
    app = create_app()

    with app.app_context():
        print("🧹 Очистка базы данных...")
        # Очищаем данные в правильном порядке (из-за foreign keys)
        OurWarehouseStock.query.delete()
        ProductVariation.query.delete()
        Product.query.delete()
        OzonCategory.query.delete()
        db.session.commit()

        print("📦 Добавление тестовых категорий...")
        for category_data in TEST_CATEGORIES:
            category = OzonCategory(**category_data)
            db.session.add(category)
        db.session.commit()

        print("🛍️ Добавление тестовых товаров...")
        for product_data in TEST_PRODUCTS:
            product = Product(**product_data)
            db.session.add(product)
        db.session.commit()

        print("📊 Добавление тестовых вариаций...")
        for variation_data in TEST_VARIATIONS:
            variation = ProductVariation(**variation_data)
            db.session.add(variation)
            # Создаем запись об остатках для каждой вариации
            stock = OurWarehouseStock(variation=variation)
            db.session.add(stock)
        db.session.commit()

        print("✅ Тестовые данные успешно добавлены!")
        print(f"📊 Категорий: {len(TEST_CATEGORIES)}")
        print(f"🛍️ Товаров: {len(TEST_PRODUCTS)}")
        print(f"📊 Вариаций: {len(TEST_VARIATIONS)}")


if __name__ == '__main__':
    populate_test_data()