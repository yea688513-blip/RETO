# Bitácora de cambios

## Qué revisé

Seguí el flujo desde `datos/cuentas.csv` hasta la respuesta simulada en `portal/respuestas.json`, sin modificar esos datos ni el código del portal. La estructura de la respuesta actual (versión 2.0) cambió respecto de la que esperaba el bot.

## Error encontrado

El bot leía `respuesta["estado"]` y `respuesta["fecha"]`, y convertía la fecha con el formato `DD/MM/AAAA`. El portal ahora entrega `estado_radicacion` y `fecha_radicacion` en formato ISO (`AAAA-MM-DD`). Por eso se detenía al procesar la primera cuenta con un `KeyError` antes de generar sus archivos de salida.

Al revisar el resto del lote también encontré datos que requerían tratamiento: `C-1003` tiene valor escrito como `1.320.500` y no tiene fecha de radicación porque sigue en revisión; `C-1005` no existe en el portal; `C-1006` tiene valor cero; y `C-1007` presenta una falla temporal en la primera consulta.

## Qué cambié

- Actualicé la lectura de respuesta para usar `estado_radicacion` y `fecha_radicacion`, y parsear la fecha ISO.
- Normalicé separadores de miles al convertir valores a entero.
- Añadí hasta dos reintentos cuando el portal informa que no está disponible. Si se agotan, esa cuenta queda en excepciones y el lote continúa.
- Separé las cuentas inválidas o inexistentes en `salida/excepciones.csv`, con un motivo legible para cada una.
- Para estados sin fecha, como `en_revision`, dejé `dias_hasta_radicar` vacío en lugar de inventar un número.
- Rechacé el valor cero de `C-1006` y lo envié a excepciones porque no representa una cuenta facturable válida.

## Decisión

Decidí excluir `C-1006` de resultados por tener valor cero, aunque el portal sí devuelva un estado. Mantenerla como cuenta procesada podría ocultar un problema de calidad o facturación; el archivo de excepciones deja visible el motivo para que alguien lo corrija en el origen.

## Cómo reproducir

Desde la carpeta del proyecto, ejecutar `python bot.py` genera `salida/resultados.csv` y `salida/excepciones.csv`. Ejecutar `python verificar.py` comprueba que el procesamiento, las excepciones y esta bitácora coincidan con lo esperado.
