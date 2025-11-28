import pytest
from src.classes import Product, Smartphone, LawnGrass, Category


@pytest.fixture
def sample_product():
    """Создает базовый продукт для тестов."""
    return Product("Телевизор Samsung", "Отличный телевизор", 50000.0, 10)


@pytest.fixture
def sample_smartphone():
    """Создает смартфон."""
    return Smartphone("iPhone 15", "Последняя модель", 100000.0, 5, 3500, "15 Pro", 256, "Черный")


@pytest.fixture
def sample_lawngrass():
    """Создает газонную траву."""
    return LawnGrass("Трава Зеленая", "Для газона", 1000.0, 20, "Россия", "2 недели", "Зеленый")


@pytest.fixture
def sample_category(sample_product):
    """Создает категорию с одним продуктом."""
    return Category("Электроника", "Все для дома", [sample_product])
