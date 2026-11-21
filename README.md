# Reto DSI · Arregla el bot

**Para quién:** quien quiera postularse como RPA Developer en DSI Factory.
**Tiempo:** unos 60 minutos.
**Necesitas:** Python 3.10 o superior. Solo la librería estándar, sin instalar nada.

> Ejemplo ilustrativo. Todos los datos son ficticios: no hay clientes, pacientes ni portales reales.

---

## La historia

Este bot revisa todos los días en qué estado va cada cuenta en el portal de una aseguradora (simulado): si ya se radicó, si está en revisión o si la devolvieron. Lee las cuentas de `datos/cuentas.csv`, consulta el portal y deja el resultado en `salida/resultados.csv`.

Ayer funcionaba. Esta mañana se cae en la primera cuenta.

Nadie tocó el bot. Algo cambió afuera.

Eso pasa todas las semanas en el trabajo de un RPA Developer: un tercero cambia su portal y el bot se detiene. Escribir el bot es la mitad del trabajo. La otra mitad es decidir qué hacer cuando algo cambia.

## Lo que tienes que hacer

1. **Que corra de punta a punta.** `python bot.py` tiene que terminar sin error.
2. **Que una cuenta con problemas no tumbe a las demás.** La cuenta que no se pueda procesar va a `salida/excepciones.csv`, con su `id_cuenta` y un `motivo` que otra persona entienda sin preguntarte.
3. **Si el portal no responde, reintenta.** Máximo 2 reintentos por cuenta. Si después de eso sigue sin responder, la cuenta va a excepciones.
4. **Revisa tu trabajo** con `python verificar.py`. El script corre el bot y compara la salida.
5. **Escribe `CAMBIOS.md`** con tres cosas:
   - Qué cambió en el portal y cómo te diste cuenta.
   - Qué arreglaste.
   - **Una decisión que tomaste y por qué.** Por ejemplo, qué hiciste con una cuenta que no tenía sentido.

## Reglas

- No modifiques `portal/`, `datos/` ni `verificar.py`. Son el mundo de afuera: no los controlas.
- Puedes reescribir `bot.py` todo lo que quieras.
- Si algo del enunciado no te queda claro, decide, y cuenta en `CAMBIOS.md` cómo decidiste. Eso también lo evaluamos.

## Qué miramos

| Qué | Peso |
|---|---|
| `CAMBIOS.md`: qué entendiste, qué decidiste y por qué | El que más |
| Que `verificar.py` pase | Alto |
| Excepciones con motivos claros, sin que el bot se caiga | Alto |
| Código que otra persona pueda leer y mantener | Medio |

No buscamos el código más corto. Buscamos el que otra persona del equipo pueda operar mañana.

## Cómo entregarlo

Envía un correo a **jairo@dsinno.io** con el asunto **`Reto RPA · Tu nombre · web`**. Incluye:

- Un enlace a tu repositorio (GitHub, GitLab u otro) o el proyecto en un `.zip`.
- Tu celular y tu ciudad.
- **¿Cómo supiste de esta vacante?**

El reto reemplaza la hoja de vida. Si quieres mandarla también, adjúntala.

Al enviar tu postulación autorizas el tratamiento de tus datos según el aviso de privacidad de la página `dsinno.io/trabaja-en-dsi`.

---

DSI no opera. DSI orquesta. · Holding de innovación en salud, desde Medellín.
