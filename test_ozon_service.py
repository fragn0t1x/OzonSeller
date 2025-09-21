#!/usr/bin/env python3
"""
Тест методов OzonService
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services import OzonService


def test_ozon_service():
    app = create_app()

    with app.app_context():
        print("=== Testing OzonService Methods ===")

        ozon_service = OzonService()

        # Тестируем получение категорий
        categories = ozon_service.get_categories()
        print(f"Categories data: {bool(categories)}")

        if categories:
            # Тестируем получение иерархии для известной категории
            test_category_id = 200001517  # Замените на реальный ID из вашей базы
            category_data = ozon_service.get_category_with_parents(test_category_id)

            print(f"Category data for ID {test_category_id}: {bool(category_data)}")

            if category_data:
                full_path = ozon_service.build_category_full_path(category_data)
                level = ozon_service.get_category_level(category_data)

                print(f"Full path: {full_path}")
                print(f"Level: {level}")
                print(f"Category: {category_data['category']}")
                print(f"Parents: {[p['category_name'] for p in category_data.get('parents', [])]}")


if __name__ == '__main__':
    test_ozon_service()