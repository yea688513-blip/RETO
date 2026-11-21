"""Portal simulado de una aseguradora. NO MODIFICAR: es el mundo de afuera.

consultar(id_cuenta) devuelve un diccionario con el estado de la cuenta.
Puede lanzar:
  - CuentaNoEncontrada: el portal no conoce esa cuenta.
  - PortalNoDisponible: el portal no respondió esta vez (falla temporal).
"""
import json
from pathlib import Path

_RUTA = Path(__file__).with_name("respuestas.json")
_INTENTOS = {}
_INESTABLES = {"C-1007": 1}  # cuenta -> número de veces que el portal falla antes de responder


class PortalNoDisponible(Exception):
    """El portal no respondió. Puede funcionar si se vuelve a intentar."""


class CuentaNoEncontrada(Exception):
    """El portal no tiene registro de la cuenta."""


def consultar(id_cuenta: str) -> dict:
    _INTENTOS[id_cuenta] = _INTENTOS.get(id_cuenta, 0) + 1
    if _INTENTOS[id_cuenta] <= _INESTABLES.get(id_cuenta, 0):
        raise PortalNoDisponible(f"Tiempo de espera agotado consultando {id_cuenta}")
    cuentas = json.loads(_RUTA.read_text(encoding="utf-8"))["cuentas"]
    if id_cuenta not in cuentas:
        raise CuentaNoEncontrada(f"La cuenta {id_cuenta} no existe en el portal")
    return dict(cuentas[id_cuenta])
