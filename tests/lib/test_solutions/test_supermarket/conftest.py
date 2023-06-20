import pytest
from solutions.supermarket.checkout_solution import Basket, Discount, Items

DISCOUNTS = [
    Discount(
        required_items=Basket("AAA"),
        removed_items=Basket("AAA"),
        discounted_price=Items.A.value.total_price * 3 - 130,
    ),
    Discount(
        required_items=Basket("AAAAA"),
        removed_items=Basket("AAAAA"),
        discounted_price=Items.A.value.total_price * 5 - 200,
    ),
    Discount(
        required_items=Basket("BB"),
        removed_items=Basket("BB"),
        discounted_price=Items.B.value.total_price * 2 - 45,
    ),
    Discount(
        required_items=Basket("EE"),
        removed_items=Basket("EEB"),
        discounted_price=Items.B.value.total_price,
    ),
]


@pytest.fixture
def greeting_template():
    return "Hello, {}!"


@pytest.fixture
def discount_table():
    return DISCOUNTS
