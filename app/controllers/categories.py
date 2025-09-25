# app/controllers/categories.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app import db
from app.models.category import ProductCategory, CategorySize, CategoryColor, CategoryPackageQuantity
from app.models import Product
from datetime import datetime

bp = Blueprint('categories', __name__)


@bp.route('/')
def categories_list():
    """Список всех категорий"""
    categories = ProductCategory.query.order_by(ProductCategory.name).all()
    return render_template('categories/list.html',
                           categories=categories,
                           now=datetime.now())


@bp.route('/add', methods=['GET', 'POST'])
def add_category():
    """Добавление новой категории с размерами, цветами и количествами в упаковке"""
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            description = request.form.get('description', '').strip()

            existing_category = ProductCategory.query.filter_by(name=name).first()
            if existing_category:
                flash('Категория с таким названием уже существует', 'warning')
                return redirect(url_for('categories.add_category'))

            category = ProductCategory(
                name=name,
                description=description or None
            )
            db.session.add(category)
            db.session.flush()

            # Добавляем размеры
            size_names = request.form.getlist('size_names[]')
            size_descriptions = request.form.getlist('size_descriptions[]')

            for i, size_name in enumerate(size_names):
                if size_name.strip():
                    size = CategorySize(
                        category_id=category.id,
                        name=size_name.strip(),
                        description=size_descriptions[i].strip() if i < len(size_descriptions) else None
                    )
                    db.session.add(size)

            # Добавляем цвета
            color_names = request.form.getlist('color_names[]')
            color_hexes = request.form.getlist('color_hexes[]')

            for i, color_name in enumerate(color_names):
                if color_name.strip():
                    color = CategoryColor(
                        category_id=category.id,
                        name=color_name.strip(),
                        hex_code=color_hexes[i].strip() if i < len(color_hexes) else '#6c757d'
                    )
                    db.session.add(color)

            # Добавляем количества в упаковке
            package_quantities = request.form.getlist('package_quantities[]')
            package_descriptions = request.form.getlist('package_descriptions[]')

            for i, quantity_str in enumerate(package_quantities):
                if quantity_str.strip():
                    quantity = int(quantity_str)
                    description = package_descriptions[i].strip() if i < len(package_descriptions) else None
                    package_qty = CategoryPackageQuantity(
                        category_id=category.id,
                        quantity=quantity,
                        description=description
                    )
                    db.session.add(package_qty)

            db.session.commit()
            flash('Категория успешно добавлена!', 'success')
            return redirect(url_for('categories.categories_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении категории: {str(e)}', 'danger')

    return render_template('categories/add.html', now=datetime.now())


@bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    """Редактирование категории"""
    category = ProductCategory.query.get_or_404(category_id)

    if request.method == 'POST':
        try:
            category.name = request.form['name'].strip()
            category.description = request.form.get('description', '').strip() or None

            # Обновляем размеры
            CategorySize.query.filter_by(category_id=category.id).delete()
            size_names = request.form.getlist('size_names[]')
            size_descriptions = request.form.getlist('size_descriptions[]')

            for i, size_name in enumerate(size_names):
                if size_name.strip():
                    size = CategorySize(
                        category_id=category.id,
                        name=size_name.strip(),
                        description=size_descriptions[i].strip() if i < len(size_descriptions) else None
                    )
                    db.session.add(size)

            # Обновляем цвета
            CategoryColor.query.filter_by(category_id=category.id).delete()
            color_names = request.form.getlist('color_names[]')
            color_hexes = request.form.getlist('color_hexes[]')

            for i, color_name in enumerate(color_names):
                if color_name.strip():
                    color = CategoryColor(
                        category_id=category.id,
                        name=color_name.strip(),
                        hex_code=color_hexes[i].strip() if i < len(color_hexes) else '#6c757d'
                    )
                    db.session.add(color)

            # Обновляем количества в упаковке
            CategoryPackageQuantity.query.filter_by(category_id=category.id).delete()
            package_quantities = request.form.getlist('package_quantities[]')
            package_descriptions = request.form.getlist('package_descriptions[]')

            for i, quantity_str in enumerate(package_quantities):
                if quantity_str.strip():
                    quantity = int(quantity_str)
                    description = package_descriptions[i].strip() if i < len(package_descriptions) else None
                    package_qty = CategoryPackageQuantity(
                        category_id=category.id,
                        quantity=quantity,
                        description=description
                    )
                    db.session.add(package_qty)

            db.session.commit()
            flash('Категория успешно обновлена!', 'success')
            return redirect(url_for('categories.categories_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении категории: {str(e)}', 'danger')

    return render_template('categories/edit.html',
                           category=category,
                           now=datetime.now())


@bp.route('/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """Удаление категории"""
    category = ProductCategory.query.get_or_404(category_id)

    try:
        products_count = Product.query.filter_by(category_id=category_id).count()
        if products_count > 0:
            flash('Нельзя удалить категорию, в которой есть товары', 'danger')
            return redirect(url_for('categories.categories_list'))

        db.session.delete(category)
        db.session.commit()
        flash('Категория успешно удалена!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении категории: {str(e)}', 'danger')

    return redirect(url_for('categories.categories_list'))


@bp.route('/<int:category_id>/attributes')
def get_category_attributes(category_id):
    """Получение всех атрибутов категории"""
    category = ProductCategory.query.get_or_404(category_id)

    sizes = [{'id': size.id, 'name': size.name, 'description': size.description}
             for size in category.sizes]

    colors = [{'id': color.id, 'name': color.name, 'hex_code': color.hex_code}
              for color in category.colors]

    package_quantities = [{'id': pq.id, 'quantity': pq.quantity, 'description': pq.description}
                          for pq in category.package_quantities]

    return jsonify({
        'sizes': sizes,
        'colors': colors,
        'package_quantities': package_quantities
    })