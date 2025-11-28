from unittest.mock import patch
import pytest

from src.classes import Category, LawnGrass, Product, Smartphone


def test_product_creation(sample_product):
    """Проверяет корректное создание объекта Product и его атрибуты."""
    assert sample_product.name == "Телевизор Samsung"
    assert sample_product.price == 50000.0
    assert sample_product.quantity == 10
    assert str(sample_product) == "Телевизор Samsung 50000.0 руб. Остаток: 10 шт."
    assert "Product" in repr(sample_product)


def test_product_validation():
    """Проверяет вызов ValueError при некорректных входных данных."""
    with pytest.raises(ValueError, match="Наименование товара не указано"):
        Product("", "Описание", 100.0, 10)
    with pytest.raises(ValueError, match="Описание отсутствует"):
        Product("Имя", "", 100.0, 10)
    with pytest.raises(ValueError, match="Цена должна быть больше нуля"):
        Product("Имя", "Описание", 0.0, 10)
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Имя", "Описание", 100.0, 0)


def test_product_price_setter_yes(sample_product):
    """Тестирует сеттер цены с вводом 'yes'."""
    # Используем patch.input для имитации пользовательского ввода "yes"
    with patch('builtins.input', return_value='yes'):
        sample_product.price = 60000.0
        assert sample_product.price == 60000.0


def test_product_price_setter_no(sample_product):
    """Тестирует сеттер цены с вводом 'no'."""
    original_price = sample_product.price
    # Используем patch.input для имитации пользовательского ввода "no"
    with patch('builtins.input', return_value='no'):
        sample_product.price = 70000.0
        assert sample_product.price == original_price


def test_product_price_setter_invalid_price(sample_product, capsys):
    """Тестирует сеттер цены с вводом недопустимой цены (<= 0)."""
    with patch('builtins.input', return_value='yes'):
        sample_product.price = -10.0
        # Проверяем, что цена не изменилась, и было выведено сообщение
        assert sample_product.price == 50000.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_addition(sample_product):
    """Тестирует сложение двух продуктов (по стоимости запасов)."""
    product2 = Product("Мыло", "Описание", 50.0, 100)
    # Ожидаемый результат: (50000.0 * 10) + (50.0 * 100) = 500000 + 5000 = 505000.0
    assert sample_product + product2 == 505000.0


def test_smartphone_creation(sample_smartphone):
    """Проверяет создание объекта Smartphone."""
    assert sample_smartphone.efficiency == 3500
    assert sample_smartphone.model == "15 Pro"
    assert "Smartphone" in repr(sample_smartphone)
    assert str(sample_smartphone) == "iPhone 15 100000.0 руб. Остаток: 5 шт."


def test_lawngrass_creation(sample_lawngrass):
    """Проверяет создание объекта LawnGrass."""
    assert sample_lawngrass.country == "Россия"
    assert sample_lawngrass.color == "Зеленый"
    assert "LawnGrass" in repr(sample_lawngrass)
    assert str(sample_lawngrass) == "Трава Зеленая 1000.0 руб. Остаток: 20 шт."


def test_subclass_addition_same_type(sample_smartphone):
    """Тестирует сложение объектов одного типа (Smartphone + Smartphone)."""
    s2 = Smartphone("iPhone 14", "Старая модель", 80000.0, 10, 3200, "14", 128, "Белый")
    # (100000.0 * 5) + (80000.0 * 10) = 500000 + 800000 = 1300000.0
    assert sample_smartphone + s2 == 1300000.0


def test_subclass_addition_different_types(sample_smartphone, sample_lawngrass):
    """Тестирует сложение объектов разных типов (Smartphone + LawnGrass), ожидаем TypeError."""
    with pytest.raises(TypeError):
        sample_smartphone + sample_lawngrass
    with pytest.raises(TypeError):
        sample_lawngrass + sample_smartphone


def test_category_creation(sample_category, sample_product):
    """Проверяет создание категории и счетчики."""
    assert sample_category.name == "Электроника"
    assert sample_category.product_count == 1
    assert str(sample_category) == "Электроника количество продуктов: 1 шт."
    # Проверяем, что продукт в списке
    assert sample_product in sample_category._Category__products


def test_category_products_property(sample_category, sample_product):
    """Тестирует свойство products (геттер), возвращающее отформатированную строку."""
    expected_output = "Телевизор Samsung 50000.0 руб. Остаток: 10 шт."
    assert sample_category.products == expected_output


def test_category_add_product_valid(sample_category, sample_smartphone):
    """Тестирует добавление валидного продукта (наследника Product)."""
    sample_category.add_product(sample_smartphone)
    assert sample_category.product_count == 2
    assert sample_smartphone in sample_category._Category__products


def test_category_add_product_invalid(sample_category, sample_product):
    """Тестирует добавление невалидного продукта (базового Product, что не разрешено в этом классе)."""
    # Согласно логике Category, можно добавлять только Smartphone или LawnGrass
    # Если мы пытаемся добавить базовый Product, должно быть исключение
    with pytest.raises(TypeError):
        p_basic = Product("Чайник", "Описание", 1000.0, 5)
        sample_category.add_product(p_basic)

    # Также проверяем на None или другие типы
    with pytest.raises(TypeError):
        sample_category.add_product(None)


def test_category_middle_price_valid(sample_category, sample_smartphone):
    """Тестирует расчет средней цены с валидными данными."""
    sample_category.add_product(sample_smartphone)
    # Средняя цена: (50000*10 + 100000*5) / (10 + 5) - нет, расчет идет по ценам продуктов в списке, а не по суммарной стоимости запаса
    # Средняя цена: (50000 + 100000) / 2 = 75000.0
    assert sample_category.middle_price() == 75000.0


def test_category_middle_price_zero_division(capsys):
    """Тестирует расчет средней цены при пустом списке продуктов (деление на ноль)."""
    empty_category = Category("Пустая", "Описание", [])
    assert empty_category.middle_price() == 0
    captured = capsys.readouterr()
    assert "Общая стоимость товаров равна нулю" in captured.out