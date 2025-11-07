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
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        print(price)
        while True:
            submit_changed_price = input("yes/no ").lower()
            if submit_changed_price:  # Проверяем, что строка не пустая
                submit_changed_price = submit_changed_price[0]
                if submit_changed_price == "y":
                    if price <= 0:
                        print("Цена не должна быть нулевая или отрицательная")
                        break
                    elif price > 0:
                        self.__price = price
                        break
                elif submit_changed_price == "n":
                    break
            else:
                print("Пожалуйста, введите 'yes' или 'no'")

    def __str__(self):
        return f"{self.name}, {self.description}, {self.__price} руб., {self.quantity} шт."

    @classmethod
    def new_product(cls, product_info, product_list=None):
        name_of_new = product_info.get("name")
        quantity_to_add = product_info.get("quantity", 0)
        new_price = product_info.get("price")
        # Проверить, передан ли список продуктов
        if product_list is not None:
            for product in product_list:
                if product.name == name_of_new:
                    product.quantity += quantity_to_add
                if product.__price < new_price:
                    product.price = new_price

                    return product

        # Если совпадений нет или список не передан, создаем новый продукт
        new_product = cls(
            name=product_info.get("name"),
            description=product_info.get("description"),
            price=product_info.get("price"),
            quantity=quantity_to_add
        )
        if product_list is not None:
            product_list.append(new_product)
        return new_product


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

    def product_list(self, product_info):
        # Вызываем метод new_product и передаем текущий список продуктов
        return Product.new_product(product_info, self.__products)

    @property
    def products(self):
        return "\n".join(str(product) for product in self.__products)

    def add_product(self, name, product=None):
        """Учет пополнения товара"""
        if self.name == name and product is not None:
            self.__products.append(product)

        elif self.name != name and product is not None:
            self.__products.append(product)

    def product_ended(self, name, product):
        """Учет убывания товара"""
        if self.name == name and product in self.products:
            self.__products.remove(product)

        elif self.name != name and product in self.products:
            self.__products.remove(product)
