# Proyecto de ejercicios Python

Este repositorio contiene ejercicios y pruebas en dos carpetas principales:

- `Primer_Link` — serie de ejercicios y ejemplos con pytest y unittest.
- `Segundo_Link` — implementación de una tabla hash con pruebas que verifican su comportamiento.

A continuación encontrarás una descripción de cada carpeta, los archivos más relevantes y cómo ejecutar las pruebas en Windows PowerShell.

## Estructura y contenido

### Primer_Link
Contiene ejemplos y tests destinados a practicar pytest, fixtures y aserciones.
Archivos principales:

- `conftest.py` — configuración de pytest y fixtures comunes (si aplica).
- `fixture_demo.py` — demostración de fixtures (utilizado por algunos tests).
- `format_data.py` — funciones para formatear/dar formato a datos (ejercicios de transformación).
- `test_assert_examples.py` — ejemplos de aserciones con pytest.
- `test_format_data.py` — tests que verifican la funcionalidad de `format_data.py`.
- `test_palindrome.py` — tests para comprobar funciones relacionadas con palíndromos.
- `test_with_unittest.py` — tests escritos con el framework `unittest` (compatibles con `pytest` si se desea).
- `test_with-pytest.py` — tests escritos con pytest.

Objetivo: practicar cómo escribir tests con pytest, usar fixtures, y comprobar distintos estilos de assertions.

### Segundo_Link
Implementación y pruebas de una estructura de datos simple (HashTable).
Archivos principales:

- `hashtable.py` — implementación de `HashTable` usando sondeo lineal (open addressing). Incluye:
  - Inserción, acceso y borrado de claves (métodos especiales: `__setitem__`, `__getitem__`, `__delitem__`).
  - Manejo de marcadores `DELETED` para eliminaciones.
  - Redimensionado y rehash automático cuando la tabla se llena.
  - Propiedades útiles: `pairs`, `keys`, `values`, `capacity`.

- `test_hashtable.py` — suite de pruebas que valida la implementación. Incluye tests para:
  - Inserción y lectura de valores.
  - Borrado y comprobación de marcadores `DELETED`.
  - Resolución de colisiones y wrapping del índice.
  - Redimensionado (doblar la capacidad) y preservación de pares.
  - Igualdad, copia y representación en string.

Nota: los tests usan `pytest` y el plugin `pytest_unordered` en algunos lugares para comparar colecciones sin importar el orden.

## Requisitos

- Python 3.8+ (cualquier versión moderna de Python 3 funciona).
- Recomendado: crear un entorno virtual para instalar dependencias de testing.

Dependencias (sólo para ejecutar tests):

- pytest
- pytest-unordered

## Instrucciones rápidas (PowerShell)

1. Abrir PowerShell y situarse en la carpeta `Python` del proyecto:

```powershell
cd "c:\Users\JVE\OneDrive - Fundación Universitaria San Pablo CEU\Escritorio\Puesta en Produccion\Python"
```

2. (Opcional pero recomendado) Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Actualizar pip e instalar las dependencias de test:

```powershell
python -m pip install --upgrade pip
pip install pytest pytest-unordered
```

4. Ejecutar los tests de una carpeta concreta:

```powershell
# Ejecutar todos los tests en Primer_Link
pytest Primer_Link -q

# Ejecutar todos los tests en Segundo_Link
pytest Segundo_Link -q
```

5. Ejecutar un test específico (por ruta o por nombre):

```powershell
pytest Segundo_Link/test_hashtable.py::test_should_double_capacity -q
```

6. También puedes ejecutar `unittest` directamente (si lo prefieres):

```powershell
python -m unittest discover -v Primer_Link
```

## Notas y recomendaciones

- Los tests en `Segundo_Link` parchean (`patch`) la función `hash` en algunos casos para forzar colisiones y comprobar el comportamiento — esto es intencional y forma parte de las pruebas.
- `pytest_unordered` se utiliza en `test_hashtable.py` para comparar listas/colecciones sin depender del orden. Si no quieres instalarlo, puedes adaptar los tests o comparar conjuntos en lugar de listas ordenadas.
- Si vas a modificar `hashtable.py`, ejecuta primero los tests para verificar que todo sigue funcionando.

## Problemas comunes

- Si algún test falla tras editar código, revisa los casos donde se parchea `hash` — los tests dependen de un comportamiento determinista en esos escenarios.
- Si alguna dependencia falta, instala `pytest` y `pytest-unordered` con `pip` como se indica arriba.
