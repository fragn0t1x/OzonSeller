#!/usr/bin/env python3
"""
Создание начальных данных
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import ProductCategory


def create_initial_data():
    app = create_app()

    with app.app_context():
        print("Creating initial data...")

        # Создаем основные категории
        categories = [
            ProductCategory(name="Носки", description="Спортивные и повседневные носки"),
            ProductCategory(name="Футболки", description="Мужские и женские футболки"),
            ProductCategory(name="Обувь", description="Кроссовки и кеды"),
            ProductCategory(name="Аксессуары", description="Ремни, сумки, головные уборы"),
        ]

        for category in categories:
            db.session.add(category)

        db.session.commit()
        print("Initial categories created successfully!")


if __name__ == '__main__':
    create_initial_data()