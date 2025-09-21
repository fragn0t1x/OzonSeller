from flask import Blueprint, render_template
from app import db
from app.models import Product, ProductVariation, OurWarehouseStock

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Главная страница с общей статистикой"""
    products_count = Product.query.count()
    variations_count = ProductVariation.query.count()

    # Подсчет общего количества товаров на складе
    total_stock = db.session.query(
        db.func.coalesce(db.func.sum(OurWarehouseStock.unpacked_quantity + OurWarehouseStock.packed_quantity), 0)
    ).scalar()

    return render_template('index.html',
                           products_count=products_count,
                           variations_count=variations_count,
                           total_stock=total_stock)