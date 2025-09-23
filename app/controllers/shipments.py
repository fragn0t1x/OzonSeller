# app/controllers/shipments.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app import db
from app.models import Shipment, ShipmentItem, ProductPackage  # Убираем OurWarehouseStock и ProductVariation
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
    # Ищем упакованные товары (packages с quantity > 0)
    packages = ProductPackage.query.filter(
        ProductPackage.quantity > 0
    ).options(
        db.joinedload(ProductPackage.product)
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

            for package_id, quantity in zip(package_ids, quantities):
                if not quantity or int(quantity) <= 0:
                    continue

                package = ProductPackage.query.get(int(package_id))
                if package and package.quantity >= int(quantity):
                    # Добавляем товар в отправку
                    item = ShipmentItem(
                        shipment_id=shipment.id,
                        package_id=package.id,  # Используем package.id
                        quantity=int(quantity)
                    )
                    db.session.add(item)

                    # Уменьшаем остатки упакованного товара
                    package.quantity -= int(quantity)
                else:
                    flash(f'Недостаточно товара для упаковки {package.sku}', 'warning')

            db.session.commit()
            flash('Отправка успешно создана!', 'success')
            return redirect(url_for('shipments.shipment_detail', shipment_id=shipment.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании отправки: {str(e)}', 'danger')

    return render_template('shipments/create.html', packages=packages)

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