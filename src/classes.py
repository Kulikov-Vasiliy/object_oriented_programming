from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный класс содержит общую функциональность"""

    @abstractmethod  # type: ignore[no-untyped-def]
    def __init__(self):  # type: ignore[no-untyped-def]
        pass

    @abstractmethod  # type: ignore[no-untyped-def]
    def __add__(self, other):  # type: ignore[no-untyped-def]
        pass


class MixinLog:
    """
    Класс-миксин, который будет при создании объекта,
    то есть при работе метода __init__, печатать в консоль
    информацию о том, от какого класса и с какими параметрами
    был создан объект
    """

    class_name: str
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):  # type: ignore[no-untyped-def]
        self.params = name, description, price, quantity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.params})"


class Product(BaseProduct, MixinLog):
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
        if not name:
            raise ValueError("Наименование товара не указано")
        self.name = name
        if not description:
            raise ValueError("Описание отсутствует")
        self.description = description
        if price is None:
            raise ValueError("Цена не указана")
        elif price <= 0:
            raise ValueError("Цена должна быть больше нуля")
        self.__price = price
        if quantity is None or quantity <= 0:
            raise (ValueError("Товар с нулевым количеством не может быть добавлен"))
        self.quantity = quantity
        super().__init__()

    @property  # type: ignore[no-redef]
    def price(self) -> float:
        return self.__price  # type: ignore[no-any-return]

    @price.setter  # type: ignore[no-redef]
    def price(self, price: float) -> None:
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
                if product.price < new_price:
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

    def __add__(self, other) -> float:  # type: ignore[no-untyped-def]
        total_price = self.__price * self.quantity + other.__price * other.quantity
        return total_price  # type: ignore[no-any-return]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" f"({self.name, self.description, self.price, self.quantity})"


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

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: int,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other) -> float:  # type: ignore[no-untyped-def]
        if isinstance(other, type(self)):
            return super().__add__(other)
        raise TypeError

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name}, {self.description}, "
            f"{self.price}, {self.quantity}, {self.efficiency}, {self.model}, "
            f"{self.memory}, {self.color})"
        )


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

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other) -> float:  # type: ignore[no-untyped-def]
        if isinstance(other, type(self)):
            return super().__add__(other)
        raise TypeError

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name}, {self.description}, "
            f"{self.price}, {self.quantity}, {self.country}, "
            f"{self.germination_period}, {self.color})"
        )


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

    def add_product(self, product=None) -> None:  # type: ignore[no-untyped-def]
        """Учет пополнения товара"""
        if isinstance(product, Product) and product is not None:
            if isinstance(product, Smartphone) or isinstance(product, LawnGrass):
                self.__products.append(product)
                self.product_count += 1
            else:
                raise TypeError
        else:
            raise TypeError

    def product_ended(self, name, product) -> None:  # type: ignore[no-untyped-def]
        """Учет убывания товара"""
        if self.name == name and product in self.__products:
            self.__products.remove(product)

        elif self.name != name and product in self.__products:
            self.__products.remove(product)

    def middle_price(self) -> int | float:
        """Определяет средний ценник всех товаров"""
        try:
            for product in self.__products:
                if not product or not product.price and not product.quantity:
                    print("Не указана цена товара или товар отсутствует")
                    return 0
                elif not isinstance(product.price, (float, int)):
                    print(
                        "Переданы неправильные типы данных в инфо поля о товаре, "
                        "например, строка вместо числа для цены или количества"
                    )
                    return 0
                elif product.price <= 0:
                    print("Цена или количество товара равно или меньше нуля")
                    return 0

            total_price = sum(product.price for product in self.__products)
            avg_price_tag = round(total_price / self.product_count, 2)
            return avg_price_tag  # type: ignore[no-any-return]

        except ZeroDivisionError:
            print("Общая стоимость товаров равна нулю")
            return 0
