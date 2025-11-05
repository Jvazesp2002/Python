from typing import Any, NamedTuple

# Objeto marcador usado internamente para señalar una ranura eliminada.
# Usamos un objeto único para evitar colisiones con claves/valores del usuario.
DELETED = object()


# Par inmutable simple para almacenar tuplas (clave, valor) en los slots.
class Pair(NamedTuple):
    key: Any
    value: Any


class HashTable:
    # Construye una HashTable a partir de un diccionario plano. capacity
    # es opcional y sobreescribe el tamaño por defecto (longitud del dict).
    @classmethod
    def from_dict(cls, dictionary, capacity=None):
        hash_table = cls(capacity or len(dictionary))
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table

    # Crea una tabla hash con una capacidad inicial (8 por defecto).
    # La capacidad debe ser un número positivo.
    def __init__(self, capacity=8):
        if capacity < 1:
            raise ValueError("Capacity must be a positive number")
        # Array interno de slots; cada slot puede ser None, DELETED o Pair.
        self._slots = capacity * [None]

    # Número de pares almacenados (excluye marcadores DELETED).
    def __len__(self):
        return len(self.pairs)

    # Itera sobre las claves; permite `for k in hashtable:`.
    def __iter__(self):
        yield from self.keys

    # Elimina una clave de la tabla usando sondeo lineal (open addressing).
    # Marca la ranura como DELETED para preservar las cadenas de sondeo.
    def __delitem__(self, key):
        for index, pair in self._probe(key):
            if pair is None:
                # Se alcanzó una ranura vacía: la clave no está presente.
                raise KeyError(key)
            if pair is DELETED:
                # Omitir marcadores eliminados durante la búsqueda.
                continue
            if pair.key == key:
                # Marcar la ranura como eliminada y salir.
                self._slots[index] = DELETED
                break
        else:
            # Se terminó el sondeo sin encontrar la clave.
            raise KeyError(key)

    # Inserta o actualiza un par clave/valor. Si no se encuentra ranura
    # disponible (tabla al límite), redimensiona y rehace el rehash.
    def __setitem__(self, key, value):
        for index, pair in self._probe(key):
            if pair is DELETED:
                # No sobrescribimos inmediatamente un marcador DELETED; se
                # sigue sondeando para preservar la búsqueda de otras claves.
                continue
            if pair is None or pair.key == key:
                # Ranura vacía o actualización de la misma clave.
                self._slots[index] = Pair(key, value)
                break
        else:
            # No se encontró ranura -> duplicar capacidad y reintentar.
            self._resize_and_rehash()
            self[key] = value

    # Recupera un valor por clave usando sondeo; lanza KeyError si falta.
    def __getitem__(self, key):
        for _, pair in self._probe(key):
            if pair is None:
                # Ranura vacía -> clave no presente.
                raise KeyError(key)
            if pair is DELETED:
                # Omitir marcadores eliminados y continuar buscando.
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    # Operador de membresía (in). Mapea KeyError a False.
    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    # Igualdad basada en el conjunto de pares (la capacidad y el orden no
    # afectan la igualdad, según las pruebas).
    def __eq__(self, other):
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return set(self.pairs) == set(other.pairs)

    # Representación en string similar a un literal dict (el orden no está garantizado).
    def __str__(self):
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    # Repr canónico que utiliza el factory `from_dict` para las pruebas.
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"

    # Devuelve una copia superficial preservando la capacidad.
    def copy(self):
        return HashTable.from_dict(dict(self.pairs), self.capacity)

    # get segura que devuelve default si la clave no existe.
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    # Conjunto de pares (clave, valor) presentes actualmente, omitiendo
    # ranuras vacías y marcadores DELETED.
    @property
    def pairs(self):
        return {pair for pair in self._slots if pair not in (None, DELETED)}

    # Lista de valores presentes en la tabla. Devuelve una nueva lista.
    @property
    def values(self):
        return [pair.value for pair in self.pairs]

    # Conjunto de claves presentes en la tabla. Devuelve un nuevo set.
    @property
    def keys(self):
        return {pair.key for pair in self.pairs}

    # Capacidad actual (número de ranuras).
    @property
    def capacity(self):
        return len(self._slots)

    # Índice primario: hash módulo capacidad.
    def _index(self, key):
        return hash(key) % self.capacity

    # Generador de sondeo lineal: produce (índice, valor_slot) empezando
    # en el índice hasheado y envolviendo al final de la tabla.
    def _probe(self, key):
        index = self._index(key)
        for _ in range(self.capacity):
            yield index, self._slots[index]
            index = (index + 1) % self.capacity

    # Duplicar la capacidad y reinsertar todos los pares presentes. Los
    # marcadores DELETED no se copian al nuevo arreglo.
    def _resize_and_rehash(self):
        copy = HashTable(capacity=self.capacity * 2)
        for key, value in self.pairs:
            copy[key] = value
        self._slots = copy._slots