# app/models/category.py
from app import db
from datetime import datetime

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sizes = db.relationship('CategorySize', backref='category', cascade='all, delete-orphan', lazy='dynamic')
    colors = db.relationship('CategoryColor', backref='category', cascade='all, delete-orphan', lazy='dynamic')
    package_quantities = db.relationship('CategoryPackageQuantity', backref='category', cascade='all, delete-orphan', lazy='dynamic')  # Новое!

    def __repr__(self):
        return f'<ProductCategory {self.name}>'

    def get_products_count(self):
        from app.models import Product
        return Product.query.filter_by(category_id=self.id).count()


class CategorySize(db.Model):
    __tablename__ = 'category_sizes'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('category_id', 'name', name='_category_size_uc'),
    )

    def __repr__(self):
        return f'<CategorySize {self.name}>'


class CategoryColor(db.Model):
    __tablename__ = 'category_colors'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    hex_code = db.Column(db.String(7), default='#6c757d')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('category_id', 'name', name='_category_color_uc'),
    )

    def __repr__(self):
        return f'<CategoryColor {self.name}>'


class CategoryPackageQuantity(db.Model):
    __tablename__ = 'category_package_quantities'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # Количество штук в упаковке
    description = db.Column(db.String(100))  # Например: "Маленькая упаковка", "Большая упаковка"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('category_id', 'quantity', name='_category_package_qty_uc'),
    )

    def __repr__(self):
        return f'<CategoryPackageQuantity {self.quantity}шт>'