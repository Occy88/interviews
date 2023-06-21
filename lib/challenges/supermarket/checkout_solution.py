

# noinspection PyUnusedLocal
# skus = unicode string
# import re

def multi_offers(basket, base_item, offer_qty): # b, A, [5,3]

    curr_qty = basket.get(base_item, 0)

    for q in offer_qty:
        sp_item = str(q) + base_item # 5A
        sp_item_qty = int(curr_qty/q)
        basket[sp_item] = sp_item_qty
        curr_qty = curr_qty - (sp_item_qty * q)
    basket[base_item] = curr_qty


def other_item_free(basket, base_item, qty, free_item):
    free_items_qty = int(basket.get(base_item, 0) / qty)
    basket[free_item] = max(basket.get(free_item, 0) - free_items_qty, 0)

import sys

def min_postive(k):
    min_elem = sys.maxsize
    for e in k:
        if min_elem > e > 0:
            min_elem = e
    return min_elem


def group_offer(group_qts): # static
    # [50 7 8 6 34]

    tot_items = sum(group_qts)
    tot_groups = int(tot_items/3)
    return tot_groups


    # if group_qts.count(0) >= 3:
    #     return 0
    #
    # min_num = min_postive(group_qts)
    #
    # counter = 0
    # for i in range(5):
    #     if group_qts[i] != 0 :
    #         group_qts[i] -= min_num
    #         counter += 1
    #
    #     if counter == 3:
    #         break
    # return min_num + group_offer(group_qts)



def checkout(skus):

    if skus == "":
        return 0

    if skus is None or type(skus) is not str:
        return -1

    skus = list(skus)

    sku_qtys = {}
    for item in skus:
        # pattern = re.compile("[A-Z]]")
        # is_match = pattern.match(item)
        if item not in {"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"}:
            return -1
        sku_qtys[item] = sku_qtys.get(item, 0) + 1

    prices = {
        "5A": 200,
        "3A": 130,
        "2B": 45,
        "A": 50,
        "B": 30,
        "C": 20,
        "D": 15,
        "E": 40,
        "F": 10,
        "3F": 20,

        "G": 20,
        "H": 10,
        "5H": 45,
        "10H": 80,

        "I": 35,
        "J": 60,
        "K": 70,
        "2K": 120,
        "L": 90,
        "M": 15,
        "N": 40,
        "O": 10,
        "P": 50,
        "5P": 200,
        "Q": 30,
        "3Q": 80,
        "R": 50,
        "S": 20,
        "T": 20,
        "U": 40,
        "4U": 120,
        "V": 50,
        "2V": 90,
        "3V": 130,
        "W": 20,
        "X": 17,
        "Y": 20,
        "Z": 21,
        "Group": 45
    }

    other_item_free(sku_qtys, "E", 2, "B")
    other_item_free(sku_qtys, "N", 3, "M")
    other_item_free(sku_qtys, "R", 3, "Q")

    multi_offers(sku_qtys, "A", [5, 3])
    multi_offers(sku_qtys, "B", [2])
    multi_offers(sku_qtys, "F", [3])

    multi_offers(sku_qtys, "H", [10, 5])
    multi_offers(sku_qtys, "K", [2])
    multi_offers(sku_qtys, "P", [5])
    multi_offers(sku_qtys, "Q", [3])
    multi_offers(sku_qtys, "U", [4])
    multi_offers(sku_qtys, "V", [3, 2])

    group_qts = [sku_qtys.get("Z", 0), sku_qtys.get("S", 0), sku_qtys.get("T", 0), sku_qtys.get("Y", 0),
                 sku_qtys.get("X", 0)]

    num_groups = group_offer(group_qts)

    sku_qtys["Group"] = num_groups

    rem_items = sum(group_qts) % 3

    if rem_items != 0:
        z_list = ["Z"] * group_qts[0]
        s_list = ["S"] * group_qts[1]
        t_list = ["T"] * group_qts[2]
        y_list = ["Y"] * group_qts[3]
        x_list = ["X"] * group_qts[4]

        z_list.extend(s_list)
        z_list.extend(t_list)
        z_list.extend(y_list)
        z_list.extend(x_list)

        rems = z_list[-rem_items:]

        sku_qtys["Z"] = rems.count("Z")
        sku_qtys["S"] = rems.count("S")
        sku_qtys["T"] = rems.count("T")
        sku_qtys["Y"] = rems.count("Y")
        sku_qtys["X"] = rems.count("X")

    else:
        sku_qtys["Z"] = 0
        sku_qtys["S"] = 0
        sku_qtys["T"] = 0
        sku_qtys["Y"] = 0
        sku_qtys["X"] = 0

    total_val = 0
    for item in sku_qtys:
        total_val = total_val + (sku_qtys[item] * prices[item])

    return total_val



