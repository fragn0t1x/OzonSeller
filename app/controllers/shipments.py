from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app import db
from app.models import Shipment, ShipmentItem, ProductPackage, StockPackaged, ProductVariation, Product, Size, Color
from datetime import datetime, timedelta

bp = Blueprint('shipments', __name__)


@bp.route('/')
def shipments_list():
    """Список всех отправок"""
    page = request.args.get('page', 1, type=int)

    # Упрощаем запрос
    shipments = Shipment.query.options(
        db.joinedload(Shipment.items).joinedload(ShipmentItem.package)
    ).order_by(Shipment.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False
    )

    return render_template('shipments/list.html',
                           shipments=shipments,
                           now=datetime.now())


@bp.route('/create', methods=['GET', 'POST'])
def create_shipment():
    """Создание новой отправки"""
    # Ищем упакованные товары с остатками > 0
    packages_with_stock = db.session.query(
        ProductPackage,
        StockPackaged
    ).join(
        StockPackaged, ProductPackage.id == StockPackaged.package_id
    ).filter(
        StockPackaged.quantity_packages > 0
    ).options(
        db.joinedload(ProductPackage.variation).joinedload(ProductVariation.product),
        db.joinedload(ProductPackage.variation).joinedload(ProductVariation.size),
        db.joinedload(ProductPackage.variation).joinedload(ProductVariation.color)
    ).all()

    if request.method == 'POST':
        try:
            # Создаем отправку
            shipment = Shipment(
                shipment_number=f"SH{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                status='preparing',
                expected_delivery_date=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(shipment)
            db.session.flush()

            # Добавляем товары в отправку
            package_ids = request.form.getlist('package_ids[]')
            quantities = request.form.getlist('quantities[]')

            added_items = 0

            for package_id, quantity in zip(package_ids, quantities):
                if not quantity or int(quantity) <= 0:
                    continue

                package = ProductPackage.query.get(int(package_id))
                stock = StockPackaged.query.filter_by(package_id=package.id).first()

                if stock and stock.quantity_packages >= int(quantity):
                    # Добавляем товар в отправку
                    item = ShipmentItem(
                        shipment_id=shipment.id,
                        package_id=package.id,
                        quantity=int(quantity)
                    )
                    db.session.add(item)

                    # Уменьшаем остатки упакованного товара
                    stock.quantity_packages -= int(quantity)
                    added_items += 1
                else:
                    available = stock.quantity_packages if stock else 0
                    flash(
                        f'Недостаточно товара для отправки {package.sku}. Доступно: {available} уп., запрошено: {quantity}',
                        'warning')

            if added_items == 0:
                flash('Не добавлено ни одного товара в отправку. Проверьте выбранные количества.', 'warning')
                db.session.rollback()
                return redirect(url_for('shipments.create_shipment'))

            db.session.commit()
            flash(f'Отправка {shipment.shipment_number} успешно создана! Добавлено {added_items} позиций.', 'success')
            return redirect(url_for('shipments.shipment_detail', shipment_id=shipment.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании отправки: {str(e)}', 'danger')

    return render_template('shipments/create.html',
                           packages=packages_with_stock,
                           now=datetime.now())


@bp.route('/<int:shipment_id>')
def shipment_detail(shipment_id):
    """Детальная информация об отправке"""
    # Упрощаем запрос - загружаем данные по отдельности
    shipment = Shipment.query.options(
        db.joinedload(Shipment.items).joinedload(ShipmentItem.package)
    ).get_or_404(shipment_id)

    # Догружаем дополнительные данные для каждого элемента
    for item in shipment.items:
        # Загружаем вариацию и связанные данные
        item.package.variation = ProductVariation.query.options(
            db.joinedload(ProductVariation.product),
            db.joinedload(ProductVariation.size),
            db.joinedload(ProductVariation.color)
        ).get(item.package.variation_id)

    return render_template('shipments/detail.html',
                           shipment=shipment,
                           now=datetime.now())


@bp.route('/<int:shipment_id>/confirm')
def confirm_shipment(shipment_id):
    """Подтверждение отправки"""
    shipment = Shipment.query.get_or_404(shipment_id)

    if shipment.status == 'preparing':
        shipment.status = 'sent'
        shipment.shipment_date = datetime.utcnow()
        db.session.commit()
        flash(f'Отправка {shipment.shipment_number} подтверждена!', 'success')
    else:
        flash('Невозможно подтвердить отправку с текущим статусом', 'warning')

    return redirect(url_for('shipments.shipment_detail', shipment_id=shipment_id))


@bp.route('/<int:shipment_id>/cancel')
def cancel_shipment(shipment_id):
    """Отмена отправки и возврат товара на склад"""
    shipment = Shipment.query.options(
        db.joinedload(Shipment.items).joinedload(ShipmentItem.package)
    ).get_or_404(shipment_id)

    if shipment.status == 'preparing':
        try:
            # Возвращаем товар на склад
            for item in shipment.items:
                stock = StockPackaged.query.filter_by(package_id=item.package_id).first()
                if stock:
                    stock.quantity_packages += item.quantity
                else:
                    # Создаем запись остатка если ее нет
                    stock = StockPackaged(
                        package_id=item.package_id,
                        quantity_packages=item.quantity
                    )
                    db.session.add(stock)

            # Удаляем отправку
            db.session.delete(shipment)
            db.session.commit()

            flash('Отправка отменена, товар возвращен на склад.', 'success')
            return redirect(url_for('shipments.shipments_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при отмене отправки: {str(e)}', 'danger')
    else:
        flash('Можно отменять только отправки в статусе "preparing"', 'warning')

    return redirect(url_for('shipments.shipment_detail', shipment_id=shipment_id))


@bp.route('/<int:shipment_id>/deliver')
def deliver_shipment(shipment_id):
    """Отметка доставки отправки"""
    shipment = Shipment.query.get_or_404(shipment_id)

    if shipment.status == 'sent':
        shipment.status = 'delivered'
        db.session.commit()
        flash(f'Отправка {shipment.shipment_number} отмечена как доставленная!', 'success')
    else:
        flash('Можно отмечать как доставленные только отправки в статусе "sent"', 'warning')

    return redirect(url_for('shipments.shipment_detail', shipment_id=shipment_id))