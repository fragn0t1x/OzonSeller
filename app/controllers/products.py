# app/controllers/products.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app import db
from app.models import Product, ProductVariation, ProductPackage, StockMovement
from app.models.category import ProductCategory

bp = Blueprint('products', __name__)


@bp.route('/')
def products_list():
    """Список всех товаров"""
    page = request.args.get('page', 1, type=int)

    products = Product.query.options(
        db.joinedload(Product.category),
        db.joinedload(Product.variations)
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

            # Сначала создаем вариации (размер-цвет)
            sizes = request.form.getlist('sizes[]')
            colors = request.form.getlist('colors[]')

            # Уникальные комбинации размер-цвет
            variations_created = set()

            for size, color in zip(sizes, colors):
                if not size.strip() and not color.strip():
                    continue

                variation_key = (size.strip(), color.strip())
                if variation_key not in variations_created:
                    variation = ProductVariation(
                        product_id=product.id,
                        size=size.strip() if size.strip() else None,
                        color=color.strip() if color.strip() else None,
                        quantity=0
                    )
                    db.session.add(variation)
                    variations_created.add(variation_key)

            db.session.flush()

            # Теперь создаем упаковки для каждой вариации
            package_sizes = request.form.getlist('package_sizes[]')
            package_colors = request.form.getlist('package_colors[]')
            package_quantities = request.form.getlist('package_quantities[]')
            skus = request.form.getlist('skus[]')

            for size, color, package_qty, sku in zip(package_sizes, package_colors, package_quantities, skus):
                if not sku.strip():
                    continue

                # Находим соответствующую вариацию
                variation = ProductVariation.query.filter_by(
                    product_id=product.id,
                    size=size.strip() if size.strip() else None,
                    color=color.strip() if color.strip() else None
                ).first()

                if variation:
                    package = ProductPackage(
                        variation_id=variation.id,
                        package_quantity=int(package_qty) if package_qty and package_qty.strip() else 1,
                        sku=sku.strip(),
                        quantity=0
                    )
                    db.session.add(package)

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

    # Получаем все вариации этого товара
    variations = ProductVariation.query.filter_by(product_id=product_id).all()

    # Группируем данные для отображения
    size_color_groups = {}

    for variation in variations:
        key = (variation.size or 'Без размера', variation.color or 'Без цвета')
        if key not in size_color_groups:
            size_color_groups[key] = {
                'size': variation.size,
                'color': variation.color,
                'unpacked_quantity': variation.quantity,
                'packages': []
            }

        # Получаем упаковки для этой вариации
        packages = ProductPackage.query.filter_by(variation_id=variation.id).all()
        for package in packages:
            size_color_groups[key]['packages'].append(package)

    return render_template('products/detail.html',
                           product=product,
                           size_color_groups=list(size_color_groups.values()))


# НОВЫЕ МАРШРУТЫ ДЛЯ ПРИХОДА И УПАКОВКИ
@bp.route('/<int:product_id>/incoming', methods=['GET', 'POST'])
def product_incoming(product_id):
    """Приход товара"""
    product = Product.query.get_or_404(product_id)
    variations = ProductVariation.query.filter_by(product_id=product_id).all()

    if request.method == 'POST':
        try:
            for variation in variations:
                quantity_field = f'quantity_{variation.id}'
                quantity = request.form.get(quantity_field, '0').strip()

                if quantity and int(quantity) > 0:
                    quantity = int(quantity)
                    variation.quantity += quantity

                    movement = StockMovement(
                        product_id=product_id,
                        size=variation.size,
                        color=variation.color,
                        movement_type='incoming',
                        quantity=quantity,
                        comment=f'Приход товара: {product.name}'
                    )
                    db.session.add(movement)

            db.session.commit()
            flash('Приход успешно добавлен!', 'success')
            return redirect(url_for('products.product_detail', product_id=product_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении прихода: {str(e)}', 'danger')

    return render_template('products/incoming.html', product=product, variations=variations)


@bp.route('/<int:product_id>/packing', methods=['GET', 'POST'])
def product_packing(product_id):
    """Упаковка товара"""
    product = Product.query.get_or_404(product_id)

    variations = ProductVariation.query.filter_by(product_id=product_id).filter(
        ProductVariation.quantity > 0
    ).all()

    packing_data = []
    for variation in variations:
        packages = ProductPackage.query.filter_by(variation_id=variation.id).all()
        if packages:
            packing_data.append({
                'variation': variation,
                'packages': packages,
                'remaining_quantity': variation.quantity
            })

    if request.method == 'POST':
        try:
            form_data = []
            for item in packing_data:
                for package in item['packages']:
                    quantity_field = f'quantity_{item["variation"].id}_{package.id}'
                    quantity = request.form.get(quantity_field, '0').strip()

                    if quantity and int(quantity) > 0:
                        form_data.append({
                            'variation_id': item['variation'].id,
                            'package_id': package.id,
                            'quantity': int(quantity),
                            'package_quantity': package.package_quantity,
                            'sku': package.sku
                        })

            # Проверяем достаточно ли товара
            for item in form_data:
                variation = ProductVariation.query.get(item['variation_id'])
                units_needed = item['quantity'] * item['package_quantity']

                if variation.quantity < units_needed:
                    flash(
                        f'Недостаточно товара для упаковки {item["sku"]}. Доступно: {variation.quantity} шт., требуется: {units_needed} шт.',
                        'danger')
                    return redirect(url_for('products.product_packing', product_id=product_id))

            # Выполняем упаковку
            for item in form_data:
                variation = ProductVariation.query.get(item['variation_id'])
                package = ProductPackage.query.get(item['package_id'])

                units_needed = item['quantity'] * item['package_quantity']
                variation.quantity -= units_needed
                package.quantity += item['quantity']

                movement = StockMovement(
                    product_id=product_id,
                    size=variation.size,
                    color=variation.color,
                    movement_type='packing',
                    quantity=item['quantity'],
                    package_quantity=item['package_quantity'],
                    comment=f'Упаковка: {item["quantity"]} уп. по {item["package_quantity"]} шт. ({item["sku"]})'
                )
                db.session.add(movement)

            db.session.commit()
            flash('Товар успешно упакован!', 'success')
            return redirect(url_for('products.product_detail', product_id=product_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при упаковке: {str(e)}', 'danger')

    return render_template('products/packing.html', product=product, packing_data=packing_data)


@bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """Удаление товара"""
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
        flash('Товар успешно удален!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении товара: {str(e)}', 'danger')

    return redirect(url_for('products.products_list'))