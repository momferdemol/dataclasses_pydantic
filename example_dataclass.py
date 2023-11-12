from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum, auto


class OrderStatus(StrEnum):
    OPEN = auto()
    CLOSED = auto()


@dataclass
class Product:
    name: str = field(compare=True)
    category: str = field(compare=True)
    shipping_weight: float = field(compare=False)
    unit_price: int = field(compare=True)
    tax_percent: float = field(compare=False)

    def __post_init__(self) -> None:
        if self.unit_price < 0:
            raise ValueError("unit_price attribute must be greater then zero.")

        if self.shipping_weight < 0:
            raise ValueError("shipping_weight attribute must be greater then zero.")

        if not 0 < self.tax_percent < 1:
            raise ValueError("tax_percent attribute must be between zero and one.")


@dataclass
class Order:
    status: OrderStatus
    creation_date: date = date.today()
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    @property
    def sub_total(self) -> int:
        return sum((product.unit_price for product in self.products))

    @property
    def tax(self) -> float:
        return sum(
            (product.unit_price * product.tax_percent for product in self.products)
        )

    @property
    def total_shipping_weight(self) -> float:
        return sum((product.shipping_weight for product in self.products))


def create_order() -> None:
    banana = Product(
        name="banana",
        category="fruit",
        shipping_weight=0.5,
        unit_price=215,
        tax_percent=0.07,
    )

    mango = Product(
        name="mango",
        category="fruit",
        shipping_weight=2,
        unit_price=319,
        tax_percent=0.07,
    )

    apple = Product(
        name="apple",
        category="fruit",
        shipping_weight=0.4,
        unit_price=115,
        tax_percent=0.05,
    )

    order = Order(status=OrderStatus.OPEN)
    for product in [banana, mango, apple]:
        order.add_product(product)

    print(f"Comparison between mango and apple: {mango == apple}")
    print(f"Total order price: ${order.sub_total/100:.2f}")
    print(f"Subtotal order price: ${order.sub_total/100:.2f}")
    print(f"Value paid in taxes: ${order.tax/100:.2f}")
    print(f"Total weight order: {order.total_shipping_weight} kg")


if __name__ == "__main__":
    create_order()
