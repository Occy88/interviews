from enum import Enum

from .data_models import (
    Basket,
    BuyAnyNItemsForYDiscount,
    BuyNForYDiscount,
    BuyNGetYFreeDiscount,
    Item,
)


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


DISCOUNTS = [
    # | A    | 50    | 3A for 130, 5A for 200 |
    BuyNForYDiscount(Items.A.value, 3, 130),
    BuyNForYDiscount(Items.A.value, 5, 200),
    # | B    | 30    | 2B for 45              |
    BuyNForYDiscount(Items.B.value, 2, 45),
    # | E    | 40    | 2E get one B free      |
    BuyNGetYFreeDiscount(Items.E.value, 2, Items.B.value, 1),
    # | F    | 10    | 2F get one F free      |
    BuyNGetYFreeDiscount(Items.F.value, 2, Items.F.value, 1),
    #   | H    | 10    | 5H for 45, 10H for 80  |
    BuyNForYDiscount(Items.H.value, 5, 45),
    BuyNForYDiscount(Items.H.value, 10, 80),
    #   | K    | 80    | 2K for 120             |
    BuyNForYDiscount(Items.K.value, 2, 120),
    #    | N    | 40    | 3N get one M free      |
    BuyNGetYFreeDiscount(Items.N.value, 3, Items.M.value, 1),
    #     | P    | 50    | 5P for 200             |
    BuyNForYDiscount(Items.P.value, 5, 200),
    # | Q    | 30    | 3Q for 80              |
    BuyNForYDiscount(Items.Q.value, 3, 80),
    # | R    | 50    | 3R get one Q free      |
    BuyNGetYFreeDiscount(Items.R.value, 3, Items.Q.value, 1),
    # | U    | 40    | 3U get one U free      |
    BuyNGetYFreeDiscount(Items.U.value, 3, Items.U.value, 1),
    # | V    | 50    | 2V for 90, 3V for 130  |
    BuyNForYDiscount(Items.V.value, 2, 90),
    BuyNForYDiscount(Items.V.value, 3, 130),
    # | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
    BuyAnyNItemsForYDiscount(Basket("STXYZ"), 3, 45),
]
