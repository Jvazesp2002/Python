from unittest.mock import patch

import pytest
from pytest_unordered import unordered

from hashtable import DELETED, HashTable


# Fixture que devuelve una tabla con 3 entradas de ejemplo. Usada por
# muchos tests para evitar duplicación de código.
@pytest.fixture
def hash_table():
    sample_data = HashTable(capacity=100)
    sample_data["hola"] = "hello"
    sample_data[98.6] = 37
    sample_data[False] = True
    return sample_data


# Verifica que se puede crear una instancia con capacidad explícita.
def test_should_create_hashtable():
    assert HashTable(capacity=100) is not None


# Verifica que la capacidad por defecto sea 8.
def test_should_create_hashtable_with_default_capacity():
    assert HashTable().capacity == 8


# Una tabla nueva y vacía debe reportar longitud 0.
def test_should_report_length_of_empty_hash_table():
    assert len(HashTable(capacity=100)) == 0


# El fixture con 3 entradas debe reportar longitud 3.
def test_should_report_length(hash_table):
    assert len(hash_table) == 3


# Comprobación de que la propiedad capacity devuelve el valor correcto
def test_should_report_capacity_of_empty_hash_table():
    assert HashTable(capacity=100).capacity == 100


# El fixture tambien debe exponer la capacity correcta.
def test_should_report_capacity(hash_table):
    assert hash_table.capacity == 100


# Al crear una tabla con capacidad 3, los slots internos deben estar vacíos.
def test_should_create_empty_pair_slots():
    assert HashTable(capacity=3)._slots == [None, None, None]


# Inserción básica de pares clave:valor y comprobación en pairs y len.
def test_should_insert_key_value_pairs():
    hash_table = HashTable(capacity=100)

    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    assert ("hola", "hello") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (False, True) in hash_table.pairs

    assert len(hash_table) == 3


# Al crear una tabla, su lista de valores no debe contener None por defecto.
def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=100).values


# Se puede insertar un valor None y aparecerá en pairs.
def test_should_insert_none_value():
    hash_table = HashTable(capacity=100)
    hash_table["key"] = None
    assert ("key", None) in hash_table.pairs


# Búsqueda correcta por clave para los tipos insertados.
def test_should_find_value_by_key(hash_table):
    assert hash_table["hola"] == "hello"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True


# Intentar acceder a una clave inexistente debe lanzar KeyError.
def test_should_raise_error_on_missing_key():
    hash_table = HashTable(capacity=100)
    with pytest.raises(KeyError) as exception_info:
        hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


# El operador in debe detectar claves existentes.
def test_should_find_key(hash_table):
    assert "hola" in hash_table


# Claves ausentes no deben encontrarse.
def test_should_not_find_key(hash_table):
    assert "missing_key" not in hash_table


# get debe devolver el valor si existe.
def test_should_get_value(hash_table):
    assert hash_table.get("hola") == "hello"


# get sin default devuelve None cuando falta la clave.
def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key") is None


# get con default devuelve el valor por defecto si falta la clave.
def test_should_get_default_value_when_missing_key(hash_table):
    assert hash_table.get("missing_key", "default") == "default"


# get con default cuando la clave existe devuelve el valor real.
def test_should_get_value_with_default(hash_table):
    assert hash_table.get("hola", "default") == "hello"


# Borrar una clave debe quitarla de pairs y reducir la longitud.
def test_should_delete_key_value_pair(hash_table):
    assert "hola" in hash_table
    assert ("hola", "hello") in hash_table.pairs
    assert len(hash_table) == 3

    del hash_table["hola"]

    assert "hola" not in hash_table
    assert ("hola", "hello") not in hash_table.pairs
    assert len(hash_table) == 2


# Borrar una clave inexistente debe lanzar KeyError con el nombre de la clave.
def test_should_raise_key_error_when_deleting(hash_table):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


# Actualizar (set) una clave existente debe cambiar su valor y mantener
# las demás entradas intactas.
def test_should_update_value(hash_table):
    assert hash_table["hola"] == "hello"

    hash_table["hola"] = "hallo"

    assert hash_table["hola"] == "hallo"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True
    assert len(hash_table) == 3


# pairs debe devolver exactamente el conjunto de pares presentes.
def test_should_return_pairs(hash_table):
    assert hash_table.pairs == {
        ("hola", "hello"),
        (98.6, 37),
        (False, True),
    }


# Una tabla vacía no tiene pares.
def test_should_get_pairs_of_empty_hash_table():
    assert HashTable(capacity=100).pairs == set()


# Verifica que pairs devuelve una copia (no el mismo objeto).
def test_should_return_copy_of_pairs(hash_table):
    assert hash_table.pairs is not hash_table.pairs


# pairs no debe incluir valores None (slots vacíos) ni marcadores DELETED.
def test_should_not_include_blank_pairs(hash_table):
    assert None not in hash_table.pairs


# Los valores duplicados se mantienen y aparecen en values.
def test_should_return_duplicate_values():
    hash_table = HashTable(capacity=100)
    hash_table["Alice"] = 24
    hash_table["Bob"] = 42
    hash_table["Joe"] = 42
    assert [24, 42, 42] == sorted(hash_table.values)


# values debe contener los valores del fixture, sin orden garantizado.
def test_should_get_values(hash_table):
    assert unordered(hash_table.values) == ["hello", 37, True]


# values vacío cuando no hay entradas.
def test_should_get_values_of_empty_hash_table():
    assert HashTable(capacity=100).values == []


# values devuelve una copia (no el mismo objeto).
def test_should_return_copy_of_values(hash_table):
    assert hash_table.values is not hash_table.values


# keys debe devolver el conjunto de claves presentes.
def test_should_get_keys(hash_table):
    assert hash_table.keys == {"hola", 98.6, False}


# keys vacío cuando no hay entradas.
def test_should_get_keys_of_empty_hash_table():
    assert HashTable(capacity=100).keys == set()


# keys devuelve una copia (no el mismo objeto).
def test_should_return_copy_of_keys(hash_table):
    assert hash_table.keys is not hash_table.keys


# Converter pairs a dict produce un dict coherente con keys/values.
def test_should_convert_to_dict(hash_table):
    dictionary = dict(hash_table.pairs)
    assert set(dictionary.keys()) == hash_table.keys
    assert set(dictionary.items()) == hash_table.pairs
    assert list(dictionary.values()) == unordered(hash_table.values)


# No se permite crear una tabla con capacidad 0.
def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)


# Ni con capacidad negativa.
def test_should_not_create_hashtable_with_negative_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=-100)


# Iteración sobre keys: cada clave debe ser una de las insertadas.
def test_should_iterate_over_keys(hash_table):
    for key in hash_table.keys:
        assert key in ("hola", 98.6, False)


# Iteración sobre values: cada valor debe ser uno de los insertados.
def test_should_iterate_over_values(hash_table):
    for value in hash_table.values:
        assert value in ("hello", 37, True)


# Iteración sobre pairs: cada par debe corresponder a claves y valores presentes.
def test_should_iterate_over_pairs(hash_table):
    for key, value in hash_table.pairs:
        assert key in hash_table.keys
        assert value in hash_table.values


# Iteración directa sobre la instancia debe producir claves.
def test_should_iterate_over_instance(hash_table):
    for key in hash_table:
        assert key in ("hola", 98.6, False)


# str devuelve una representación de estilo dict (orden no garantizado).
def test_should_use_dict_literal_for_str(hash_table):
    assert str(hash_table) in {
        "{'hola': 'hello', 98.6: 37, False: True}",
        "{'hola': 'hello', False: True, 98.6: 37}",
        "{98.6: 37, 'hola': 'hello', False: True}",
        "{98.6: 37, False: True, 'hola': 'hello'}",
        "{False: True, 'hola': 'hello', 98.6: 37}",
        "{False: True, 98.6: 37, 'hola': 'hello'}",
    }


# from_dict debe crear una tabla con las mismas entradas y capacidad
def test_should_create_hashtable_from_dict(hash_table):
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    hash_table = HashTable.from_dict(dictionary)

    assert hash_table.capacity == len(dictionary)
    assert hash_table.keys == set(dictionary.keys())
    assert hash_table.pairs == set(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())


# from_dict permite pasar una capacidad personalizada.
def test_should_create_hashtable_from_dict_with_custom_capacity(hash_table):
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    hash_table = HashTable.from_dict(dictionary, capacity=100)

    assert hash_table.capacity == 100
    assert hash_table.keys == set(dictionary.keys())
    assert hash_table.pairs == set(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())


# repr tiene una forma canónica usada por los tests.
def test_should_have_canonical_string_representation(hash_table):
    assert repr(hash_table) in {
        "HashTable.from_dict({'hola': 'hello', 98.6: 37, False: True})",
        "HashTable.from_dict({'hola': 'hello', False: True, 98.6: 37})",
        "HashTable.from_dict({98.6: 37, 'hola': 'hello', False: True})",
        "HashTable.from_dict({98.6: 37, False: True, 'hola': 'hello'})",
        "HashTable.from_dict({False: True, 'hola': 'hello', 98.6: 37})",
        "HashTable.from_dict({False: True, 98.6: 37, 'hola': 'hello'})",
    }


# Igualdad con uno mismo debe ser True.
def test_should_compare_equal_to_itself(hash_table):
    assert hash_table == hash_table


# Copia devuelve una tabla equivalente pero distinta.
def test_should_compare_equal_to_copy(hash_table):
    assert hash_table is not hash_table.copy()
    assert hash_table == hash_table.copy()


# Igualdad independiente del orden de inserción.
def test_should_compare_equal_different_key_value_order(hash_table):
    h1 = HashTable.from_dict({"a": 1, "b": 2, "c": 3})
    h2 = HashTable.from_dict({"b": 2, "a": 1, "c": 3})
    assert h1 == h2


# Comparación desigual con contenido distinto.
def test_should_compare_unequal(hash_table):
    other = HashTable.from_dict({"different": "value"})
    assert hash_table != other


# Comparación con otro tipo de datos debe ser False.
def test_should_compare_unequal_another_data_type(hash_table):
    assert hash_table != 42


# copy preserva keys, values, pairs y capacity.
def test_should_copy_keys_values_pairs_capacity(hash_table):
    copy = hash_table.copy()
    assert copy is not hash_table
    assert set(hash_table.keys) == set(copy.keys)
    assert set(hash_table.pairs) == set(copy.pairs)
    assert unordered(hash_table.values) == copy.values
    assert hash_table.capacity == copy.capacity


# Igualdad no depende de la capacidad interna.
def test_should_compare_equal_different_capacity():
    data = {"a": 1, "b": 2, "c": 3}
    h1 = HashTable.from_dict(data, capacity=50)
    h2 = HashTable.from_dict(data, capacity=100)
    assert h1 == h2


# Forzamos hash constante para simular colisiones y verificar el comportamiento
@patch("builtins.hash", return_value=24)
def test_should_detect_and_resolve_hash_collisions(mock_hash):
    hash_table = HashTable(capacity=100)
    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    assert len(hash_table) == 3

    # Comprobamos que las tuplas están en los índices esperados según el parche.
    assert hash_table._slots[24] == ("hola", "hello")
    assert hash_table._slots[25] == (98.6, 37)
    assert hash_table._slots[26] == (False, True)


# Forzamos side_effects en hash para comprobar wrapping del índice.
@patch("builtins.hash", side_effect=[2, 1, 1])
def test_should_wrap_index_around_when_collides(mock_hash):
    hash_table = HashTable(capacity=3)
    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    assert len(hash_table) == 3

    assert hash_table._slots[2] == ("hola", "hello")
    assert hash_table._slots[1] == (98.6, 37)
    assert hash_table._slots[0] == (False, True)


# No debemos sobrescribir una ranura marcada DELETED cuando insertamos
def test_should_not_overwrite_deleted(hash_table):
    del hash_table["hola"]
    deleted_slot = hash_table._slots.index(DELETED)

    assert len(hash_table) == 2
    assert DELETED in hash_table._slots

    with patch("builtins.hash", return_value=deleted_slot):
        hash_table["gracias"] = "thank you"

    # Aún debe haber al menos un DELETED en los slots (no se sobrescribe)
    assert len(hash_table) == 3
    assert DELETED in hash_table._slots


# Insertar una entrada adicional en una tabla pequeña debe forzar
# el doblado de la capacidad y preservar todos los pares.
def test_should_double_capacity():
    hash_table = HashTable(capacity=3)
    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    hash_table["gracias"] = "thank you"

    assert len(hash_table) == 4
    assert hash_table.capacity == 6
    assert dict(hash_table.pairs) == {
        "hola": "hello",
        98.6: 37,
        False: True,
        "gracias": "thank you",
    }


# Cuando todas las claves colisionan por hash, la lectura debe seguir
# devolviendo los valores correctos.
@patch("builtins.hash", return_value=24)
def test_should_get_collided_values(mock_hash):
    hash_table = HashTable(capacity=3)
    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    assert len(hash_table) == 3

    assert hash_table["hola"] == "hello"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True


# Simula varios hashes para insertar y borrar y comprobar que las búsquedas
# ignoran marcadores DELETED y siguen encontrando otras claves.
@patch("builtins.hash", side_effect=[0, 1, 2, 0, 1, 0])
def test_should_not_get_deleted_values(mock_hash):
    hash_table = HashTable(capacity=3)
    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    del hash_table["hola"]
    del hash_table[98.6]

    assert hash_table[False] is True


# Al borrar un par concreto, su slot interno pasa a ser DELETED.
def test_should_mark_as_deleted(hash_table):
    index = hash_table._slots.index(("hola", "hello"))
    del hash_table["hola"]
    assert hash_table._slots[index] is DELETED


# pairs no debe incluir pares eliminados.
def test_pairs_should_not_contain_deleted(hash_table):
    del hash_table["hola"]
    del hash_table[98.6]

    assert hash_table.pairs == {(False, True)}