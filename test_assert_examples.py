## Conversor de minusculas a mayusculas, reversor de listas y generador de numeros primos con tests hechos con assert.
def test_uppercase():
    assert "ruidos fuertes".upper() == "RUIDOS FUERTES"

def test_reversed():
    assert list(reversed([1, 2, 3, 4])) == [4, 3, 2, 1]

def test_some_primes():
    assert 37 in {
        num
        for num in range(2, 50)
        if not any(num % div == 0 for div in range(2, num))
    }