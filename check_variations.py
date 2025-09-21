#!/usr/bin/env python3
"""
Проверка подсчета вариаций
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product, ProductVariation


def check_variations():
    app = create_app()

    with app.app_context():
        print("=== Checking Variations ===")

        products = Product.query.all()
        for product in products:
            # Прямой запрос к базе
            direct_count = ProductVariation.query.filter_by(product_id=product.id).count()

            # Через метод
            method_count = product.variations_count

            # Через явный запрос
            explicit_count = len(product.get_variations())

            print(f"Product: {product.name}")
            print(f"  Direct count: {direct_count}")
            print(f"  Method count: {method_count}")
            print(f"  Explicit count: {explicit_count}")
            print(f"  Variations: {[v.sku for v in product.get_variations()]}")
            print()


if __name__ == '__main__':
    check_variations()