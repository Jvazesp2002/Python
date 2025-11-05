import pytest
import requests
## Este fixture deshabilita las llamadas de red durante las pruebas.
## el autouse=True asegura que este fixture se aplique a todas las pruebas automáticamente.
@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())