# app/controllers/products.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from app import db
from app.models import Product, ProductVariation, ProductPackage, StockUnpackaged, StockPackaged
from app.models.category import ProductCategory, CategorySize, CategoryColor  # Измененный импорт
from datetime import datetime

bp = Blueprint('products', __name__)

@bp.route('/')
def products_list():
    """Список всех товаров"""
    page = request.args.get('page', 1, type=int)

    # Упрощаем запрос - убираем сложные joins
    products = Product.query.options(
        db.joinedload(Product.category)
    ).order_by(Product.name).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False
    )

    return render_template('products/list.html',
                           products=products,
                           now=datetime.now())

@bp.route('/add', methods=['GET', 'POST'])
def add_product():
    """Добавление нового товара с новой архитектурой"""
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

            # 1. Создаем НЕУПАКОВАННЫЕ вариации (все комбинации размер-цвет)
            selected_size_ids = request.form.getlist('size_ids[]')
            selected_color_ids = request.form.getlist('color_ids[]')

            for size_id in selected_size_ids:
                for color_id in selected_color_ids:
                    if size_id and color_id:
                        # Создаем вариацию
                        variation = ProductVariation(
                            product_id=product.id,
                            size_id=int(size_id),
                            color_id=int(color_id)
                        )
                        db.session.add(variation)
                        db.session.flush()

                        # Создаем остаток для неупакованного товара
                        stock_unpackaged = StockUnpackaged(
                            variation_id=variation.id,
                            quantity_pieces=0
                        )
                        db.session.add(stock_unpackaged)

            # 2. Создаем УПАКОВАННЫЕ вариации (только выбранные упаковки)
            package_size_ids = request.form.getlist('package_size_ids[]')
            package_color_ids = request.form.getlist('package_color_ids[]')
            package_quantities = request.form.getlist('package_quantities[]')
            skus = request.form.getlist('skus[]')

            for i, (size_id, color_id, package_qty, sku) in enumerate(zip(
                    package_size_ids, package_color_ids, package_quantities, skus)):

                if not sku.strip():
                    continue

                # Находим соответствующую вариацию
                variation = ProductVariation.query.filter_by(
                    product_id=product.id,
                    size_id=int(size_id),
                    color_id=int(color_id)
                ).first()

                if variation:
                    package = ProductPackage(
                        variation_id=variation.id,
                        package_quantity=int(package_qty),
                        sku=sku.strip()
                    )
                    db.session.add(package)
                    db.session.flush()

                    # Создаем остаток для упакованного товара
                    stock_packaged = StockPackaged(
                        package_id=package.id,
                        quantity_packages=0
                    )
                    db.session.add(stock_packaged)

            db.session.commit()
            flash('Товар успешно добавлен!', 'success')
            return redirect(url_for('products.products_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении товара: {str(e)}', 'danger')

    return render_template('products/add.html',
                           categories=categories,
                           now=datetime.now())

# app/controllers/products.py - нужно обновить product_detail
@bp.route('/<int:product_id>')
def product_detail(product_id):
    """Детальная информация о товаре"""
    product = Product.query.get_or_404(product_id)

    # Получаем все вариации этого товара с остатками
    variations_with_stock = db.session.query(
        ProductVariation,
        StockUnpackaged,
        CategorySize,  # Добавляем явную загрузку размеров
        CategoryColor  # Добавляем явную загрузку цветов
    ).join(
        StockUnpackaged, ProductVariation.id == StockUnpackaged.variation_id
    ).join(
        CategorySize, ProductVariation.size_id == CategorySize.id  # Правильное соединение
    ).join(
        CategoryColor, ProductVariation.color_id == CategoryColor.id  # Правильное соединение
    ).filter(
        ProductVariation.product_id == product_id
    ).all()

    # Группируем данные для отображения
    size_color_groups = {}

    for variation, stock, size, color in variations_with_stock:  # Обновляем распаковку
        key = (size.name, color.name)  # Используем name из связанных таблиц
        if key not in size_color_groups:
            size_color_groups[key] = {
                'size': size.name,
                'color': color.name,
                'unpacked_quantity': stock.quantity_pieces,
                'packages': []
            }

        # Получаем упаковки для этой вариации с остатками
        packages_with_stock = db.session.query(
            ProductPackage,
            StockPackaged
        ).join(
            StockPackaged, ProductPackage.id == StockPackaged.package_id
        ).filter(
            ProductPackage.variation_id == variation.id
        ).all()

        for package, package_stock in packages_with_stock:
            size_color_groups[key]['packages'].append({
                'package': package,
                'quantity': package_stock.quantity_packages
            })

    return render_template('products/detail.html',
                           product=product,
                           size_color_groups=list(size_color_groups.values()),
                           now=datetime.now())


@bp.route('/<int:product_id>/incoming', methods=['GET', 'POST'])
def product_incoming(product_id):
    """Приход товара - только в неупакованные"""
    product = Product.query.get_or_404(product_id)

    # Получаем все вариации с остатками неупакованного
    variations_with_stock = db.session.query(
        ProductVariation,
        StockUnpackaged
    ).join(
        StockUnpackaged, ProductVariation.id == StockUnpackaged.variation_id
    ).filter(
        ProductVariation.product_id == product_id
    ).all()

    if request.method == 'POST':
        try:
            for variation, stock in variations_with_stock:
                quantity_field = f'quantity_{variation.id}'
                quantity = request.form.get(quantity_field, '0').strip()

                if quantity and int(quantity) > 0:
                    quantity = int(quantity)
                    stock.quantity_pieces += quantity

            db.session.commit()
            flash('Приход успешно добавлен!', 'success')
            return redirect(url_for('products.product_detail', product_id=product_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении прихода: {str(e)}', 'danger')

    return render_template('products/incoming.html',
                           product=product,
                           variations_with_stock=variations_with_stock,
                           now=datetime.now())  # Добавляем now


@bp.route('/<int:product_id>/packing', methods=['GET', 'POST'])
def product_packing(product_id):
    """Упаковка товара"""
    product = Product.query.get_or_404(product_id)

    # Находим вариации с ненулевыми остатками неупакованного товара
    variations_with_stock = db.session.query(
        ProductVariation,
        StockUnpackaged
    ).join(
        StockUnpackaged, ProductVariation.id == StockUnpackaged.variation_id
    ).filter(
        ProductVariation.product_id == product_id,
        StockUnpackaged.quantity_pieces > 0
    ).all()

    packing_data = []
    for variation, stock in variations_with_stock:
        packages = ProductPackage.query.filter_by(variation_id=variation.id).all()
        if packages:
            packing_data.append({
                'variation': variation,
                'packages': packages,
                'remaining_quantity': stock.quantity_pieces
            })

    if request.method == 'POST':
        try:
            # Собираем данные из формы
            operations = []
            for item in packing_data:
                for package in item['packages']:
                    quantity_field = f'quantity_{item["variation"].id}_{package.id}'
                    quantity = request.form.get(quantity_field, '0').strip()

                    if quantity and int(quantity) > 0:
                        operations.append({
                            'variation': item['variation'],
                            'package': package,
                            'quantity': int(quantity)
                        })

            # Проверяем достаточно ли товара
            for op in operations:
                stock_unpackaged = StockUnpackaged.query.filter_by(
                    variation_id=op['variation'].id
                ).first()
                units_needed = op['quantity'] * op['package'].package_quantity

                if stock_unpackaged.quantity_pieces < units_needed:
                    flash(
                        f'Недостаточно товара для упаковки {op["package"].sku}. '
                        f'Доступно: {stock_unpackaged.quantity_pieces} шт., требуется: {units_needed} шт.',
                        'danger'
                    )
                    return redirect(url_for('products.product_packing', product_id=product_id))

            # Выполняем упаковку
            for op in operations:
                # Уменьшаем неупакованный остаток
                stock_unpackaged = StockUnpackaged.query.filter_by(
                    variation_id=op['variation'].id
                ).first()
                units_used = op['quantity'] * op['package'].package_quantity
                stock_unpackaged.quantity_pieces -= units_used

                # Увеличиваем упакованный остаток
                stock_packaged = StockPackaged.query.filter_by(
                    package_id=op['package'].id
                ).first()
                if stock_packaged:
                    stock_packaged.quantity_packages += op['quantity']
                else:
                    # Создаем запись если ее нет
                    stock_packaged = StockPackaged(
                        package_id=op['package'].id,
                        quantity_packages=op['quantity']
                    )
                    db.session.add(stock_packaged)

            db.session.commit()
            flash('Товар успешно упакован!', 'success')
            return redirect(url_for('products.product_detail', product_id=product_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при упаковке: {str(e)}', 'danger')

    return render_template('products/packing.html',
                           product=product,
                           packing_data=packing_data,
                           now=datetime.now())  # Добавляем now


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


@bp.route('/get_category_attributes/<int:category_id>')
def get_category_attributes(category_id):
    """Получение размеров, цветов и вариантов упаковки категории"""
    category = ProductCategory.query.get_or_404(category_id)

    sizes = [{'id': size.id, 'name': size.name, 'description': size.description}
             for size in category.sizes]

    colors = [{'id': color.id, 'name': color.name, 'hex_code': color.hex_code}
              for color in category.colors]

    # Добавляем варианты упаковки
    packaging_options = []
    for packaging in category.packaging_options:
        packaging_options.append({
            'size_id': packaging.size_id,
            'size_name': packaging.size.name,
            'color_id': packaging.color_id,
            'color_name': packaging.color.name,
            'package_quantity': packaging.package_quantity
        })

    return jsonify({
        'sizes': sizes,
        'colors': colors,
        'packaging_options': packaging_options
    })

## app/controllers/products.py - новый метод add_product_v2
@bp.route('/add_v2', methods=['GET', 'POST'])
def add_product_v2():
    """Новая версия добавления товара с тремя блоками чекпоинтов"""
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

            # 1. Создаем НЕУПАКОВАННЫЕ вариации (все комбинации размер-цвет)
            selected_size_ids = request.form.getlist('size_ids[]')
            selected_color_ids = request.form.getlist('color_ids[]')

            for size_id in selected_size_ids:
                for color_id in selected_color_ids:
                    if size_id and color_id:
                        variation = ProductVariation(
                            product_id=product.id,
                            size_id=int(size_id),
                            color_id=int(color_id)
                        )
                        db.session.add(variation)
                        db.session.flush()

                        stock_unpackaged = StockUnpackaged(
                            variation_id=variation.id,
                            quantity_pieces=0
                        )
                        db.session.add(stock_unpackaged)

            # 2. Создаем УПАКОВАННЫЕ вариации из автоматически сгенерированных
            package_size_ids = request.form.getlist('package_size_ids[]')
            package_color_ids = request.form.getlist('package_color_ids[]')
            package_quantities = request.form.getlist('package_quantities[]')
            skus = request.form.getlist('skus[]')

            for i, (size_id, color_id, package_qty, sku) in enumerate(zip(
                    package_size_ids, package_color_ids, package_quantities, skus)):

                if not sku.strip():
                    continue

                # Находим соответствующую вариацию
                variation = ProductVariation.query.filter_by(
                    product_id=product.id,
                    size_id=int(size_id),
                    color_id=int(color_id)
                ).first()

                if variation:
                    package = ProductPackage(
                        variation_id=variation.id,
                        package_quantity=int(package_qty),
                        sku=sku.strip()
                    )
                    db.session.add(package)
                    db.session.flush()

                    stock_packaged = StockPackaged(
                        package_id=package.id,
                        quantity_packages=0
                    )
                    db.session.add(stock_packaged)

            db.session.commit()
            flash('Товар успешно добавлен!', 'success')
            return redirect(url_for('products.products_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении товара: {str(e)}', 'danger')

    return render_template('products/add_v2.html',
                           categories=categories,
                           now=datetime.now())