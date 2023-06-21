import pytest

from solutions.CHK import checkout_solution

def test_does_individual_checkout() -> None:
    assert checkout_solution.checkout("A") == 50
    assert checkout_solution.checkout("B") == 30
    assert checkout_solution.checkout("C") == 20
    assert checkout_solution.checkout("D") == 15

def test_does_checkout_with_multiple_items_no_discounts() -> None:
    assert checkout_solution.checkout("ABCD") == 115

def test_does_checkout_with_multiple_items_with_discounts() -> None:
    assert checkout_solution.checkout("AAA") == 130
    assert checkout_solution.checkout("BB") == 45
    assert checkout_solution.checkout("AAAAAA") == 260
    assert checkout_solution.checkout("AAAAA") == 230
    assert checkout_solution.checkout("AAAA") == 180
    assert checkout_solution.checkout("BBBB") == 90
    assert checkout_solution.checkout("BBB") == 75
    assert checkout_solution.checkout("BBBAA") == 175

def test_handle_cross_referenced_discounts() -> None:
    assert checkout_solution.checkout("EEB") == 80
    assert checkout_solution.checkout("EEEB") == 120
    assert checkout_solution.checkout("EEEEBB") == 160
    assert checkout_solution.checkout("BEBEEE") == 160

def test_does_checkout_with_invalid_items() -> None:
    assert checkout_solution.checkout("Z") == -1