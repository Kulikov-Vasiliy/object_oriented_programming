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


    def __str__(self):
        return f"{self.name}, {self.description}, {self.price} руб., {self.quantity} шт."



class Category:
    """
    Класс собирает информацию о категории:
    категория
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

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []
        Category.category_count += 1
        self.product_count = len(self.__products)

    @property
    def products(self):
        return [str(product) for product in self.__products]

    def add_product(self, name, product=None):
        """Учет пополнения товара"""
        if self.name == name and product is not None:
            self.__products.append(product)

        elif self.name != name and product is not None:
            self.__products.append(product)

    # @product_ended.setter
    def product_ended(self, name, product=not None):
        """Учет убывания товара"""
        if self.name == name and product in self.products:
            self.__products.remove(product)

        elif self.name != name and product in self.products:
            self.__products.remove(product)
