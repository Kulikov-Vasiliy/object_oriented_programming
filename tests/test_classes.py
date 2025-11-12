import pytest

from src.classes import Category, Product


# Фикстура для имитации ввода пользователя
@pytest.fixture
def mock_input(monkeypatch):  # type: ignore[no-untyped-def]
    """Фикстура для имитации пользовательского ввода через input()"""

    def _mock_input_factory(responses):  # type: ignore[no-untyped-def]
        # Преобразуем список ответов в имитированный поток ввода
        input_gen = (response + "\n" for response in responses)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(input_gen).strip())

    return _mock_input_factory


class TestProduct:

    def test_product_initialization(self):  # type: ignore[no-untyped-def]
        product = Product("Apple", "Fruit", 1.5, 100)
        assert product.name == "Apple"
        assert product.description == "Fruit"
        assert product.price == 1.5  # Проверяем геттер
        assert product.quantity == 100

    def test_product_str(self):  # type: ignore[no-untyped-def]
        product = Product("Milk", "Dairy", 2.0, 50)
        assert str(product) == "Milk 2.0 руб. Остаток: 50 шт."

    def test_price_setter_accept_new_price(self, mock_input, capsys):  # type: ignore[no-untyped-def]
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

    def test_price_setter_reject_new_price(self, mock_input):  # type: ignore[no-untyped-def]
        # Имитируем ввод "no" для отказа
        mock_input(["no"])
        product = Product("Cheese", "Dairy", 5.0, 10)

        # Пытаемся установить новую цену, но она должна остаться прежней
        product.price = 4.5

        assert product.price == 5.0  # Цена не изменилась

    def test_price_setter_invalid_price(self, mock_input, capsys):  # type: ignore[no-untyped-def]
        # Имитируем ввод "yes" для подтверждения, но цена невалидна
        mock_input(["yes"])
        product = Product("Eggs", "Groceries", 3.0, 30)

        product.price = 0
        captured = capsys.readouterr()

        # Проверяем, что появилось сообщение об ошибке, и цена не изменилась
        assert "Цена не должна быть нулевая или отрицательная\n" in captured.out
        assert product.price == 3.0

    @pytest.fixture
    def category_setup(self):  # type: ignore[no-untyped-def]
        """Фикстура, предоставляющая экземпляр категории и продукт"""
        category = Category("Electronics", "Devices")
        product = Product("Laptop", "Portable PC", 1000.0, 10)
        return category, product

    def test_add_product_matching_name(self, category_setup):  # type: ignore[no-untyped-def]
        """Тест на добавление продукта, когда имя категории совпадает"""
        category, product = category_setup

        initial_count = category.product_count
        initial_list_len = len(category._Category__products)

        # Вызываем метод с совпадающим именем
        category.add_product(name="Electronics", product=product)

        # Проверяем, что продукт был добавлен и счетчики обновились
        assert len(category._Category__products) == initial_list_len + 1
        assert category.product_count == initial_count + 1
        assert product in category._Category__products
        assert category._Category__products[-1] is product  # Проверяем, что это тот же объект

    def test_add_product_non_matching_name(self, category_setup):  # type: ignore[no-untyped-def]
        """Тест на добавление продукта, когда имя категории не совпадает"""
        category, product = category_setup

        initial_count = category.product_count
        initial_list_len = len(category._Category__products)

        # Вызываем метод с НЕсовпадающим именем
        # Логика вашего кода позволяет добавлять товар, даже если имя не совпадает.
        category.add_product(name="Food", product=product)

        # Проверяем, что продукт все равно был добавлен и счетчики обновились
        assert len(category._Category__products) == initial_list_len + 1
        assert category.product_count == initial_count + 1
        assert product in category._Category__products

    def test_add_product_none_product(self, category_setup):  # type: ignore[no-untyped-def]
        """Тест на вызов метода с product=None (ничего не должно произойти)"""
        category, _ = category_setup

        initial_count = category.product_count
        initial_list_len = len(category._Category__products)

        # Вызываем метод без продукта
        category.add_product(name="Electronics", product=None)

        # Проверяем, что состояние объекта не изменилось
        assert len(category._Category__products) == initial_list_len
        assert category.product_count == initial_count

    def test_product_addition(self):  # type: ignore[no-untyped-def]
        """Тестирование сложения двух продуктов для получения общей стоимости"""
        product1 = Product("Laptop", "Electronics", 1000.0, 2)  # Общая стоимость: 2000.0
        product2 = Product("Mouse", "Accessory", 20.0, 5)  # Общая стоимость: 100.0

        total_value = product1 + product2

        # Ожидаемый результат: 2000.0 + 100.0 = 2100.0
        assert total_value == 2100.0

    def test_product_addition_zero_quantity(self):  # type: ignore[no-untyped-def]
        """Тестирование сложения с продуктом, количество которого равно нулю"""
        product1 = Product("Monitor", "Electronics", 300.0, 1)  # Общая стоимость: 300.0
        product2 = Product("Cable", "Accessory", 5.0, 0)  # Общая стоимость: 0.0

        total_value = product1 + product2

        assert total_value == 300.0

    def test_product_addition_single_item(self):  # type: ignore[no-untyped-def]
        """Тестирование сложения продуктов, каждого по одной штуке"""
        product1 = Product("Keyboard", "Accessory", 50.0, 1)
        product2 = Product("Pad", "Accessory", 10.0, 1)

        total_value = product1 + product2

        assert total_value == 60.0


class TestCategory:

    def test_category_initialization_and_counters(self):  # type: ignore[no-untyped-def]
        # Сбросим счетчик перед тестом, если нужно, или просто проверим инкремент
        initial_count = Category.category_count
        product1 = Product("Phone", "Mobile", 500.0, 10)
        category = Category("Electronics", "Devices", products=[product1])

        assert category.name == "Electronics"
        assert category.product_count == 1
        assert Category.category_count == initial_count + 1

    def test_category_products_property(self):  # type: ignore[no-untyped-def]
        p1 = Product("Pen", "Writing", 0.5, 200)
        p2 = Product("Paper", "Office", 2.0, 50)
        category = Category("Office Supplies", "Work essentials", products=[p1, p2])

        expected_output = "Pen 0.5 руб. Остаток: 200 шт.\n" "Paper 2.0 руб. Остаток: 50 шт."
        assert category.products == expected_output

    def test_category_product_list_method(self, mock_input):  # type: ignore[no-untyped-def]
        # product_list вызывает Product.new_product, который вызывает price.setter
        mock_input(["yes"])

        category = Category("Books", "Reading materials")
        product_info = {"name": "Python Basics", "description": "Guide", "price": 30.0, "quantity": 15}

        new_prod = category.product_list(product_info)

        assert new_prod.name == "Python Basics"
        # Проверяем, что продукт был добавлен во внутренний список категории
        assert len(category._Category__products) == 1
        assert category._Category__products[0] is new_prod

    def test_add_product_method(self):  # type: ignore[no-untyped-def]
        category = Category("Toys", "Fun stuff")
        new_toy = Product("Lego", "Bricks", 50.0, 10)

        # Метод add_product имеет избыточные проверки name == name, но мы его тестируем как есть
        category.add_product(name="Toys", product=new_toy)

        assert len(category._Category__products) == 1
        assert category._Category__products[0].name == "Lego"

    def test_product_ended_method(self):  # type: ignore[no-untyped-def]
        p1 = Product("T-shirt", "Clothing", 15.0, 50)
        category = Category("Apparel", "Wearables", products=[p1])

        assert len(category._Category__products) == 1

        # Метод product_ended тоже имеет избыточные проверки
        category.product_ended(name="Apparel", product=p1)

        assert len(category._Category__products) == 0

    def test_category_str_empty(self):  # type: ignore[no-untyped-def]
        """Тестирование строкового представления пустой категории"""
        category = Category("Groceries", "Everyday items")

        # Ожидаемый формат: "{self.name} количество продуктов: {self.product_count} шт."
        expected_str = "Groceries количество продуктов: 0 шт."
        assert str(category) == expected_str

    def test_category_str_with_products(self):  # type: ignore[no-untyped-def]
        """Тестирование строкового представления категории с несколькими продуктами"""
        p1 = Product("Apple", "Fruit", 1.0, 10)
        p2 = Product("Milk", "Dairy", 2.0, 5)

        # При инициализации product_count будет 2
        category = Category("Food", "Edibles", products=[p1, p2])

        expected_str = "Food количество продуктов: 2 шт."
        assert str(category) == expected_str

    def test_category_str_after_adding_product(self):  # type: ignore[no-untyped-def]
        """Тестирование обновления строкового представления после добавления продукта"""
        category = Category("Books", "Reading materials")
        product = Product("Novel", "Fiction", 25.0, 1)

        # Используем метод add_product для изменения состояния
        category.add_product(name="Books", product=product)

        expected_str = "Books количество продуктов: 1 шт."
        assert str(category) == expected_str
