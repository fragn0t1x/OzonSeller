from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app import db
from app.models import Product, ProductVariation, OurWarehouseStock
from app.models.category import ProductCategory
from app.utils.stock_utils import create_stock_for_variation

bp = Blueprint('products', __name__)


@bp.route('/')
def products_list():
    """Список всех товаров"""
    page = request.args.get('page', 1, type=int)

    products = Product.query.options(
        db.joinedload(Product.category)
    ).order_by(Product.name).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False
    )

    return render_template('products/list.html', products=products)


@bp.route('/add', methods=['GET', 'POST'])
def add_product():
    """Добавление нового товара"""
    categories = ProductCategory.query.order_by(ProductCategory.name).all()

    if request.method == 'POST':
        try:
            # Создаем основной товар
            product = Product(
                name=request.form['name'],
                category_id=request.form['category_id'],
                description=request.form.get('description', '')
            )
            db.session.add(product)
            db.session.flush()

            # Обрабатываем позиции
            sizes = request.form.getlist('sizes[]')
            colors = request.form.getlist('colors[]')
            package_quantities = request.form.getlist('package_quantities[]')
            skus = request.form.getlist('skus[]')

            for size, color, package_qty, sku in zip(sizes, colors, package_quantities, skus):
                if not sku.strip():
                    continue

                variation = ProductVariation(
                    product_id=product.id,
                    sku=sku.strip(),
                    size=size.strip() if size.strip() else None,
                    color=color.strip() if color.strip() else None,
                    package_quantity=int(package_qty) if package_qty and package_qty.strip() else 1
                )

                db.session.add(variation)
                db.session.flush()

                # Создаем остатки для позиции
                create_stock_for_variation(variation.id)

            db.session.commit()
            flash('Товар успешно добавлен!', 'success')
            return redirect(url_for('products.products_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении товара: {str(e)}', 'danger')

    return render_template('products/add.html', categories=categories)


@bp.route('/<int:product_id>')
def product_detail(product_id):
    """Детальная информация о товаре"""
    product = Product.query.get_or_404(product_id)
    variations = ProductVariation.query.filter_by(product_id=product_id).all()

    # Загружаем остатки для каждой вариации
    variations_with_stock = []
    for variation in variations:
        stock = variation.get_stock()

        # Правильный расчет общего количества
        if stock:
            unpacked_total = stock.unpacked_quantity
            packed_total = stock.packed_quantity * variation.package_quantity
            total = unpacked_total + packed_total
        else:
            unpacked_total = 0
            packed_total = 0
            total = 0

        variations_with_stock.append({
            'variation': variation,
            'stock': stock,
            'unpacked_total': unpacked_total,
            'packed_total': packed_total,
            'total': total
        })

    return render_template('products/detail.html',
                           product=product,
                           variations_with_stock=variations_with_stock)