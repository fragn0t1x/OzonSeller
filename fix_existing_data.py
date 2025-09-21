#!/usr/bin/env python3
"""
Исправление существующих данных в базе
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product, ProductVariation


def fix_existing_data():
    app = create_app()

    with app.app_context():
        print("=== Fixing Existing Data ===")

        # 1. Исправляем package_quantity для существующих вариаций
        variations = ProductVariation.query.filter(
            (ProductVariation.package_quantity == None) |
            (ProductVariation.package_quantity == 0)
        ).all()

        print(f"Found {len(variations)} variations with invalid package_quantity")

        for variation in variations:
            variation.package_quantity = 1
            print(f"Fixed variation {variation.sku}: package_quantity = 1")

        # 2. Перегенерируем variation_name для всех вариаций
        all_variations = ProductVariation.query.all()
        print(f"Regenerating variation_name for {len(all_variations)} variations")

        for variation in all_variations:
            variation._generate_variation_name()
            print(f"Regenerated: {variation.variation_name}")

        db.session.commit()
        print("Data fix completed!")


if __name__ == '__main__':
    fix_existing_data()