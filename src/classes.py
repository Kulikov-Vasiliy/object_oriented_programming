class Product:
    """
    Класс собирает информацию о продукте:
    имя
    описание
    цена
    количество
    """
    name: str
    description: str
    price: float
    quantity: int


    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Класс собирает информацию о категории:
    категорияv
    описание
    продукты
    количество категорий
    количество продуктов в категории
    """
    name: str
    description: str
    products: []
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        self.product_count = len(self.products)

    def product_added(self, name, product):
        """Учет пополнения товара"""
        if self.name == name:
            self.products.append(product)

            return product

        self.products.append(product)

        return product

    def product_ended(self, name, product):
        """Учет убывания товара"""
        if self.name == name and product in self.products:
            self.products.remove(product)

            return product

        return product
