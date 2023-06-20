import pytest
from solutions.supermarket.checkout_solution import (
    Basket,
    Discount,
    Item,
    Items,
    checkout,
    combine_skus_duplicates,
    compute_discounts,
    validate_skus,
)


def _get_sku_parametrization():
    return (
        "skus,expected",
        [
            ("A", Items.A.value.total_price),
            ("AA", Items.A.value.total_price * 2),
            ("AAAAA", 200),
            ("AAAAAAAA", 200 + 130),
            ("EE", 80),
            ("BBEE", 40 * 2 + 30),
            ("BBEEB", 40 * 2 + 45),
            ("FFF", Items.F.value.total_price * 2),
            ("STX", 45),
            ("SSSZ", 65),
            ("ZZZ", 45),
            ("SSS", 45),
            ("STXS", 62),
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ", 1602),
        ],
    )


class TestItem:
    def test_item_initialization(self):
        item = Item("A", 50, 3)
        assert item.key == "A"
        assert item.price == 50
        assert item.quantity == 3

    def test_item_total_price(self):
        item = Item("A", 50, 3)
        assert item.total_price == 150

    def test_item_construct(self):
        item = Item("A", 50)
        assert item.quantity == 1
        item.construct(3)
        assert item.quantity == 3
        assert item.total_price == 150


class TestBasket:
    def test_basket_initialization(self):
        basket = Basket("")
        assert isinstance(basket.items, dict)
        assert basket.value == 0

    def test_basket_create(self):
        basket = Basket("AAABBB")
        assert len(basket.items) == 2
        assert basket.items["A"].quantity == 3
        assert basket.items["B"].quantity == 3

    def test_basket_value(self):
        basket = Basket("AAABBB")
        assert basket.value == (
            Items["A"].value.total_price * 3 + Items["B"].value.total_price * 3
        )

    def test_basket_subtraction(self):
        basket1 = Basket("AAABBB")
        basket2 = Basket("AAB")
        basket1 - basket2
        assert basket1.items["A"].quantity == 1
        assert basket1.items["B"].quantity == 2

    def test_basket_subtraction_error(self):
        basket1 = Basket("AAABBB")
        basket2 = Basket("AABCC")
        with pytest.raises(TypeError):
            basket1 - basket2


class TestDiscount:
    def setup_method(self):
        self.basket = Basket("AAABBB")
        self.discount = Discount(
            required_items=Basket("AAA"),
            removed_items=Basket("AAA"),
            discounted_price=130,
        )

    def test_discount_initialization(self):
        assert isinstance(self.discount.required_items, Basket)
        discounted_price = 130
        assert (
            self.discount.discounted_price == discounted_price
        ), self.discount.discounted_price

    def test_discount_apply(self):
        discounted_price = self.discount.apply_discount(self.basket)
        assert discounted_price == 130
        assert "A" not in self.basket.items

    def test_discount_comparison(self):
        other_discount = Discount(
            required_items=Basket("BB"),
            removed_items=Basket("BB"),
            discounted_price=55,
        )
        assert not self.discount <= other_discount
        assert other_discount <= self.discount


class TestCHK:
    @pytest.mark.parametrize(
        "input_skus",
        [
            "a",
            "1",
            "abc",
            "A B C",
            "123",
        ],
    )
    def test_validate_skus_invalid(self, input_skus):
        # ARRANGE
        # ACT
        # ASSERT
        with pytest.raises(TypeError):
            validate_skus(input_skus)

    @pytest.mark.parametrize("input_skus", ["AA", "AB", ""])
    def test_validate_skus_valid(self, input_skus):
        # ARRANGE
        # ACT
        # ASSERT
        validate_skus(input_skus)

    @pytest.mark.parametrize(
        "skus,expected",
        [
            ("A", {"A": 1}),
            ("AA", {"A": 2}),
            ("ABC", {"A": 1, "B": 1, "C": 1}),
            ("AAB", {"A": 2, "B": 1}),
            ("", {}),
        ],
    )
    def test_combine_skus_duplicates(self, skus, expected):
        # ARRANGE
        # ACT
        combined = combine_skus_duplicates(skus)
        # ASSERT
        assert combined == expected

    @pytest.mark.parametrize(*_get_sku_parametrization())
    def test_compute_discounts(self, skus, expected):
        assert compute_discounts(skus) == expected

    @pytest.mark.parametrize(*_get_sku_parametrization())
    def test_checkout(self, skus, expected):
        assert checkout(skus) == expected

    def test_checkout_err(self):
        assert checkout("invalid") == -1
