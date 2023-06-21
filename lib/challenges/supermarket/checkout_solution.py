import math


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):


    price_table = {
        'A': {'price': 50, 'special_offer': [(5, 200), (3, 130)]},
        'B': {'price': 30, 'special_offer': [(2, 45)]},
        'C': {'price': 20},
        'D': {'price': 15},
        'E': {'price': 40, 'special_offer': [(2, 'B')]},
        'F': {'price': 10, 'special_offer': [(2, 'F')]},
        'G': {'price': 20},
        'H': {'price': 10, 'special_offer': [(5, 45), (10, 80)]},
        'I': {'price': 35},
        'J': {'price': 60},
        'K': {'price': 70, 'special_offer': [(2, 120)]},
        'L': {'price': 90},
        'M': {'price': 15},
        'N': {'price': 40, 'special_offer': [(3, 'M')]},
        'O': {'price': 10},
        'P': {'price': 50, 'special_offer': [(5, 200)]},
        'Q': {'price': 30, 'special_offer': [(3, 80)]},
        'R': {'price': 50, 'special_offer': [(3, 'Q')]},
        'S': {'price': 20, 'special_offer_any_three': [(3, 45)]},
        'T': {'price': 20, 'special_offer_any_three': [(3, 45)]},
        'U': {'price': 40, 'special_offer': [(3, 'U')]},
        'V': {'price': 50, 'special_offer': [(2, 90), (3, 130)]},
        'W': {'price': 20},
        'X': {'price': 17, 'special_offer_any_three': [(3, 45)]},
        'Y': {'price': 20, 'special_offer_any_three': [(3, 45)]},
        'Z': {'price': 21, 'special_offer_any_three': [(3, 45)]}

    }

    item_counts = {}
    total_price = 0
    skus = sorted(skus)
    for item in skus:
        if item in price_table:
            item_counts[item] = item_counts.get(item, 0) + 1
        else:
            return -1

    item_counts_copy = item_counts.copy()
    count_special_three = 0
    running_offer_price = 0
    min_price = 100
    prices = []
    for item, count in item_counts.items():
        if 'special_offer' in price_table[item]:
            special_offers = sorted(price_table[item]['special_offer'], reverse=True)

            for offer in special_offers:

                offer_qty, offer_value = offer

                if not isinstance(offer_value, str):

                    while count >= offer_qty:
                        total_price += offer_value
                        count -= offer_qty

                if offer_value in item_counts and count >= offer_qty:

                    count_offer = count

                    while count_offer >= offer_qty:

                        if item != offer_value:
                            item_counts[offer_value] -= 1

                        elif item == offer_value and count_offer > offer_qty:
                            item_counts[offer_value] -= 1
                            total_price -= price_table[offer_value]["price"]

                        count_offer -= offer_qty

                    if item_counts[offer_value] == 0:

                        if "special_offer" in price_table[offer_value]:
                            total_price = 0
                        else:
                            total_price -= item_counts_copy[offer_value] * price_table[offer_value]["price"]

                    elif item_counts[offer_value] >= price_table[offer_value]["special_offer"][0][0] and item != offer_value:
                        total_price -= price_table[offer_value]["price"]

                    elif item_counts[offer_value] < price_table[offer_value]["special_offer"][0][0]:
                        total_price += item_counts[offer_value] * price_table[offer_value]["price"]
                        total_price -= price_table[offer_value]["special_offer"][0][1]

        elif "special_offer_any_three" in price_table[item]:
            count_special_three += count
            running_offer_price += count * price_table[item]["price"]

            prices.append(price_table[item]["price"])

            if price_table[item]["price"] < min_price:
                min_price = price_table[item]["price"]

            if count_special_three == 3:
                running_offer_price -= count * price_table[item]["price"]
                total_price -= running_offer_price
                total_price += price_table[item]["special_offer_any_three"][0][1]
                count_special_three = 0
                running_offer_price = 0
                continue
            elif count_special_three > 3:
                running_offer_price -= count * price_table[item]["price"]
                total_price -= running_offer_price
                total_price += price_table[item]["special_offer_any_three"][0][1]

                count_special_three -= 3
                running_offer_price = count_special_three * price_table[item]["price"]
                count = count_special_three

            if count_special_three > 1 and len(prices) > 1:
                prices = sorted(prices)
                running_offer_price = 0

                for i in range(count_special_three):
                    total_price += prices[i]
                    running_offer_price += prices[i]
                    count -= 1

            elif count_special_three == 1:

                price_table[item]["price"] = min_price

        total_price += count * price_table[item]['price']

    return total_price
