# app/models/product.py
from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship('ProductCategory', backref='products', foreign_keys=[category_id])
    variations = db.relationship('ProductVariation', backref='product', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.name}>'

    @property
    def total_variations_count(self):
        return len(self.variations)


class ProductVariation(db.Model):
    """Неупакованные товары (размер, цвет, общее количество штук)"""
    __tablename__ = 'product_variations'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=0)  # Общее количество штук для этой вариации

    # Связь с упаковками для этой вариации
    packages = db.relationship('ProductPackage', backref='variation', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ProductVariation {self.size} - {self.color}>'


class ProductPackage(db.Model):
    """Упакованные товары (варианты упаковки для конкретной вариации)"""
    __tablename__ = 'product_packages'
    __table_args__ = {'extend_existing': True}  # Добавляем эту строку

    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('product_variations.id', ondelete='CASCADE'), nullable=False)
    package_quantity = db.Column(db.Integer, default=1)  # Штук в упаковке
    sku = db.Column(db.String(255), nullable=False)  # Артикул
    quantity = db.Column(db.Integer, default=0)  # Количество упаковок

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ProductPackage {self.sku} - {self.quantity} уп.>'

    @property
    def total_quantity(self):
        """Общее количество штук в упаковках"""
        return self.quantity * self.package_quantity