import pytest


@pytest.fixture
def greeting_template():
    return "Hello, {}!"
