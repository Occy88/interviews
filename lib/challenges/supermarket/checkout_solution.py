from collections import defaultdict


prices = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
    'G': 20,
    'H': 10,
    'I': 35,
    'J': 60,
    'K': 70,
    'L': 90,
    'M': 15,
    'N': 40,
    'O': 10,
    'P': 50,
    'Q': 30,
    'R': 50,
    'S': 20,
    'T': 20,
    'U': 40,
    'V': 50,
    'W': 20,
    'X': 17,
    'Y': 20,
    'Z': 21,
}

special_offers = {
    # Each tuple is (number of items, discounted price)
    'A': [(5, 200), (3, 130)],
    'B': [(2, 45)],
    'H': [(10, 80), (5, 45)],
    'K': [(2, 120)],
    'P': [(5, 200)],
    'Q': [(3, 80)],
    'V': [(3, 130), (2, 90)],
}

group_discount_offers = {
    # Match any combination of the skus in the key such that X of them gives Y price, value being (X, Y)
    ('Z', 'S', 'T', 'Y', 'X'): (3, 45)
}

buy_x_get_y_free_offers = {
    # Item to get free, number of items required for discount, num to get free
    'E': ('B', 2, 1),
    'F': ('F', 2, 1),
    'N': ('M', 3, 1),
    'R': ('Q', 3, 1),
    'U': ('U', 3, 1),
}

# noinspection PyUnusedLocal
# skus = unicode string

def build_counts_by_sku(skus: str):
    if not type(skus) == str:
        raise ValueError

    counts_per_sku = defaultdict(int)
    for sku in skus:
        if sku in prices:
            counts_per_sku[sku] += 1
        else:
            raise ValueError
    return counts_per_sku


def run_buy_x_get_y_free_offers(counts_per_sku: dict) -> dict:
    """
    Run all buy x get y free offers, removing the free items from the count
    for that item.

    Note - mutates the input counts
    """
    for item, offer in buy_x_get_y_free_offers.items():
        count = counts_per_sku[item]
        free_sku = offer[0]
        num_required = offer[1]
        num_given_free_per_occurence = offer[2]
        if (free_sku == item):
            # Special case for the sku giving itself for free
            # offer applies in groups of (amount_to_trigger + amount_to_remove)
            # TODO - does this work for Y > 1?
            num_required = num_required + num_given_free_per_occurence
        num_occurrences = count // num_required
        num_free = num_given_free_per_occurence * num_occurrences
        # Even if the offer fires, can't give more for free than are actually in the basket
        counts_per_sku[free_sku] = max(
            0,
            counts_per_sku[free_sku] - num_free
        )
    return counts_per_sku


def run_group_offers(counts_by_sku) -> int:
    """
    Run all group offers, removing SKUs used from the count. Return the subtotal for all offers applied.

    Note: mutates the counts_by_sku passed in, removing all items used towards offers
    """
    subtotal = 0
    for sku_list, offer_terms in group_discount_offers.items():
        amount_required = offer_terms[0]
        price = offer_terms[1]
        total_count = sum(counts_by_sku[sku] for sku in sku_list)
        total_offers = total_count // amount_required
        total_items_to_remove = total_offers * amount_required
        for sku in sku_list:
            remaining = counts_by_sku[sku]
            amount_to_remove = min(total_items_to_remove, remaining)
            counts_by_sku[sku] -= amount_to_remove
            total_items_to_remove -= amount_to_remove

        subtotal += price * total_offers

    return subtotal


def run_x_for_y_offers(counts_per_sku):
    """
    Run all 'X skus for Y price' offers. Return the subtotal for all offers applied.

    Note: mutates the counts_by_sku passed in, removing all items used towards offers
    """
    total = 0
    for sku, count in counts_per_sku.items():
        remaining = count
        if special_offers_for_sku := special_offers.get(sku):
            for special_offer in special_offers_for_sku:
                num_items_required = special_offer[0]
                discounted_price = special_offer[1]
                num_of_discounts = remaining // num_items_required
                total += num_of_discounts * discounted_price
                remaining -= num_of_discounts * num_items_required
        counts_per_sku[sku] = remaining
    return total


def total_for_items(counts_per_sku):
    total = 0
    for sku, count in counts_per_sku.items():
        total += prices[sku] * count
    return total


def checkout(skus):
    # String will have a letter for each occurrence of the item
    try:
        counts_per_sku = build_counts_by_sku(skus)
    except ValueError:
        return -1

    run_buy_x_get_y_free_offers(counts_per_sku)
    total = run_group_offers(counts_per_sku)
    total += run_x_for_y_offers(counts_per_sku)
    total += total_for_items(counts_per_sku)

    return total