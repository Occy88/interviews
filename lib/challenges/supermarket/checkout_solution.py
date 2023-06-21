from collections import Counter


def checkout(items):
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

    special_double_offers = {
        'A': [{'quantity': 5, 'price': 200}, {'quantity': 3, 'price': 130}],
        'H': [{'quantity': 10, 'price': 80}, {'quantity': 5, 'price': 45}],
        'V': [{'quantity': 3, 'price': 130}, {'quantity': 2, 'price': 90}],
    }
    special_price_offers = {
        'B': {'quantity': 2, 'price': 45},
        'K': {'quantity': 2, 'price': 120},
        'P': {'quantity': 5, 'price': 200},
        'Q': {'quantity': 3, 'price': 80},
    }
    special_extra_offers = {
        'F': {'quantity': 2, 'free': 'F'},
        'U': {'quantity': 3, 'free': 'U'},
    }
    special_free_offers = {
        'E': {'quantity': 2, 'free': 'B'},
        'N': {'quantity': 3, 'free': 'M'},
        'R': {'quantity': 3, 'free': 'Q'},
    }

    # check if skus is empty
    if not items:
        return 0

    # check if skus is a string
    if not isinstance(items, str):
        return -1

    # count the frequency of each sku
    item_counts = Counter(items)
    total_price = 0

    # check if skus contains only valid skus
    if any([sku not in prices.keys() for sku in item_counts.keys()]):
        return -1

    # select from special_free_offer items first if available
    for free_item, offer in special_free_offers.items():
        if free_item in item_counts.keys() and offer['free'] in item_counts.keys():
            count = item_counts[free_item]
            total_free = count // offer['quantity']
            if total_free >= 1:
                item_counts[offer['free']] -= total_free
                if item_counts[offer['free']] < 0:
                    item_counts[offer['free']] = 0

    # apply special_combo_offers
    # special combo list is sorted from low to high prices
    special_combo_offers = ['X', 'S', 'T', 'Y', 'Z']
    # Creating a new Counter with selected items
    selected_counts = Counter(
        {item: item_counts[item] for item in special_combo_offers if
         item in item_counts.keys()})
    # Summing the values of the Counter
    total_selected_count = sum(selected_counts.values())

    if total_selected_count >= 3:
        total_price += (total_selected_count // 3) * 45
        # Sort the Counter by the special_combo_offers list to favour the customer
        sorted_counter = sorted(selected_counts.items(),
                                key=lambda x: special_combo_offers.index(x[0]))
        total_combo_remainder_count = total_selected_count % 3
        if total_combo_remainder_count > 0:
            y = 0
            while y <= total_combo_remainder_count:
                # select the key value pairs from the sorted counter to favour the customer
                key_y, value_y = sorted_counter[y]
                # if the value_y is greater that remainder, use it
                if value_y >= total_combo_remainder_count:
                    total_price += prices[key_y] * total_combo_remainder_count
                    break
                item_remainder_count = value_y % 3
                if item_remainder_count == 0:
                    y += 1
                    total_combo_remainder_count -= 1
                    continue
                total_price += prices[key_y] * item_remainder_count
                y += item_remainder_count
                total_combo_remainder_count -= item_remainder_count

        # Subtract the selected_counts from the original counter
        item_counts = item_counts - selected_counts

    if len(item_counts) > 0:
        for item, count in item_counts.items():
            # apply special offers
            if item in special_double_offers.keys():
                offer = special_double_offers[item]
                for o in offer:
                    if count >= o['quantity']:
                        total_price += (count // o['quantity']) * o['price']
                        count %= o['quantity']

            if item in special_price_offers.keys():
                offer = special_price_offers[item]
                if count >= offer['quantity']:
                    total_price += (count // offer['quantity']) * offer['price']
                    count %= offer['quantity']

            if item in special_extra_offers.keys():
                offer = special_extra_offers[item]
                offer_quantity = offer['quantity'] + 1
                if count >= offer_quantity:
                    free_count = count // offer_quantity
                    remainder_count = count % offer_quantity
                    if remainder_count == 1:
                        free_count += 1
                    count = count - free_count + remainder_count

                    # add the price of the remaining items
            total_price += count * prices.get(item, 0)

    return total_price

