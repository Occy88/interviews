from solutions.CHK import checkout_solution


class TestCheckout:
    def test_checkout(self):
        assert checkout_solution.checkout("AAAB") == 160

    def test_checkout_incorrect_item(self):
        assert checkout_solution.checkout("AAaB") == -1

    def test_checkout_2E_and_B(self):
        assert checkout_solution.checkout("EEB") == 80

    def test_checkout_4E_and_3B(self):
        assert checkout_solution.checkout("EEEEBBB") == 190

    def test_checkout_E(self):
        assert checkout_solution.checkout("E") == 40

    def test_checkout_5A(self):
        assert checkout_solution.checkout("AAAAA") == 200

    def test_checkout_8A(self):
        assert checkout_solution.checkout("A" * 8) == 330

    def test_checkout_9A(self):
        assert checkout_solution.checkout("A" * 9) == 380

    def test_checkout_F(self):
        assert checkout_solution.checkout("F") == 10

    def test_checkout_2F(self):
        assert checkout_solution.checkout("FF") == 20

    def test_checkout_3F(self):
        assert checkout_solution.checkout("FFF") == 20

    def test_checkout_4F(self):
        assert checkout_solution.checkout("FFFF") == 30

    def test_checkout_6F(self):
        assert checkout_solution.checkout("F" * 6) == 40

    def test_checkout_9F(self):
        assert checkout_solution.checkout("F" * 9) == 60

    def test_checkout_r4(self):
        assert checkout_solution.checkout("AABBQQQRR") == 325
        assert checkout_solution.checkout("AAABBQQQRRR") == 385
        assert checkout_solution.checkout("AAAAABBQQQRRR") == 455
        assert checkout_solution.checkout("UUU") == 120
        assert checkout_solution.checkout("NNNM") == 120

    def test_checkout_r5(self):
        assert checkout_solution.checkout("STX") == 45
        assert checkout_solution.checkout("STXS") == 62
        assert checkout_solution.checkout("STAABBQQQRRXS") == 387

    def test_checkout_r5_1(self):
        assert checkout_solution.checkout("ABCDEFGHIJKLMNOPQRSTUVW") == 795
        assert checkout_solution.checkout("CXYZYZC") == 122