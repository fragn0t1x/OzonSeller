#!/usr/bin/env python3
"""
Обновление иерархии категорий для существующих товаров
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import OzonCategory
from app.services import OzonService


def update_categories_hierarchy():
    app = create_app()

    with app.app_context():
        print("=== Updating Categories Hierarchy ===")

        ozon_service = OzonService()
        categories = OzonCategory.query.all()

        updated_count = 0
        error_count = 0

        for category in categories:
            try:
                # Получаем полную иерархию для каждой категории
                category_data = ozon_service.get_category_with_parents(category.category_id)

                if category_data:
                    # Обновляем поля иерархии
                    full_path = ozon_service.build_category_full_path(category_data)
                    level = ozon_service.get_category_level(category_data)
                    parent_id = ozon_service.get_parent_id_from_category_data(category_data)

                    category.full_path = full_path
                    category.level = level
                    category.parent_category_id = parent_id

                    updated_count += 1
                    print(f"Updated: {full_path} (Level: {level})")
                else:
                    print(f"Warning: No data for category ID {category.category_id}")
                    error_count += 1

            except Exception as e:
                print(f"Error processing category {category.category_id}: {e}")
                error_count += 1
                continue

        if updated_count > 0:
            db.session.commit()
            print(f"Successfully updated {updated_count} categories with hierarchy")
        else:
            print("No categories were updated")

        if error_count > 0:
            print(f"Encountered {error_count} errors during update")

        print("Hierarchy update completed!")


if __name__ == '__main__':
    update_categories_hierarchy()