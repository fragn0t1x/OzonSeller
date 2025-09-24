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

    category = db.relationship('ProductCategory', backref='products')
    variations = db.relationship('ProductVariation', backref='product', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.name}>'

class ProductVariation(db.Model):
    """Неупакованные товары (связь с справочниками размеров/цветов)"""
    __tablename__ = 'product_variations'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)  # Ссылка на справочник
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)  # Ссылка на справочник
    # УБИРАЕМ quantity - теперь в StockUnpackaged
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    size = db.relationship('Size', backref='variations')
    color = db.relationship('Color', backref='variations')
    packages = db.relationship('ProductPackage', backref='variation', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ProductVariation {self.size.name} - {self.color.name}>'

class ProductPackage(db.Model):
    """Упакованные товары (только связь с вариацией)"""
    __tablename__ = 'product_packages'

    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('product_variations.id', ondelete='CASCADE'), nullable=False)
    package_quantity = db.Column(db.Integer, nullable=False)  # Штук в упаковке
    sku = db.Column(db.String(100), nullable=False, unique=True)  # Артикул
    # УБИРАЕМ quantity - теперь в StockPackaged
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ProductPackage {self.sku}>'

    @property
    def total_quantity_pieces(self):
        """Общее количество штук в упаковках"""
        from app.models.stock import StockPackaged
        stock = StockPackaged.query.filter_by(package_id=self.id).first()
        if stock:
            return stock.quantity_packages * self.package_quantity
        return 0