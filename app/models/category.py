from app import db
from datetime import datetime


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Уберите это отношение, так как оно уже определено в Product
    # products = db.relationship('Product', backref='category_rel', lazy=True)

    def __repr__(self):
        return f'<ProductCategory {self.name}>'

    def get_products_count(self):
        """Получаем количество товаров в категории"""
        from app.models import Product
        return Product.query.filter_by(category_id=self.id).count()