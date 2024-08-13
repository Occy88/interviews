from challenges.supermarket.checkout import checkout


def test_checkout():
    assert 100 == checkout('AA')
