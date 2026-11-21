"""Bot de seguimiento de radicacion de cuentas."""
import csv
from datetime import datetime
from pathlib import Path

from portal.portal import CuentaNoEncontrada, PortalNoDisponible, consultar

ENTRADA = Path("datos/cuentas.csv")
SALIDA = Path("salida/resultados.csv")
EXCEPCIONES = Path("salida/excepciones.csv")
INTENTOS_MAXIMOS = 3  # Primer intento y hasta dos reintentos.


def leer_cuentas(ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def convertir_valor(texto):
    # El origen mezcla valores simples y formato colombiano con puntos de miles.
    return int(texto.replace(".", "").replace(",", "").strip())


def consultar_con_reintentos(id_cuenta):
    for intento in range(INTENTOS_MAXIMOS):
        try:
            return consultar(id_cuenta)
        except PortalNoDisponible:
            if intento == INTENTOS_MAXIMOS - 1:
                raise


def guardar_csv(ruta, columnas, filas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)


def procesar():
    resultados = []
    excepciones = []

    for cuenta in leer_cuentas(ENTRADA):
        id_cuenta = cuenta.get("id_cuenta", "").strip()
        try:
            valor = convertir_valor(cuenta["valor"])
            if valor <= 0:
                raise ValueError("el valor de la cuenta debe ser mayor que cero")

            respuesta = consultar_con_reintentos(id_cuenta)
            estado = respuesta["estado_radicacion"]
            fecha = respuesta.get("fecha_radicacion")

            dias = ""
            if fecha:
                fecha_servicio = datetime.strptime(cuenta["fecha_servicio"], "%d/%m/%Y").date()
                fecha_radicacion = datetime.strptime(fecha, "%Y-%m-%d").date()
                dias = (fecha_radicacion - fecha_servicio).days

            resultados.append({
                "id_cuenta": id_cuenta,
                "aseguradora": cuenta["aseguradora"],
                "valor": valor,
                "estado": estado,
                "dias_hasta_radicar": dias,
            })
        except CuentaNoEncontrada:
            excepciones.append({"id_cuenta": id_cuenta, "motivo": "La cuenta no existe en el portal."})
        except PortalNoDisponible:
            excepciones.append({"id_cuenta": id_cuenta, "motivo": "El portal no respondió tras 3 intentos (2 reintentos)."})
        except (KeyError, ValueError, TypeError) as error:
            excepciones.append({"id_cuenta": id_cuenta, "motivo": f"Datos de cuenta inválidos: {error}."})

    guardar_csv(SALIDA, ["id_cuenta", "aseguradora", "valor", "estado", "dias_hasta_radicar"], resultados)
    guardar_csv(EXCEPCIONES, ["id_cuenta", "motivo"], excepciones)
    print(f"Listo: {len(resultados)} cuentas procesadas; {len(excepciones)} en excepciones")


if __name__ == "__main__":
    procesar()
