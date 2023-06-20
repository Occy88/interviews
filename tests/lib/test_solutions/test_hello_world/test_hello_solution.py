import pytest
from solutions.hello_world import hello_world


class TestHelloWorld:
    def test_hello_correct_format(self, greeting_template):
        # ARRANGE
        name = "John"
        # ACT
        result = hello_world.hello(name)
        # ASSERT
        assert result == greeting_template.format(name)

    def test_hello_raises_type_error(self, greeting_template):
        # ARRANGE
        name = 42
        # ACT
        # ASSERT
        with pytest.raises(TypeError):
            hello_world.hello(name)
