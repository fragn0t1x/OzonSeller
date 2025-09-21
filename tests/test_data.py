"""
Тестовые данные для заполнения базы данных
"""

TEST_CATEGORIES = [
    {
        'category_id': 17034420,
        'category_name': 'Носки',
        'type_id': 970778135,
        'type_name': 'Носки',
        'disabled': False
    },
    {
        'category_id': 17034421,
        'category_name': 'Футболки',
        'type_id': 970778136,
        'type_name': 'Футболки',
        'disabled': False
    }
]

TEST_PRODUCTS = [
    {
        'name': 'Носки спортивные',
        'category_id': 1,
        'description': 'Качественные спортивные носки'
    },
    {
        'name': 'Футболка хлопковая',
        'category_id': 2,
        'description': 'Мужская футболка из 100% хлопка'
    }
]

TEST_VARIATIONS = [
    # Носки - разные размеры и упаковки
    {'product_id': 1, 'sku': 'NSK-001-36-5', 'size': '36-41', 'package_quantity': 5},
    {'product_id': 1, 'sku': 'NSK-001-41-5', 'size': '41-47', 'package_quantity': 5},
    {'product_id': 1, 'sku': 'NSK-001-36-10', 'size': '36-41', 'package_quantity': 10},

    # Футболки - разные размеры
    {'product_id': 2, 'sku': 'TSH-001-M', 'size': 'M', 'package_quantity': 1},
    {'product_id': 2, 'sku': 'TSH-001-L', 'size': 'L', 'package_quantity': 1},
    {'product_id': 2, 'sku': 'TSH-001-XL', 'size': 'XL', 'package_quantity': 1}
]