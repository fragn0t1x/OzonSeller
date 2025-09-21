#!/usr/bin/env python3
"""
Диагностика проблем с вариациями
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product, ProductVariation


def diagnose_variations():
    app = create_app()

    with app.app_context():
        print("=== Variation Diagnosis ===")

        # 1. Проверяем все товары с нулевым количеством вариаций
        products_with_no_variations = Product.query.all()

        for product in products_with_no_variations:
            # Прямой запрос к вариациям
            direct_variations = ProductVariation.query.filter_by(product_id=product.id).all()

            print(f"Product: {product.name} (ID: {product.id})")
            print(f"  variations_count: {product.variations_count}")
            print(f"  get_variations(): {len(product.get_variations())}")
            print(f"  direct query: {len(direct_variations)}")

            if direct_variations:
                print(f"  Found variations:")
                for v in direct_variations:
                    print(f"    - {v.sku} (ID: {v.id}, Product ID: {v.product_id})")
                    print(f"      Size: {v.size}, Color: {v.color}, Package: {v.package_quantity}")

            print()


if __name__ == '__main__':
    diagnose_variations()