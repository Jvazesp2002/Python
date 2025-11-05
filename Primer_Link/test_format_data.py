import pytest
from format_data import format_data_for_display, format_data_for_excel
## Este test verifica las funciones de formateo de datos para visualización y exportación a Excel.
@pytest.fixture
def example_people_data():
    return [
        {
            "given_name": "Jorge",
            "family_name": "Vazquez",
            "title": "Senior Software Engineer",
        },
        {
            "given_name": "Pedro",
            "family_name": "Perez",
            "title": "Project Manager",
        },
    ]
    
def test_format_data_for_display(example_people_data):
    assert format_data_for_display(example_people_data) == [
        "Jorge Vazquez: Senior Software Engineer",
        "Pedro Perez: Project Manager",
    ]

def test_format_data_for_excel(example_people_data):
    assert format_data_for_excel(example_people_data) == """given,family,title
Jorge,Vazquez,Senior Software Engineer
Pedro,Perez,Project Manager"""