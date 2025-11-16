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

    def __init__(self, name, description, price, quantity):  # type: ignore[no-untyped-def]
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property  # type: ignore[no-redef]
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price) -> None:
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

    def __str__(self) -> str:
        return f"{self.name} {self.__price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, product_info, product_list=None):  # type: ignore[no-untyped-def]
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
            quantity=quantity_to_add,
        )
        if product_list is not None:
            product_list.append(new_product)
        return new_product

    def __add__(self, other) -> float:
        return (self.__price * self.quantity) + (other.__price * other.quantity)


class Smartphone(Product):
    """
    Подкласс Product собирает информацию:
    производительность
    модель
    объем встроенной памяти
    цвет
    """
    efficiency: int
    model: str
    memory: int
    color: str

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other) -> float:
        if isinstance(other, Smartphone):
            return super().__add__(other)
        raise TypeError


class LawnGrass(Product):
    """
    Подкласс Product собирает информацию:
    страна-производитель
    срок прорастания
    цвет
    """
    country: str
    germination_period: str
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other) -> float:
        if isinstance(other, LawnGrass):
            return super().__add__(other)
        raise TypeError


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
    products: list
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products=None):  # type: ignore[no-untyped-def]
        self.name = name
        self.description = description
        self.__products = products if products is not None else []
        Category.category_count += 1
        self.product_count = len(self.__products)

    def __str__(self) -> str:
        return f"{self.name} количество продуктов: {self.product_count} шт."

    def product_list(self, product_info):  # type: ignore[no-untyped-def]
        # Вызываем метод new_product и передаем текущий список продуктов
        return Product.new_product(product_info, self.__products)

    @property  # type: ignore[no-redef]
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    def add_product(self, name, product=None) -> None:
        """Учет пополнения товара"""
        if self.name == name and product is not None:
            self.__products.append(product)
            self.product_count += 1

        elif self.name != name and product is not None:
            self.__products.append(product)
            self.product_count += 1

    def product_ended(self, name, product) -> None:
        """Учет убывания товара"""
        if self.name == name and product in self.__products:
            self.__products.remove(product)

        elif self.name != name and product in self.__products:
            self.__products.remove(product)
