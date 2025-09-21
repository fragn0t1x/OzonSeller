#!/usr/bin/env python3
"""
Проверка текущего состояния базы данных
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product, ProductVariation, OzonCategory


def check_database():
    app = create_app()

    with app.app_context():
        print("=== Database Check ===")

        # Проверяем таблицы
        tables = db.inspect(db.engine).get_table_names()
        print(f"Tables in database: {tables}")

        # Проверяем количество записей
        print(f"Products count: {Product.query.count()}")
        print(f"Variations count: {ProductVariation.query.count()}")
        print(f"Categories count: {OzonCategory.query.count()}")

        # Проверяем первые записи
        products = Product.query.all()
        for product in products:
            print(f"Product: {product.name}, Variations: {product.variations_count}")
            if product.category:
                print(f"  Category: {product.category.category_name}")

            # Показываем вариации для товаров с 0 вариациями (для диагностики)
            if product.variations_count == 0:
                variations = ProductVariation.query.filter_by(product_id=product.id).all()
                print(f"  DEBUG: Direct query found {len(variations)} variations")
                for v in variations:
                    print(f"    - {v.sku}: product_id={v.product_id}")


if __name__ == '__main__':
    check_database()