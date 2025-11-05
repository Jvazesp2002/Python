from pickle import FALSE

import pytest
## Esta función verifica si una cadena es un palíndromo,
## ignorando mayúsculas, espacios y signos de puntuación.
def is_palindrome(s):
    normalized = ''.join(c.lower() for c in s if c.isalnum())
    return normalized == normalized[::-1]


## Pruebas parametrizadas para la función is_palindrome.
@pytest.mark.parametrize("maybe_palindrome, expected_result", [
    ("", True),
    ("a", True),
    ("Bob", True),
    ("Nunca par o impar", False),
    ("¿Ven las ocas a Dios?", False),
    ("abc", False),
    ("abab", False),
])
def test_is_palindrome(maybe_palindrome, expected_result):
    assert is_palindrome(maybe_palindrome) == expected_result