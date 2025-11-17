import unittest
from io import StringIO
from unittest.mock import patch
from src.classes import Category, Product, Smartphone, LawnGrass


class TestProduct(unittest.TestCase):

    def setUp(self):
        # Инициализация объекта Product для использования в тестах
        self.product = Product("TestName", "TestDescription", 100.0, 10)

    def test_init(self):
        # Проверка корректности инициализации атрибутов
        self.assertEqual(self.product.name, "TestName")
        self.assertEqual(self.product.description, "TestDescription")
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.quantity, 10)

    @patch('sys.stdin', new_callable=StringIO)
    def test_price_setter_yes_valid(self, mock_input):
        # Тест установки новой валидной цены с подтверждением 'yes'
        mock_input.write('yes\n')
        mock_input.seek(0)  # Сброс указателя чтения
        self.product.price = 150.0
        self.assertEqual(self.product.price, 150.0)

    @patch('sys.stdin', new_callable=StringIO)
    def test_price_setter_yes_invalid(self, mock_input):
        # Тест попытки установки невалидной цены с подтверждением 'yes'
        mock_input.write('yes\n')
        mock_input.seek(0)
        original_price = self.product.price
        self.product.price = -50.0
        # Цена не должна измениться, так как новая цена невалидна
        self.assertEqual(self.product.price, original_price)

    @patch('sys.stdin', new_callable=StringIO)
    def test_price_setter_no(self, mock_input):
        # Тест отказа от установки новой цены с 'no'
        mock_input.write('no\n')
        mock_input.seek(0)
        original_price = self.product.price
        self.product.price = 200.0
        # Цена не должна измениться
        self.assertEqual(self.product.price, original_price)

    def test_str(self):
        # Тест метода __str__
        expected_str = "TestName 100.0 руб. Остаток: 10 шт."
        self.assertEqual(str(self.product), expected_str)

    def test_add(self):
        # Тест метода __add__ для двух продуктов
        other_product = Product("OtherTestName", "OtherDescription", 50.0, 5)
        expected_total = (100.0 * 10) + (50.0 * 5)  # 1000 + 250
        self.assertEqual(self.product + other_product, expected_total)

    def test_new_product_create_new(self):
        # Тест new_product для создания нового продукта
        product_info = {"name": "NewProd", "description": "NewDesc", "price": 10.0, "quantity": 1}
        new_prod = Product.new_product(product_info)
        self.assertEqual(new_prod.name, "NewProd")

    def test_new_product_update_existing(self):
        # Тест new_product для обновления существующего продукта в списке
        product_list = [self.product]
        product_info = {"name": "TestName", "price": 120.0, "quantity": 5}
        updated_prod = Product.new_product(product_info, product_list)

        # Проверяем, что количество обновилось
        self.assertEqual(self.product.quantity, 15)  # 10 + 5
        # Проверяем, что цена обновилась (если новая цена выше)
        self.assertEqual(self.product.price, 120.0)  # 100 < 120


class TestCategory(unittest.TestCase):

    def setUp(self):
        # Инициализация объектов для тестов категории
        self.product1 = Product("Prod1", "Desc1", 10.0, 1)
        self.product2 = Product("Prod2", "Desc2", 20.0, 2)
        self.category = Category("TestCat", "CatDesc", [self.product1, self.product2])
        # Сбросим счетчик категорий, если нужно изолировать тесты
        Category.category_count = 1

    def test_init(self):
        # Проверка инициализации категории
        self.assertEqual(self.category.name, "TestCat")
        self.assertEqual(self.category.product_count, 2)
        self.assertEqual(Category.category_count, 1)  # Предполагая сброс в setUp

    def test_str(self):
        # Тест метода __str__
        expected_str = "TestCat количество продуктов: 2 шт."
        self.assertEqual(str(self.category), expected_str)

    def test_products_property(self):
        # Тест свойства products
        expected_products_str = (
            "Prod1 10.0 руб. Остаток: 1 шт.\n"
            "Prod2 20.0 руб. Остаток: 2 шт."
        )
        self.assertEqual(self.category.products, expected_products_str)

    def test_add_product_valid(self):
        # Тест добавления валидного продукта (используем подклассы для прохождения проверки типа)
        smartphone = Smartphone("Phone", "Cool", 500.0, 1, 10, "M1", 64, "Black")
        self.category.add_product(smartphone)
        self.assertEqual(self.category.product_count, 3)
        self.assertIn(smartphone, self.category._Category__products)  # Доступ к приватному атрибуту

    def test_add_product_invalid_type(self):
        # Тест добавления невалидного типа (обычный Product)
        product = Product("Invalid", "Prod", 1.0, 1)
        with self.assertRaises(TypeError):
            self.category.add_product(product)

class TestSubclasses(unittest.TestCase):

    def setUp(self):
        self.smartphone1 = Smartphone("SPhone1", "Desc1", 100.0, 1, 10, "M1", 64, "Black")
        self.smartphone2 = Smartphone("SPhone2", "Desc2", 200.0, 2, 20, "M2", 128, "White")
        self.grass1 = LawnGrass("Grass1", "Desc3", 50.0, 3, "USA", "2 weeks", "Green")

    def test_smartphone_init(self):
        self.assertEqual(self.smartphone1.model, "M1")
        self.assertEqual(self.smartphone1.price, 100.0)

    def test_grass_init(self):
        self.assertEqual(self.grass1.country, "USA")
        self.assertEqual(self.grass1.germination_period, "2 weeks")

    def test_smartphone_add_valid(self):
        # Сложение двух смартфонов
        expected_total = (100.0 * 1) + (200.0 * 2)  # 100 + 400 = 500
        self.assertEqual(self.smartphone1 + self.smartphone2, expected_total)

    def test_smartphone_add_invalid(self):
        # Попытка сложить смартфон и траву (должно вызвать TypeError)
        with self.assertRaises(TypeError):
            self.smartphone1 + self.grass1

    def test_grass_add_invalid(self):
        # Попытка сложить траву и смартфон (должно вызвать TypeError)
        with self.assertRaises(TypeError):
            self.grass1 + self.smartphone1
