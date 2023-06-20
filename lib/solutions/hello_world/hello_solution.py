# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name: str) -> str:
    """Returns greeting for friend_name

    Parameters
    ----------
    friend_name: Name to greet

    Returns
    -------

    """
    if not isinstance(friend_name, str):
        raise TypeError(
            f"Type of {friend_name} is {type(friend_name)}, Expected type: {str}"
        )
    greeting_template = "Hello, {}!"
    return greeting_template.format(friend_name)
