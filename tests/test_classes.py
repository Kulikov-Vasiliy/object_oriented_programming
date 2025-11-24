import unittest
from io import StringIO
from unittest.mock import patch

from src.classes import Category, LawnGrass, Product, Smartphone


class TestProduct(unittest.TestCase):
    def setUp(self):
        # Инициализация тестовых данных перед каждым тестом
        self.product1 = Product("Laptop", "Powerful laptop", 1200.0, 10)
        self.product2 = Product("Mouse", "Wireless mouse", 25.5, 50)
        self.smartphone = Smartphone("iPhone 13", "Latest iPhone", 999.0, 15, 10, "13", 128, "Blue")
        self.lawn_grass = LawnGrass("Green Mix", "Universal grass", 10.0, 100, "USA", "1 week", "Green")

    def test_product_str(self):
        # Проверка метода __str__
        self.assertEqual(str(self.product1), "Laptop 1200.0 руб. Остаток: 10 шт.")

    def test_product_add(self):
        # Проверка метода __add__ для Product (должен работать только для объектов Product)
        total_value = (1200.0 * 10) + (25.5 * 50)
        self.assertEqual(self.product1 + self.product2, total_value)

    def test_price_property_and_setter(self):
        # Проверка свойства price (getter)
        self.assertEqual(self.product1.price, 1200.0)

        # Проверка сеттера цены с имитацией ввода пользователя (yes/no)
        # Имитируем ввод "yes" для подтверждения новой цены
        with patch("sys.stdin", StringIO("yes\n")):
            self.product1.price = 1300.0
            self.assertEqual(self.product1.price, 1300.0)

            # Имитируем ввод "no" для отмены изменения цены
            with patch("sys.stdin", StringIO("no\n")):
                self.product1.price = 1400.0
                self.assertEqual(self.product1.price, 1300.0)  # Цена не должна измениться

            # Имитируем ввод некорректной/отрицательной цены
            with patch("sys.stdin", StringIO("yes\n")):
                # Вывод ошибки в консоль при отрицательной цене, цена не меняется
                self.product1.price = -100.0
                self.assertEqual(self.product1.price, 1300.0)

    def test_new_product_classmethod(self):
        # Проверка метода new_product (classmethod)
        product_list = [self.product1]
        new_product_info = {"name": "Laptop", "description": "Powerful laptop", "price": 1250.0, "quantity": 5}

        # Добавление существующего продукта (обновление количества и цены)
        with patch("sys.stdin", StringIO("yes\n")):
            updated_product = Product.new_product(new_product_info, product_list)
            self.assertEqual(updated_product.quantity, 15)
            self.assertEqual(updated_product.price, 1250.0)  # Цена должна обновиться, т.к. 1250 > 1200

        # Добавление нового продукта
        new_product_info_2 = {"name": "Monitor", "description": "4K monitor", "price": 400.0, "quantity": 2}
        newly_created_product = Product.new_product(new_product_info_2, product_list)
        self.assertEqual(len(product_list), 2)
        self.assertEqual(newly_created_product.name, "Monitor")


class TestSubclasses(unittest.TestCase):
    def setUp(self):
        self.smartphone1 = Smartphone("iPhone 13", "Latest iPhone", 999.0, 15, 10, "13", 128, "Blue")
        self.smartphone2 = Smartphone("Samsung S21", "Android phone", 800.0, 20, 9, "S21", 256, "Black")
        self.lawn_grass1 = LawnGrass("Green Mix", "Universal grass", 10.0, 100, "USA", "1 week", "Green")

    def test_smartphone_add(self):
        # Проверка __add__ для смартфонов
        expected_value = (999.0 * 15) + (800.0 * 20)
        self.assertEqual(self.smartphone1 + self.smartphone2, expected_value)

    def test_lawn_grass_add(self):
        # Проверка __add__ для газонов
        expected_value = (10.0 * 100) + (10.0 * 100)  # Assuming lawn_grass1 + lawn_grass1
        self.assertEqual(self.lawn_grass1 + self.lawn_grass1, expected_value)

    def test_subclass_add_type_error(self):
        # Проверка, что сложение разных подклассов вызывает TypeError
        with self.assertRaises(TypeError):
            self.smartphone1 + self.lawn_grass1


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.product1 = Product("Laptop", "Powerful laptop", 1200.0, 10)
        self.product2 = Product("Mouse", "Wireless mouse", 25.5, 50)
        self.category = Category("Electronics", "Gadgets", [self.product1])

    def test_category_init(self):
        # Проверка инициализации категории и счетчиков
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.product_count, 1)

    def test_add_product(self):
        # Проверка добавления продукта (только Product или подклассы)
        # Этот код в функции add_product принимает только Smartphone или LawnGrass,
        # что противоречит типу product1 (Product).
        # Если ваш код должен принимать базовый класс Product, логику надо поправить.
        # Исходя из текущего кода, этот тест должен вызывать ошибку:
        with self.assertRaises(TypeError):
            self.category.add_product(self.product2)

        # Пример добавления корректного подкласса
        smartphone = Smartphone("iPhone 13", "Latest iPhone", 999.0, 15, 10, "13", 128, "Blue")
        self.category.add_product(smartphone)
        self.assertEqual(self.category.product_count, 2)

    def test_category_products_property(self):
        # Проверка проперти products (геттер форматированной строки)
        expected_str = "Laptop 1200.0 руб. Остаток: 10 шт."
        self.assertEqual(self.category.products, expected_str)

    def test_category_str(self):
        # Проверка метода __str__ категории
        self.assertEqual(str(self.category), "Electronics количество продуктов: 1 шт.")


class TestMixinLog(unittest.TestCase):
    def test_mixin_log_repr(self):
        # Проверка работы миксина __repr__
        # Хотя MixinLog имеет свой __init__ и __repr__, Product его переопределяет.
        # Product использует super().__init__(), который вызывает MixinLog.__init__
        # в порядке MRO, но Product.__init__ не вызывает MixinLog.__init__ с параметрами
        # name, description, price, quantity, как предполагалось в MixinLog.
        # Текущая реализация MixinLog не будет работать должным образом с Product.
        # Product переопределяет __repr__ в любом случае.

        # Проверим __repr__ класса Product, который включает логирование
        product = Product("TestItem", "Description", 100.0, 5)
        # Ожидаемый вывод от Product.__repr__
        expected_repr = "Product(('TestItem', 'Description', 100.0, 5))"
        self.assertEqual(repr(product), expected_repr)
