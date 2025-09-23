# app/models/__init__.py
from app.models.category import ProductCategory
from app.models.product import Product, ProductVariation, ProductPackage
from app.models.shipment import Shipment, ShipmentItem
from app.models.stock_movement import StockMovement  # Добавляем

__all__ = [
    'ProductCategory',
    'Product',
    'ProductVariation',
    'ProductPackage',
    'Shipment',
    'ShipmentItem'
]