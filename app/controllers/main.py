# app/controllers/main.py
from flask import Blueprint, render_template
from app import db
from app.models import Product, ProductVariation, ProductPackage

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Главная страница с общей статистикой"""
    products_count = Product.query.count()
    variations_count = ProductVariation.query.count()
    packages_count = ProductPackage.query.count()

    # Подсчет общего количества товаров на складе
    total_unpacked = db.session.query(
        db.func.coalesce(db.func.sum(ProductVariation.quantity), 0)
    ).scalar()

    total_packed = db.session.query(
        db.func.coalesce(db.func.sum(ProductPackage.quantity * ProductPackage.package_quantity), 0)
    ).scalar()

    total_stock = total_unpacked + total_packed

    return render_template('index.html',
                           products_count=products_count,
                           variations_count=variations_count,
                           packages_count=packages_count,
                           total_stock=total_stock)