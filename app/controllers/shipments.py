from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app import db
from app.models import Shipment, ShipmentItem, ProductVariation, OurWarehouseStock
from datetime import datetime, timedelta

bp = Blueprint('shipments', __name__)

@bp.route('/')
def shipments_list():
    """Список всех отправок"""
    page = request.args.get('page', 1, type=int)
    shipments = Shipment.query.order_by(Shipment.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False
    )
    return render_template('shipments/list.html', shipments=shipments)

@bp.route('/create', methods=['GET', 'POST'])
def create_shipment():
    """Создание новой отправки"""
    # Убрали warehouses так как OzonWarehouse удален
    variations = db.session.query(ProductVariation).join(
        OurWarehouseStock,
        OurWarehouseStock.variation_id == ProductVariation.id
    ).filter(
        OurWarehouseStock.packed_quantity > 0
    ).options(
        db.joinedload(ProductVariation.our_stock),
        db.joinedload(ProductVariation.product)
    ).all()

    if request.method == 'POST':
        try:
            # Создаем отправку (убрали destination_warehouse_id)
            shipment = Shipment(
                shipment_number=f"SH{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                status='preparing',
                expected_delivery_date=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(shipment)
            db.session.flush()

            # Добавляем товары в отправку
            variation_ids = request.form.getlist('variation_ids[]')
            quantities = request.form.getlist('quantities[]')

            for variation_id, quantity in zip(variation_ids, quantities):
                if not quantity or int(quantity) <= 0:
                    continue

                variation = ProductVariation.query.get(int(variation_id))
                stock = variation.get_stock()
                if variation and stock and stock.packed_quantity >= int(quantity):
                    # Добавляем товар в отправку
                    item = ShipmentItem(
                        shipment_id=shipment.id,
                        variation_id=variation.id,
                        quantity=int(quantity)
                    )
                    db.session.add(item)

                    # Уменьшаем остатки упакованного товара
                    stock.packed_quantity -= int(quantity)
                else:
                    flash(f'Недостаточно товара для вариации {variation.sku}', 'warning')

            db.session.commit()
            flash('Отправка успешно создана!', 'success')
            return redirect(url_for('shipments.shipment_detail', shipment_id=shipment.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании отправки: {str(e)}', 'danger')

    return render_template('shipments/create.html', variations=variations)

@bp.route('/<int:shipment_id>')
def shipment_detail(shipment_id):
    """Детальная информация об отправке"""
    shipment = Shipment.query.get_or_404(shipment_id)
    return render_template('shipments/detail.html', shipment=shipment)

@bp.route('/<int:shipment_id>/confirm')
def confirm_shipment(shipment_id):
    """Подтверждение отправки"""
    shipment = Shipment.query.get_or_404(shipment_id)

    if shipment.status == 'preparing':
        shipment.status = 'sent'
        shipment.shipment_date = datetime.utcnow()
        db.session.commit()
        flash('Отправка подтверждена!', 'success')
    else:
        flash('Невозможно подтвердить отправку с текущим статусом', 'warning')

    return redirect(url_for('shipments.shipment_detail', shipment_id=shipment_id))