import pytest
import sys
from io import StringIO
from src.classes import Category, Product


# Фикстура для имитации ввода пользователя
@pytest.fixture
def mock_input(monkeypatch):
    """Фикстура для имитации пользовательского ввода через input()"""
    def _mock_input_factory(responses):
        # Преобразуем список ответов в имитированный поток ввода
        input_gen = (response + '\n' for response in responses)
        monkeypatch.setattr('builtins.input', lambda prompt="": next(input_gen).strip())
    return _mock_input_factory


class TestProduct:

    def test_product_initialization(self):
        product = Product("Apple", "Fruit", 1.5, 100)
        assert product.name == "Apple"
        assert product.description == "Fruit"
        assert product.price == 1.5  # Проверяем геттер
        assert product.quantity == 100

    def test_product_str(self):
        product = Product("Milk", "Dairy", 2.0, 50)
        assert str(product) == "Milk, Dairy, 2.0 руб., 50 шт."

    def test_price_setter_accept_new_price(self, mock_input, capsys):
        # Имитируем ввод "yes" для подтверждения
        mock_input(["yes"])
        product = Product("Bread", "Bakery", 1.0, 20)

        # Устанавливаем новую цену
        product.price = 1.2

        # Проверяем вывод в консоль перед вводом "yes"
        captured = capsys.readouterr()
        assert "1.2\n" in captured.out

        # Проверяем, что цена была изменена
        assert product.price == 1.2

    def test_price_setter_reject_new_price(self, mock_input):
        # Имитируем ввод "no" для отказа
        mock_input(["no"])
        product = Product("Cheese", "Dairy", 5.0, 10)

        # Пытаемся установить новую цену, но она должна остаться прежней
        product.price = 4.5

        assert product.price == 5.0  # Цена не изменилась

    def test_price_setter_invalid_price(self, mock_input, capsys):
        # Имитируем ввод "yes" для подтверждения, но цена невалидна
        mock_input(["yes"])
        product = Product("Eggs", "Groceries", 3.0, 30)

        product.price = 0
        captured = capsys.readouterr()

        # Проверяем, что появилось сообщение об ошибке, и цена не изменилась
        assert "Цена не должна быть нулевая или отрицательная\n" in captured.out
        assert product.price == 3.0

    def test_new_product_add_quantity_and_update_price(self, mock_input):
        # Для метода new_product также требуется имитация input() внутри price.setter,
        # так как он может вызвать этот сеттер.
        mock_input(["yes"])

        existing_products = [Product("Laptop", "Electronics", 1000.0, 5)]
        new_info = {"name": "Laptop", "description": "Gaming Laptop", "price": 1100.0, "quantity": 2}

        new_prod = Product.new_product(new_info, existing_products)

        # Проверяем, что количество обновилось (5 + 2 = 7)
        assert existing_products[0].quantity == 7
        # Проверяем, что цена обновилась (1000 -> 1100)
        assert existing_products[0].price == 1100.0
        # Метод вернул обновленный существующий продукт
        assert new_prod is existing_products[0]

    def test_new_product_create_new(self):
        existing_products = [Product("Mouse", "Accessory", 20.0, 10)]
        new_info = {"name": "Keyboard", "description": "Accessory", "price": 40.0, "quantity": 5}

        new_prod = Product.new_product(new_info, existing_products)

        # Проверяем, что новый продукт добавлен в список
        assert len(existing_products) == 2
        assert new_prod.name == "Keyboard"
        assert existing_products[1] is new_prod


class TestCategory:

    def test_category_initialization_and_counters(self):
        # Сбросим счетчик перед тестом, если нужно, или просто проверим инкремент
        initial_count = Category.category_count
        product1 = Product("Phone", "Mobile", 500.0, 10)
        category = Category("Electronics", "Devices", products=[product1])

        assert category.name == "Electronics"
        assert category.product_count == 1
        assert Category.category_count == initial_count + 1

    def test_category_products_property(self):
        p1 = Product("Pen", "Writing", 0.5, 200)
        p2 = Product("Paper", "Office", 2.0, 50)
        category = Category("Office Supplies", "Work essentials", products=[p1, p2])

        expected_output = (
            "Pen, Writing, 0.5 руб., 200 шт.\n"
            "Paper, Office, 2.0 руб., 50 шт."
        )
        assert category.products == expected_output

    def test_category_product_list_method(self, mock_input):
        # product_list вызывает Product.new_product, который вызывает price.setter
        mock_input(["yes"])

        category = Category("Books", "Reading materials")
        product_info = {"name": "Python Basics", "description": "Guide", "price": 30.0, "quantity": 15}

        new_prod = category.product_list(product_info)

        assert new_prod.name == "Python Basics"
        # Проверяем, что продукт был добавлен во внутренний список категории
        assert len(category._Category__products) == 1
        assert category._Category__products[0] is new_prod

    def test_add_product_method(self):
        category = Category("Toys", "Fun stuff")
        new_toy = Product("Lego", "Bricks", 50.0, 10)

        # Метод add_product имеет избыточные проверки name == name, но мы его тестируем как есть
        category.add_product(name="Toys", product=new_toy)

        assert len(category._Category__products) == 1
        assert category._Category__products[0].name == "Lego"

    def test_product_ended_method(self):
        p1 = Product("T-shirt", "Clothing", 15.0, 50)
        category = Category("Apparel", "Wearables", products=[p1])

        assert len(category._Category__products) == 1

        # Метод product_ended тоже имеет избыточные проверки
        category.product_ended(name="Apparel", product=p1)

        assert len(category._Category__products) == 0