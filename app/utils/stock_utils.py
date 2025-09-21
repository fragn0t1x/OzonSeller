from app import db
from app.models import OurWarehouseStock

def create_stock_for_variation(variation_id):
    """Создает запись об остатках для вариации"""
    stock = OurWarehouseStock(variation_id=variation_id)
    db.session.add(stock)
    return stock

def get_stock_for_variation(variation_id):
    """Получает остатки для вариации"""
    return OurWarehouseStock.query.filter_by(variation_id=variation_id).first()