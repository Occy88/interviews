import re


def validate_skus(skus):
    """Ensure skus are a valid string [A-Z]
    Parameters
    ----------
    skus

    Returns
    -------

    """
    if skus == "":
        return
    pattern = "^[A-Z]+$"
    if not re.fullmatch(pattern, skus):
        raise TypeError(f"Expected {skus} to match {pattern}")


def choose_max(l1, l2):
    if not l1 and not l2:
        raise ValueError("Both Lists Empty")
    if not l1:
        return l2[0]
    if not l2:
        return l1[0]
    return max(l1[0], l2[0])
