# app/utils/stock_utils.py
from app import db
from app.models import ProductVariation, ProductPackage
# Если файл существует, нужно обновить импорты
from app.models.category import CategorySize, CategoryColor  # Заменяем старые импорты

def create_variation(product_id, size, color):
    """Создает вариацию товара (неупакованный)"""
    variation = ProductVariation(
        product_id=product_id,
        size=size,
        color=color,
        quantity=0
    )
    db.session.add(variation)
    return variation

def create_package(product_id, size, color, package_quantity, sku):
    """Создает упаковку товара"""
    package = ProductPackage(
        product_id=product_id,
        size=size,
        color=color,
        package_quantity=package_quantity,
        sku=sku,
        quantity=0
    )
    db.session.add(package)
    return package

def get_variation(product_id, size, color):
    """Находит вариацию по характеристикам"""
    return ProductVariation.query.filter_by(
        product_id=product_id,
        size=size,
        color=color
    ).first()

def get_package(product_id, size, color, package_quantity, sku):
    """Находит упаковку по характеристикам"""
    return ProductPackage.query.filter_by(
        product_id=product_id,
        size=size,
        color=color,
        package_quantity=package_quantity,
        sku=sku
    ).first()