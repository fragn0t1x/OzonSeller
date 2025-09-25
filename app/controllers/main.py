# app/controllers/main.py
from flask import Blueprint, render_template
from app import db
from app.models import Product, ProductCategory, Shipment, ProductVariation, ProductPackage, StockUnpackaged, \
    StockPackaged
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

        # Правильный подсчет общего количества товаров
        total_unpackaged = db.session.query(db.func.sum(StockUnpackaged.quantity_pieces)).scalar() or 0

        total_packaged = 0
        packaged_stocks = db.session.query(StockPackaged, ProductPackage).join(
            ProductPackage, StockPackaged.package_id == ProductPackage.id
        ).all()

        for stock, package in packaged_stocks:
            total_packaged += stock.quantity_packages * package.package_quantity

        total_stock = total_unpackaged + total_packaged

        # Последние товары (5 штук)
        recent_products = Product.query.options(
            db.joinedload(Product.category)
        ).order_by(Product.created_at.desc()).limit(5).all()

        # Подсчитываем вариации и упаковки
        total_variations = ProductVariation.query.count()
        total_packages = ProductPackage.query.count()

        # Статистика по отправкам
        shipments_stats = {
            'preparing': Shipment.query.filter_by(status='preparing').count(),
            'sent': Shipment.query.filter_by(status='sent').count(),
            'delivered': Shipment.query.filter_by(status='delivered').count()
        }

        # Заглушка для последних действий
        recent_activities = [
            {'action': 'Система запущена', 'time': datetime.now().strftime('%H:%M'),
             'details': 'База данных инициализирована'},
        ]

        # Добавляем информацию о последних действиях если есть товары
        if products_count > 0:
            recent_activities.insert(0, {
                'action': f'Всего товаров: {products_count}',
                'time': datetime.now().strftime('%H:%M'),
                'details': f'Вариаций: {total_variations}, Упаковок: {total_packages}'
            })

        return render_template('index.html',
                               products_count=products_count,
                               categories_count=categories_count,
                               shipments_count=shipments_count,
                               total_stock=total_stock,
                               recent_products=recent_products,
                               total_variations=total_variations,
                               total_packages=total_packages,
                               shipments_stats=shipments_stats,
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
                               total_variations=0,
                               total_packages=0,
                               shipments_stats={'preparing': 0, 'sent': 0, 'delivered': 0},
                               recent_activities=[],
                               now=datetime.now())


@bp.route('/dashboard')
def dashboard():
    """Расширенная панель управления"""
    try:
        # Статистика по товарам
        products_by_category = db.session.query(
            ProductCategory.name,
            db.func.count(Product.id)
        ).join(Product, Product.category_id == ProductCategory.id) \
            .group_by(ProductCategory.name).all()

        # Товары с низкими остатками
        low_stock_products = []

        # Проверяем неупакованные остатки
        low_unpackaged = db.session.query(
            Product.name,
            ProductVariation,
            StockUnpackaged.quantity_pieces
        ).join(ProductVariation, ProductVariation.product_id == Product.id) \
            .join(StockUnpackaged, StockUnpackaged.variation_id == ProductVariation.id) \
            .filter(StockUnpackaged.quantity_pieces < 10) \
            .all()

        for product_name, variation, quantity in low_unpackaged:
            low_stock_products.append({
                'product': product_name,
                'type': 'неупакованный',
                'variation': f"{variation.size.name}/{variation.color.name}",
                'quantity': quantity,
                'alert': 'низкий запас' if quantity < 5 else 'средний запас'
            })

        # Последние отправки
        recent_shipments = Shipment.query.options(
            db.joinedload(Shipment.items).joinedload(ShipmentItem.package)
        ).order_by(Shipment.created_at.desc()).limit(5).all()

        return render_template('dashboard.html',
                               products_by_category=products_by_category,
                               low_stock_products=low_stock_products,
                               recent_shipments=recent_shipments,
                               now=datetime.now())

    except Exception as e:
        print(f"Ошибка в dashboard: {e}")
        return render_template('dashboard.html',
                               products_by_category=[],
                               low_stock_products=[],
                               recent_shipments=[],
                               now=datetime.now())


@bp.route('/health')
def health_check():
    """Проверка состояния системы"""
    try:
        # Проверяем подключение к базе данных
        db.session.execute(text('SELECT 1'))
        db_status = 'OK'

        # Проверяем основные таблицы
        tables = {
            'products': Product.query.count(),
            'categories': ProductCategory.query.count(),
            'variations': ProductVariation.query.count(),
            'packages': ProductPackage.query.count(),
            'shipments': Shipment.query.count()
        }

        return {
            'status': 'healthy',
            'database': db_status,
            'tables': tables,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, 500