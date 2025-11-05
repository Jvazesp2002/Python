import pytest

## Ejemplo de uso de fixtures en pytest
@pytest.fixture
def example_fixture():
    return 1

def test_with_fixture(example_fixture):
    assert example_fixture == 1