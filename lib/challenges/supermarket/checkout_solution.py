from __future__ import annotations

from .constants import DISCOUNTS
from .data_models import Basket
from .utils import choose_max, validate_skus

# pre-sort static discounts.


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
    static_discounts = sorted(
        [d for d in DISCOUNTS if not d.discount_compute_required], reverse=True
    )
    dynamic_discounts = [d for d in DISCOUNTS if d.discount_compute_required]

    basket = Basket(skus)
    checkout_value = 0

    while static_discounts or dynamic_discounts:
        # compute dynamic values first
        dynamic_discounts = sorted(
            [d for d in dynamic_discounts if d.discount_met(basket)], reverse=True
        )
        static_discounts = [d for d in static_discounts if d.discount_met(basket)]
        try:
            best_discount = choose_max(dynamic_discounts, static_discounts)
        except ValueError:
            break
        basket = best_discount.apply_discount(basket)
        checkout_value += best_discount.cost
    return basket.value + checkout_value
    # basket value and total discounts applied


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
