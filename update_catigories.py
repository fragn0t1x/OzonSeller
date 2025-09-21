#!/usr/bin/env python3
"""
Обновление названий категорий для существующих товаров
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import OzonCategory
from app.services import OzonService


def update_existing_categories():
    app = create_app()

    with app.app_context():
        print("=== Updating Existing Categories ===")

        ozon_service = OzonService()
        categories = OzonCategory.query.all()

        updated_count = 0
        for category in categories:
            if category.category_name.startswith('Категория '):
                # Пытаемся получить настоящее название
                real_name = ozon_service.get_category_name_by_id(category.category_id)
                if real_name:
                    old_name = category.category_name
                    category.category_name = real_name
                    updated_count += 1
                    print(f"Updated: {old_name} -> {real_name}")

        if updated_count > 0:
            db.session.commit()
            print(f"Updated {updated_count} categories")
        else:
            print("No categories need updating")

        print("Update completed!")


if __name__ == '__main__':
    update_existing_categories()