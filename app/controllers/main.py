from flask import Blueprint, render_template
from app import db
from app.models import Product, ProductCategory, Shipment, ProductVariation  # Добавляем импорт
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Главная страница с общей статистикой"""
    try:
        # Основные счетчики
        products_count = Product.query.count()
        categories_count = ProductCategory.query.count()
        shipments_count = Shipment.query.count()

        # Упрощенный подсчет общего количества товаров
        total_stock = 0

        # Последние товары (5 штук)
        recent_products = Product.query.options(
            db.joinedload(Product.category)
        ).order_by(Product.created_at.desc()).limit(5).all()

        # Все товары для статистики вариаций
        products = Product.query.all()

        # Подсчитываем вариации и упаковки отдельными запросами
        total_variations = ProductVariation.query.count()

        # Упрощенный подсчет упаковок
        from app.models import ProductPackage
        total_packages = ProductPackage.query.count()

        # Заглушка для последних действий
        recent_activities = [
            {'action': 'Система запущена', 'time': 'Только что', 'details': 'База данных инициализирована'},
        ]

        return render_template('index.html',
                               products_count=products_count,
                               categories_count=categories_count,
                               shipments_count=shipments_count,
                               total_stock=total_stock,
                               recent_products=recent_products,
                               products=products,
                               total_variations=total_variations,
                               total_packages=total_packages,
                               recent_activities=recent_activities,
                               now=datetime.now())

    except Exception as e:
        print(f"Ошибка на главной странице: {e}")
        # Если вообще ничего не работает, показываем базовую страницу
        return render_template('index.html',
                               products_count=0,
                               categories_count=0,
                               shipments_count=0,
                               total_stock=0,
                               recent_products=[],
                               products=[],
                               total_variations=0,
                               total_packages=0,
                               recent_activities=[],
                               now=datetime.now())