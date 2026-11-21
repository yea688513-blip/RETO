"""Corre el bot y revisa la salida. NO MODIFICAR."""
import csv
import subprocess
import sys
from pathlib import Path

ESPERADO = {
    "C-1001": {"aseguradora": "Aseguradora Norte", "valor": "1250000", "estado": "radicada", "dias_hasta_radicar": "7"},
    "C-1002": {"aseguradora": "Aseguradora Sur", "valor": "845000", "estado": "radicada", "dias_hasta_radicar": "15"},
    "C-1003": {"aseguradora": "Aseguradora Norte", "valor": "1320500", "estado": "en_revision", "dias_hasta_radicar": ""},
    "C-1004": {"aseguradora": "Aseguradora Centro", "valor": "410000", "estado": "radicada", "dias_hasta_radicar": "5"},
    "C-1007": {"aseguradora": "Aseguradora Centro", "valor": "780000", "estado": "radicada", "dias_hasta_radicar": "2"},
    "C-1008": {"aseguradora": "Aseguradora Sur", "valor": "560000", "estado": "devuelta", "dias_hasta_radicar": "6"},
}
EXCEPCIONES_ESPERADAS = {"C-1005", "C-1006"}

problemas = []


def leer(ruta):
    if not ruta.exists():
        problemas.append(f"No existe {ruta}")
        return []
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


for vieja in (Path("salida/resultados.csv"), Path("salida/excepciones.csv")):
    if vieja.exists():
        vieja.unlink()

corrida = subprocess.run([sys.executable, "bot.py"], capture_output=True, text=True)
if corrida.returncode != 0:
    print("✗ El bot terminó con error:\n")
    print(corrida.stderr.strip()[-1500:])
    sys.exit(1)
print("✓ El bot corrió de punta a punta")

resultados = {fila.get("id_cuenta"): fila for fila in leer(Path("salida/resultados.csv"))}
for id_cuenta, esperado in ESPERADO.items():
    fila = resultados.get(id_cuenta)
    if fila is None:
        problemas.append(f"{id_cuenta} no está en resultados.csv")
        continue
    for campo, valor in esperado.items():
        if str(fila.get(campo, "")).strip() != valor:
            problemas.append(f"{id_cuenta} · {campo}: se esperaba «{valor}» y llegó «{fila.get(campo)}»")
sobrantes = set(resultados) - set(ESPERADO)
if sobrantes:
    problemas.append(f"Cuentas en resultados.csv que deberían ser excepciones: {', '.join(sorted(sobrantes))}")

excepciones = leer(Path("salida/excepciones.csv"))
ids_exc = {fila.get("id_cuenta") for fila in excepciones}
if ids_exc != EXCEPCIONES_ESPERADAS:
    problemas.append(f"excepciones.csv tiene {sorted(i for i in ids_exc if i)}; se esperaban {sorted(EXCEPCIONES_ESPERADAS)}")
for fila in excepciones:
    if not (fila.get("motivo") or "").strip():
        problemas.append(f"{fila.get('id_cuenta')} está en excepciones sin motivo")

cambios = Path("CAMBIOS.md")
if not cambios.exists() or len(cambios.read_text(encoding="utf-8").strip()) < 200:
    problemas.append("Falta CAMBIOS.md (o es muy corto): cuenta qué cambió, qué arreglaste y qué decidiste")

if problemas:
    print(f"\n✗ {len(problemas)} cosa(s) por revisar:")
    for p in problemas:
        print(f"  - {p}")
    sys.exit(1)
print("✓ Resultados y excepciones correctos")
print("✓ CAMBIOS.md presente")
print("\nListo para enviar. Lo que más pesa en la revisión es tu CAMBIOS.md.")
