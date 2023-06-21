from solutions.CHK import checkout_solution
import unittest

class TestSum(unittest.TestCase):

    def test_checkout_with_valid_input(self):
        self.assertEqual(checkout_solution.checkout("AAABCD"), 195)
        self.assertEqual(checkout_solution.checkout("AAAABBB"), 255)
        self.assertEqual(checkout_solution.checkout("A"), 50)
        self.assertEqual(checkout_solution.checkout("B"), 30)
        self.assertEqual(checkout_solution.checkout("ABAB"), 145)
        self.assertEqual(checkout_solution.checkout(""), 0)

        self.assertEqual(checkout_solution.checkout("AAAAA"), 200)
        self.assertEqual(checkout_solution.checkout("AAA"), 130)
        self.assertEqual(checkout_solution.checkout("AAAAABBAAAA"), 425)

        self.assertEqual(checkout_solution.checkout("EE"), 80)
        self.assertEqual(checkout_solution.checkout("EEEEEB"), 200)
        self.assertEqual(checkout_solution.checkout("EEEEE"), 200)
        self.assertEqual(checkout_solution.checkout("EEB"), 80)
        self.assertEqual(checkout_solution.checkout("EEEB"), 120)
        self.assertEqual(checkout_solution.checkout("EEEEBB"), 160)

        self.assertEqual(checkout_solution.checkout("F"), 10)
        self.assertEqual(checkout_solution.checkout("FF"), 20)
        self.assertEqual(checkout_solution.checkout("FFF"), 20)
        self.assertEqual(checkout_solution.checkout("FFFF"), 30)
        self.assertEqual(checkout_solution.checkout("FFFFF"), 40)
        self.assertEqual(checkout_solution.checkout("FFFFFF"), 40)

        self.assertEqual(checkout_solution.checkout("VVV"), 130)
        self.assertEqual(checkout_solution.checkout("VVVV"), 180)
        self.assertEqual(checkout_solution.checkout("VVVVV"), 220)

        # self.assertEqual(checkout_solution.checkout("XYZST"), 45 + 17 + 20)
        # self.assertEqual(checkout_solution.checkout("XXX"), 17 * 3)
        # self.assertEqual(checkout_solution.checkout("XXXSSTTZZZ"), 90 + 21 + (17*3))

        self.assertEqual(checkout_solution.checkout("SSS"), 45)
        self.assertEqual(checkout_solution.checkout("SSSZ"), 65)
        self.assertEqual(checkout_solution.checkout("ZZZ"), 45)
        self.assertEqual(checkout_solution.checkout("ZX"), 38)
        self.assertEqual(checkout_solution.checkout("ZZZX"), 45+17)
        self.assertEqual(checkout_solution.checkout("ZZZSSSX"), 90 + 17)
        self.assertEqual(checkout_solution.checkout("ZZZZ"), 45 + 21)


    def test_checkout_with_invalid_input(self):
        self.assertEqual(checkout_solution.checkout(None), -1)
        self.assertEqual(checkout_solution.checkout(1234), -1)

