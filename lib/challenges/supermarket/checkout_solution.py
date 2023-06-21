

# noinspection PyUnusedLocal
# skus = unicode string

"""
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
+------+-------+------------------------+
"""

PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40
}

DISCOUNTS = {
    "A": {
        "quantity": 3,
        "price": 130
    },
    "B": {
        "quantity": 2,
        "price": 45
    }
}

GIVEAWAYS = {
    "E": {
        "quantity": 2,
        "free_item": "B"
    }
}


def checkout(skus: str):
    print(f"skus: {skus}")
    skus_list = sorted(list(skus))
    unique_skus = set(skus_list)
    total = 0

    if any([sku not in PRICES for sku in skus_list]):
        return -1

    for sku in unique_skus:
        print(f"current total: {total}")
        number_of_item = skus_list.count(sku)
        if sku in DISCOUNTS:
            discount = DISCOUNTS[sku]
            if "free_item" in discount:
                free_item_index = discount["free_item"]
                number_of_free_items = number_of_item // discount["quantity"]
                if free_item_index in unique_skus:
                    number_of_free_items = min(number_of_free_items, skus_list.count(free_item_index))
                    total -= number_of_free_items * PRICES[free_item_index]
                if free_item_index in DISCOUNTS:
                    free_item_discount = DISCOUNTS[free_item_index]
                    number_of_discounts_to_negate = skus_list.count(free_item_index) // free_item_discount["quantity"]
                    total += number_of_discounts_to_negate * free_item_discount["price"]

            else:    
                while number_of_item >= discount["quantity"]:
                    total += discount["price"]
                    number_of_item -= discount["quantity"]
        total += number_of_item * PRICES[sku]


    return total