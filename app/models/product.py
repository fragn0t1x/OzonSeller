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
    __tablename__ = 'product_variations'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('category_sizes.id'), nullable=False)  # Правильно!
    color_id = db.Column(db.Integer, db.ForeignKey('category_colors.id'), nullable=False)  # Правильно!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    size = db.relationship('CategorySize', backref='variations')
    color = db.relationship('CategoryColor', backref='variations')
    packages = db.relationship('ProductPackage', backref='variation', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ProductVariation {self.size.name} - {self.color.name}>'

class ProductPackage(db.Model):
    __tablename__ = 'product_packages'

    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('product_variations.id', ondelete='CASCADE'), nullable=False)
    package_quantity = db.Column(db.Integer, nullable=False)
    sku = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ProductPackage {self.sku}>'

    @property
    def total_quantity_pieces(self):
        from app.models.stock import StockPackaged
        stock = StockPackaged.query.filter_by(package_id=self.id).first()
        if stock:
            return stock.quantity_packages * self.package_quantity
        return 0