import pytest
from src.classes import Product, Category


def test_product_init():
    """Тест корректности инициализации объекта Product."""
    product = Product(name="Молоко", description="Коровье", price=100.0, quantity=50)

    assert product.name == "Молоко"
    assert product.description == "Коровье"
    assert product.price == 100.0
    assert product.quantity == 50

def test_product_attributes_types():
    """Тест типов атрибутов объекта Product."""
    product = Product(name="Хлеб", description="Ржаной", price=50.5, quantity=100)

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


# Фикстура для создания тестовых продуктов, чтобы не повторять код
@pytest.fixture
def products_list():
    return [
        Product(name="Молоко", description="Коровье", price=100.0, quantity=50),
        Product(name="Хлеб", description="Ржаной", price=50.5, quantity=100),
    ]


def test_category_init(products_list):
    """Тест корректности инициализации объекта Category."""
    category = Category(name="Продукты", description="Продукты питания", products=products_list)

    assert category.name == "Продукты"
    assert category.description == "Продукты питания"
    assert category.products == products_list
    assert category.product_count == 2


def test_category_class_attribute_count():
    """Тест атрибута класса category_count."""
    # Сбрасываем счетчик перед тестом, если он был изменен другими тестами
    Category.category_count = 0

    Category(name="Продукты", description="", products=[])
    assert Category.category_count == 1

    Category(name="Электроника", description="", products=[])
    assert Category.category_count == 2


def test_product_added_to_category_with_matching_name(products_list):
    """Тест добавления продукта в категорию с совпадающим именем."""
    category = Category(name="Продукты", description="", products=products_list)
    new_product = Product(name="Сыр", description="Голландский", price=300.0, quantity=20)

    initial_product_count = len(category.products)
    category.product_added(name="Продукты", product=new_product)

    assert len(category.products) == initial_product_count + 1
    assert new_product in category.products


def test_product_added_to_category_with_different_name(products_list):
    """Тест добавления продукта в категорию с несовпадающим именем.
    В текущей реализации продукт все равно добавляется."""
    category = Category(name="Продукты", description="", products=products_list)
    new_product = Product(name="Сыр", description="Голландский", price=300.0, quantity=20)

    initial_product_count = len(category.products)
    category.product_added(name="Несуществующая категория", product=new_product)

    assert len(category.products) == initial_product_count + 1
    assert new_product in category.products


def test_product_ended_from_category_if_name_does_not_match(products_list):
    """Тест удаления продукта, когда имя категории не совпадает.
    В текущей реализации продукт все равно удаляется, если существует."""
    category = Category(name="Продукты", description="", products=products_list.copy())
    product_to_remove = products_list[0]

    initial_product_count = len(category.products)
    category.product_ended(name="Неверное имя", product=product_to_remove)

    assert len(category.products) == initial_product_count - 1
    assert product_to_remove not in category.products


def test_product_ended_from_category(products_list):
    """Тест удаления существующего продукта из категории."""
    category = Category(name="Продукты", description="", products=products_list.copy())
    product_to_remove = products_list[0]

    initial_product_count = len(category.products)
    category.product_ended(name="Продукты", product=product_to_remove)

    assert len(category.products) == initial_product_count - 1
    assert product_to_remove not in category.products


def test_product_ended_not_in_category(products_list):
    """Тест попытки удаления продукта, которого нет в категории."""
    category = Category(name="Продукты", description="", products=products_list.copy())
    non_existent_product = Product(name="Несуществующий", description="", price=0, quantity=0)

    initial_product_count = len(category.products)
    category.product_ended(name="Продукты", product=non_existent_product)

    assert len(category.products) == initial_product_count
