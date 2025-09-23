# app/controllers/categories.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.category import ProductCategory
from app.models import Product  # Добавляем импорт Product

bp = Blueprint('categories', __name__)

@bp.route('/')
def categories_list():
    """Список всех категорий"""
    categories = ProductCategory.query.order_by(ProductCategory.name).all()
    return render_template('categories/list.html', categories=categories)

@bp.route('/add', methods=['GET', 'POST'])
def add_category():
    """Добавление новой категории"""
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            description = request.form.get('description', '').strip()

            # Проверяем, существует ли категория
            existing_category = ProductCategory.query.filter_by(name=name).first()
            if existing_category:
                flash('Категория с таким названием уже существует', 'warning')
                return redirect(url_for('categories.add_category'))

            category = ProductCategory(
                name=name,
                description=description or None
            )

            db.session.add(category)
            db.session.commit()

            flash('Категория успешно добавлена!', 'success')
            return redirect(url_for('categories.categories_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении категории: {str(e)}', 'danger')

    return render_template('categories/add.html')

@bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    """Редактирование категории"""
    category = ProductCategory.query.get_or_404(category_id)

    if request.method == 'POST':
        try:
            category.name = request.form['name'].strip()
            category.description = request.form.get('description', '').strip() or None

            db.session.commit()
            flash('Категория успешно обновлена!', 'success')
            return redirect(url_for('categories.categories_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении категории: {str(e)}', 'danger')

    return render_template('categories/edit.html', category=category)

@bp.route('/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """Удаление категории"""
    category = ProductCategory.query.get_or_404(category_id)

    try:
        # Проверяем, есть ли товары в этой категории
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