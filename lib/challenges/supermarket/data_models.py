from __future__ import annotations

import dataclasses
import functools
from abc import ABC, abstractmethod
from collections import Counter
from typing import Dict


class BaseDiscount(ABC):
    _value: int
    _cost: int
    discount_compute_required: bool

    @property
    def value(self):
        if not self._value:
            raise ValueError(
                "Value must be initialized, perhaps compute_value was not called"
            )
        return self._value

    @property
    def cost(self):
        """Final price of items"""
        if not self._cost:
            raise ValueError(
                "Cost must be initialized, perhaps compute_value was not called"
            )
        return self._cost

    @abstractmethod
    def compute_value(self, basket: Basket) -> int:
        """Value of discount"""
        raise NotImplementedError

    @abstractmethod
    def discount_met(self, basket: Basket):
        """Does the basket meet the discount requirements"""
        raise NotImplementedError

    @abstractmethod
    def apply_discount(self, basket: Basket) -> int:
        raise NotImplementedError

    def __lt__(self, other):
        return self.value < other.value


class BuyNForYDiscount(BaseDiscount):
    """Buy N for Y cost discount"""

    def __init__(self, item: Item, n: int, y: int):
        self.item = item
        self.n = n
        self.y = y
        self._cost = y
        self.discount_compute_required = False
        self._value = item.price * n - y

    def compute_value(self, basket: Basket) -> int:
        pass

    def discount_met(self, basket: Basket):
        return basket.get_item_count(self.item) >= self.n

    def apply_discount(self, basket: Basket) -> Basket:
        basket.items[self.item.key].quantity -= self.n
        return basket


class BuyNGetYFreeDiscount(BaseDiscount):
    """Buy N get Y free discount discount"""

    def __init__(self, item: Item, n: int, free_item: Item, y: int):
        self.item = item
        self.free_item = free_item
        self.n = n
        self.y = y
        self._cost = self.n * item.price
        self.discount_compute_required = False
        self._value = item.price * n - free_item.price * y

    def compute_value(self, basket: Basket) -> int:
        pass

    def discount_met(self, basket: Basket):
        return (
            basket.get_item_count(self.item) >= self.n
            and basket.get_item_count(self.free_item) >= self.y
        )

    def apply_discount(self, basket: Basket) -> Basket:
        basket.items[self.item.key].quantity -= self.n
        basket.items[self.free_item.key].quantity -= self.y
        return basket


class BuyAnyNItemsForYDiscount(BaseDiscount):
    """Buy n items from a set of items for y price"""

    # basket to remove when applying discount post computation of discount value
    # as the value is dynamic based on which items are selected for removal
    _basket_remove: Basket

    def __init__(self, basket: Basket, n: int, y: int):
        # presort items by price
        self.items = sorted(basket.items.values(), reverse=True)
        self.n = n
        self.y = y
        self._cost = y
        self.discount_compute_required = True

    def compute_value(self, basket: Basket) -> int:
        """The best value will be derived if we use the most expensive items first"""
        total_items = 0
        real_value = 0
        sku_removed = ""
        for item in self.items:
            required = self.n - total_items
            available = min(required, basket.get_item_count(item))
            total_items += available
            sku_removed = f"{sku_removed}{item.key * available}"
            real_value += item.price * available
        if total_items < self.n:
            raise ValueError("Not Enough Items")
        self._value = real_value - self.y
        self._basket_remove = Basket(sku_removed)

    def discount_met(self, basket: Basket):
        try:
            self.compute_value(basket)
        except ValueError:
            return False
        return True

    def apply_discount(self, basket: Basket) -> Basket:
        return basket - self._basket_remove


class Basket:
    _items: Dict[str, Item]

    @property
    def value(self):
        return sum([item.total_price for item in self.items.values()])

    @property
    def items(self) -> Dict[str, Item]:
        if not hasattr(self, "_items"):
            self._items = {}
        return self._items

    def __init__(self, skus):
        from .constants import Items

        combined = Counter(skus)
        for key, quantity in combined.items():
            item = Items[key].value
            self.items[key] = Item(key=key, quantity=quantity, price=item.total_price)

    def __sub__(self, other: Basket):
        """Subtracts another Basket instance from this one."""
        if not set(self.items.keys()).issuperset(set(other.items.keys())):
            raise ValueError("Can't subtract non-existing items")
        new_basket = self.__copy__()
        for key, item in other.items.items():
            new_basket.items[key].quantity -= other.items[key].quantity
            if new_basket.items[key].quantity < 0:
                raise ValueError("Cant have negative quantity of items in basket")
        return new_basket

    def get_item_count(self, item: Item):
        if item.key in self.items:
            return self.items[item.key].quantity
        return 0

    def __copy__(self):
        skus = "".join(key * val.quantity for key, val in self.items.items())
        return Basket(skus)


@functools.total_ordering
@dataclasses.dataclass
class Item:
    key: str
    price: int
    quantity: int = 1

    @property
    def total_price(self) -> int:
        return self.quantity * self.price

    def construct(self, quantity: int):
        self.quantity = quantity
        return self

    def __le__(self, other):
        return self.price < other.price
