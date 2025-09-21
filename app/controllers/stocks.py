from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import OurWarehouseStock, StockMovement, ProductVariation, Product

bp = Blueprint('stocks', __name__)


@bp.route('/')
def stocks_overview():
    """Обзор остатков на складах"""
    variations_with_stock = db.session.query(
        ProductVariation,
        OurWarehouseStock,
        Product
    ).join(
        OurWarehouseStock, OurWarehouseStock.variation_id == ProductVariation.id
    ).join(
        Product, Product.id == ProductVariation.product_id
    ).order_by(ProductVariation.sku).all()

    return render_template('stocks/overview.html', variations_with_stock=variations_with_stock)


@bp.route('/incoming/select-product')
def incoming_select_product():
    """Выбор товара для прихода"""
    products = Product.query.order_by(Product.name).all()
    return render_template('stocks/incoming_select_product.html', products=products)


@bp.route('/incoming/add/<int:product_id>', methods=['GET', 'POST'])
def incoming_add(product_id):
    """Добавление прихода товара"""
    product = Product.query.get_or_404(product_id)
    positions = ProductVariation.query.filter_by(product_id=product_id).all()

    if request.method == 'POST':
        try:
            for position in positions:
                quantity_field = f'quantity_{position.id}'
                quantity = request.form.get(quantity_field, '0').strip()

                if quantity and int(quantity) > 0:
                    quantity = int(quantity)

                    stock = position.get_stock()
                    if not stock:
                        stock = OurWarehouseStock(variation_id=position.id)
                        db.session.add(stock)

                    # Добавляем в неупакованные (штуки)
                    stock.unpacked_quantity += quantity

                    movement = StockMovement(
                        variation_id=position.id,
                        movement_type='incoming',
                        quantity=quantity,
                        comment=f'Приход товара: {product.name}'
                    )
                    db.session.add(movement)

            db.session.commit()
            flash('Приход успешно добавлен!', 'success')
            return redirect(url_for('stocks.stocks_overview'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении прихода: {str(e)}', 'danger')

    return render_template('stocks/incoming_add.html', product=product, positions=positions)


@bp.route('/packing/select-product')
def packing_select_product():
    """Выбор товара для упаковки"""
    products = Product.query.order_by(Product.name).all()
    return render_template('stocks/packing_select_product.html', products=products)


@bp.route('/packing/add/<int:product_id>', methods=['GET', 'POST'])
def packing_add(product_id):
    """Упаковка товара"""
    product = Product.query.get_or_404(product_id)
    positions = ProductVariation.query.filter_by(product_id=product_id).all()

    positions_with_stock = []
    for position in positions:
        stock = position.get_stock()
        if stock and stock.unpacked_quantity > 0:
            positions_with_stock.append({
                'position': position,
                'stock': stock
            })

    if request.method == 'POST':
        try:
            for item in positions_with_stock:
                position = item['position']
                stock = item['stock']

                quantity_field = f'quantity_{position.id}'
                quantity = request.form.get(quantity_field, '0').strip()

                if quantity and int(quantity) > 0:
                    quantity_to_pack = int(quantity)  # Количество УПАКОВОК

                    # Рассчитываем сколько ШТУК нужно для упаковки
                    units_needed = quantity_to_pack * position.package_quantity

                    # Проверяем, достаточно ли неупакованного товара
                    if stock.unpacked_quantity < units_needed:
                        flash(
                            f'Недостаточно неупакованного товара для позиции {position.sku}. Нужно {units_needed} шт., доступно {stock.unpacked_quantity} шт.',
                            'danger')
                        return redirect(url_for('stocks.packing_add', product_id=product_id))

                    # Переводим из неупакованных в упакованные
                    stock.unpacked_quantity -= units_needed  # Вычитаем ШТУКИ
                    stock.packed_quantity += quantity_to_pack  # Добавляем УПАКОВКИ

                    movement = StockMovement(
                        variation_id=position.id,
                        movement_type='packing',
                        quantity=quantity_to_pack,
                        comment=f'Упаковка товара: {product.name} ({quantity_to_pack} уп. по {position.package_quantity} шт.)'
                    )
                    db.session.add(movement)

            db.session.commit()
            flash('Товар успешно упакован!', 'success')
            return redirect(url_for('stocks.stocks_overview'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при упаковке: {str(e)}', 'danger')

    return render_template('stocks/packing_add.html', product=product, positions_with_stock=positions_with_stock)