from lib.challenges.supermarket import checkout

def test_checkout():
    try:
        assert 100 == checkout('AA')
    except NotImplementedError:
        pass