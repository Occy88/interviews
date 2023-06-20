from __future__ import annotations

import collections
import dataclasses
import functools
import re
from enum import Enum
from typing import Dict, List


@functools.total_ordering
@dataclasses.dataclass
class Discount:
    required_items: Basket
    # discounted_price = price to charge customer for discount
    discounted_price: int
    removed_items: Basket  # a function that applies the discount
    choose: int = dataclasses.field(default=None)
    _sorted_required_items: List[Item] = dataclasses.field(default=None)

    @property
    def total_discounted_price(self):
        """
        Returns
        -------
        Real cost to supermarket (value of removed_items - discounted price)


        """
        return self.removed_items.value - self.discounted_price

    @property
    def sorted_required_items(self):
        if self._sorted_required_items is None:
            self._sorted_required_items = sorted(
                self.required_items.items.values(), reverse=True
            )
        return self._sorted_required_items

    def choose_items_to_remove(self, basket: Basket):
        if self.choose is None:
            return
        to_remove = self.choose
        basket_copy = basket.__copy__()
        skus = ""
        for item in self.sorted_required_items:
            if to_remove <= 0:
                break
            if (
                item.key in basket_copy.items
                and basket_copy.items[item.key].quantity > 0
            ):
                can_remove = min(basket_copy.items[item.key].quantity, to_remove)
                basket_copy.items[item.key].quantity -= can_remove
                skus = f"{skus}{item.key * can_remove}"
                to_remove -= can_remove
        if to_remove > 0:
            raise TypeError("Offer not met")
        self.removed_items = Basket(skus)

    def apply_discount(self, basket: Basket):
        """
        Applies the discount to the provided basket.

        Parameters
        ----------
        basket : Basket
            The basket to which the discount will be applied.

        Returns
        -------
        Basket
            The basket after applying the discount.

        Raises
        ------
        ValueError,TypeError
        """
        self.choose_items_to_remove(basket)

        basket -= self.removed_items
        return self.discounted_price

    def __le__(self, other):
        return self.total_discounted_price <= other.total_discounted_price


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


def combine_skus_duplicates(skus: str) -> Dict[str, int]:
    """
    Counts the frequency of each SKU in a given string.

    The function takes a string of SKUs where each SKU is represented by
    an uppercase letter [A-Z]. It returns a dictionary where the keys are
    the SKUs and the values are the count of each SKU in the input string.

    Parameters
    ----------
    skus : str
        A string containing the SKUs to be counted. Each SKU should be an uppercase
        letter [A-Z].

    Returns
    -------
    dict
        A dictionary where the keys are the unique SKUs from the input string and the
        values are the count of each SKU.
        If a SKU is not present in the input string, it will not appear in the output
        dictionary.

    Examples
    --------
    >>> combine_skus_duplicates('AAB')
    {'A': 2, 'B': 1}

    >>> combine_skus_duplicates('ABC')
    {'A': 1, 'B': 1, 'C': 1}
    """
    combined = collections.defaultdict(int)
    for sku in skus:
        combined[sku] += 1
    return combined


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
        combined = combine_skus_duplicates(skus)
        for key, quantity in combined.items():
            item = Items[key].value
            self.items[key] = Item(key=key, quantity=quantity, price=item.total_price)

    def __sub__(self, other: Basket):
        """Subtracts another Basket instance from this one."""
        if not isinstance(other, Basket):
            raise TypeError(f"Unsupported operand type for -: {type(other)}")
        # VALIDATE FIRST
        for item_key, other_item in other.items.items():
            if item_key not in self.items:
                raise TypeError(f"{item_key} not found")
            result = self.items[item_key].quantity - other_item.quantity
            if result < 0:
                raise ValueError("can't have negative quantity of items")
        # APPLY
        for item_key, other_item in other.items.items():
            result = self.items[item_key].quantity - other_item.quantity
            self.items[item_key].quantity = result

            # If quantity is zero, remove the item
            if self.items[item_key].quantity == 0:
                del self.items[item_key]

        return self

    def __copy__(self):
        skus = "".join(key * val.quantity for key, val in self.items.items())
        return Basket(skus)


class Items(Enum):
    A = Item("A", 50)
    B = Item("B", 30)
    C = Item("C", 20)
    D = Item("D", 15)
    E = Item("E", 40)
    F = Item("F", 10)
    G = Item("G", 20)
    H = Item("H", 10)
    I = Item("I", 35)  # noqa
    J = Item("J", 60)
    K = Item("K", 70)
    L = Item("L", 90)
    M = Item("M", 15)
    N = Item("N", 40)
    O = Item("O", 10)  # noqa
    P = Item("P", 50)
    Q = Item("Q", 30)
    R = Item("R", 50)
    S = Item("S", 20)
    T = Item("T", 20)
    U = Item("U", 40)
    V = Item("V", 50)
    W = Item("W", 20)
    X = Item("X", 17)
    Y = Item("Y", 20)
    Z = Item("Z", 21)


def validate_skus(skus):
    """Ensure skus are a valid string [A-Z]
    Parameters
    ----------
    skus

    Returns
    -------

    """
    if skus == "":
        return
    pattern = "^[A-Z]+$"
    if not re.fullmatch(pattern, skus):
        raise TypeError(f"Expected {skus} to match {pattern}")


def compute_discounts(skus: str) -> int:
    """Computest the total price given the frequency of skus as a str.
    Parameters
    ----------
    skus : str
    A string containing the SKUs to be counted. Each SKU should be an uppercase
    letter [A-Z].

    Returns
    -------

    """
    basket = Basket(skus)
    total_discount = 0
    for discount in DISCOUNTS:
        while True and len(basket.items) > 0:
            try:
                total_discount += discount.apply_discount(basket)
            except (ValueError, TypeError):
                break
    return basket.value + total_discount  # Final price is the sum of the remaining
    # basket value and total discounts applied


DISCOUNTS = [
    # | A    | 50    | 3A for 130, 5A for 200 |
    Discount(
        required_items=Basket("A" * 3),
        removed_items=Basket("A" * 3),
        discounted_price=130,
    ),
    Discount(
        required_items=Basket("A" * 5),
        removed_items=Basket("A" * 5),
        discounted_price=200,
    ),
    # | B    | 30    | 2B for 45              |
    Discount(
        required_items=Basket("B" * 2),
        removed_items=Basket("B" * 2),
        discounted_price=45,
    ),
    # | E    | 40    | 2E get one B free      |
    Discount(
        required_items=Basket("EE"),
        removed_items=Basket("EEB"),
        discounted_price=Items.E.value.price * 2,
    ),
    # | F    | 10    | 2F get one F free      |
    Discount(
        required_items=Basket("F" * 3),
        removed_items=Basket("F" * 3),
        discounted_price=Items.F.value.price * 2,
    ),
    #   | H    | 10    | 5H for 45, 10H for 80  |
    Discount(
        required_items=Basket("H" * 5),
        removed_items=Basket("H" * 5),
        discounted_price=45,
    ),
    Discount(
        required_items=Basket("H" * 10),
        removed_items=Basket("H" * 10),
        discounted_price=80,
    ),
    #   | K    | 80    | 2K for 120             |
    Discount(
        required_items=Basket("K" * 2),
        removed_items=Basket("K" * 2),
        discounted_price=120,
    ),
    #    | N    | 40    | 3N get one M free      |
    Discount(
        required_items=Basket("N" * 3),
        removed_items=Basket("N" * 3 + "M"),
        discounted_price=Items.N.value.price * 3,
    ),
    #     | P    | 50    | 5P for 200             |
    Discount(
        required_items=Basket("P" * 5),
        removed_items=Basket("P" * 5),
        discounted_price=200,
    ),
    # | Q    | 30    | 3Q for 80              |
    Discount(
        required_items=Basket("Q" * 3),
        removed_items=Basket("Q" * 3),
        discounted_price=80,
    ),
    # | R    | 50    | 3R get one Q free      |
    Discount(
        required_items=Basket("R" * 3),
        removed_items=Basket("R" * 3 + "Q"),
        discounted_price=Items.R.value.price * 3,
    ),
    # | U    | 40    | 3U get one U free      |
    Discount(
        required_items=Basket("U" * 3),
        removed_items=Basket("U" * 4),
        discounted_price=Items.U.value.price * 3,
    ),
    # | V    | 50    | 2V for 90, 3V for 130  |
    Discount(
        required_items=Basket("V" * 2),
        removed_items=Basket("V" * 2),
        discounted_price=90,
    ),
    Discount(
        required_items=Basket("V" * 3),
        removed_items=Basket("V" * 3),
        discounted_price=130,
    ),
    # | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
    Discount(
        required_items=Basket("STXYZ"),
        removed_items=Basket(""),
        discounted_price=45,
        choose=3,
    ),
]
DISCOUNTS.sort(
    reverse=True
)  # Now discounts are sorted in descending order of discounted_price


def checkout(skus: str) -> int:
    """Compute skus checkout value given discounts

    Parameters
    ----------
    skus: string representing skus
    ABBBDKEEEDJHHSKKKE

    Returns
    -------
    int: > 0 or -1 for error.
    """
    try:
        validate_skus(skus)
    except TypeError:
        return -1
    return compute_discounts(skus)
