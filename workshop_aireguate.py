"""
Workshop AireGuate
Acceso y análisis de datos de calidad del aire con Python

Universidad Rafael Landívar
Datos proporcionados mediante la API de Smability.
"""


# ==================================================================
# Parte 1 — Qué estamos haciendo
# Objetivo: Reconocer de dónde salen los datos y cómo llegan a Python.
# ==================================================================

# Una **API** es una interfaz que un programa ofrece a otros programas. Una **solicitud
# HTTP** es un mensaje enviado a un servidor; **GET** es el método que usamos para pedir
# información. **JSON** es un formato de texto para intercambiar datos organizados.
# AWS aloja el endpoint de la API; la API de Smability entrega registros horarios de
# sensores ambientales. Recibiremos información del equipo y del periodo, más una lista de
# mediciones, indicadores AQI y campos de calidad. El nombre del dominio identifica AWS API
# Gateway; no necesitamos conocer ni suponer los componentes internos del servidor.
# print es una función incorporada: muestra un mensaje en la salida.
# Una función realiza una tarea; lo que le damos entre paréntesis es un argumento.
print("API → JSON → pandas → organización → análisis → gráficas")

# Python solicita los datos y después los transforma. AWS no crea nuestras gráficas: las
# haremos localmente.

# ==================================================================
# Parte 2 — Entender la URL
# Objetivo: Distinguir la dirección base de los parámetros que puedes cambiar.
# ==================================================================

# El **endpoint** o `BASE_URL` es la dirección del servicio. Los **parámetros de consulta**
# van después de `?`, separados por `&`; cada uno tiene un nombre y un valor.
# `action=hourly_history` solicita el historial horario; `deviceID` selecciona el equipo;
# `days` pide el número de días. Pedir siete días no garantiza 168 registros: puede haber
# horas ausentes.
# Un **diccionario** de Python relaciona claves con valores mediante `clave: valor`. Es
# apropiado para `params` porque cada parámetro tiene un nombre. Usaremos claves de texto,
# entre comillas.
# La dirección base no incluye el signo ? ni los parámetros.
print("https://jciiy1ok97.execute-api.us-east-1.amazonaws.com/default/getData")

# El endpoint identifica el servicio; los parámetros precisan qué información pedimos.

# ==================================================================
# Parte 3 — Primera llamada a la API
# Objetivo: Pedir siete días del equipo SMAA_006.
# ==================================================================

# Una **variable** es un nombre asociado a un valor. El operador `=` asigna ese valor; no
# expresa aquí una comparación. Un **string** es texto y lleva comillas (`"SMAA_006"`); un
# **integer** es un número entero (`7`) y no lleva comillas porque queremos un valor
# numérico. `True` y `False` son valores booleanos.
# `import` carga una biblioteca. Un **método** es una operación asociada a un objeto, como
# `response.raise_for_status()`. Los paréntesis ejecutan esa operación. En `try` colocamos
# algo que puede fallar y en `except` explicamos un error previsto.
import requests

BASE_URL = "https://jciiy1ok97.execute-api.us-east-1.amazonaws.com/default/getData"

# ==========================================================
# CAMBIA SOLAMENTE ESTAS VARIABLES
# ==========================================================
DEVICE_ID = "SMAA_006"  # Después prueba "SMAA_005".
DAYS = 7  # Entero positivo: cantidad de días solicitados.
USAR_EJEMPLO = False  # True permite estudiar cuatro registros sin Internet.

# Un diccionario relaciona el nombre de cada ubicación con el ID del equipo.
DISPOSITIVOS = {
    "Zona 16 - Campus Universidad Rafael Landívar": "SMAA_006",
    "Zona 9 - Centro Landivariano Integral de Proyección": "SMAA_005"
}
if DEVICE_ID not in DISPOSITIVOS.values():
    raise ValueError("Selecciona SMAA_006 o SMAA_005 para este workshop.")
if type(DAYS) is not int or DAYS < 1:
    raise ValueError("DAYS debe ser un entero positivo, por ejemplo 7.")

params = {
    "action": "hourly_history",
    "deviceID": DEVICE_ID,
    "days": DAYS
}
response = None  # None representa que aún no tenemos una respuesta.
if USAR_EJEMPLO:
    print("MODO EDUCATIVO: muestra fija de SMAA_006; DEVICE_ID y DAYS no la modifican.")
else:
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        print("URL construida:", response.url)
        # Detiene el flujo si el servidor responde con un error HTTP (4xx o 5xx).
        response.raise_for_status()
        print("Estado HTTP:", response.status_code)
    except requests.RequestException as error:
        # Incluye problemas HTTP, conexión y tiempo de espera agotado.
        raise RuntimeError(
            "No se pudo consultar la API. Revisa Internet y vuelve a intentar; "
            "para practicar sin conexión, cambia USAR_EJEMPLO a True."
        ) from error

# `raise_for_status()` comprueba el estado HTTP, pero todavía no valida el contenido JSON.
# Los mensajes de error detienen el proceso para evitar analizar una respuesta inválida.

# ==================================================================
# Parte 4 — JSON
# Objetivo: Identificar los dos niveles de la respuesta y extraer un registro.
# ==================================================================

# `response.json()` interpreta el texto JSON como objetos de Python. El nivel superior es un
# diccionario: una **clave**, por ejemplo `"deviceID"`, identifica su **valor**. Una
# **lista** almacena elementos en orden. El valor de `data["data"]` es una lista de
# diccionarios; cada diccionario es un registro horario.
# `data["deviceID"]`, `data["days"]` y `data["hours"]` son metadatos. Las mediciones están
# en `data["data"]`. El nombre de la variable `data` y la clave `"data"` coinciden, pero son
# cosas distintas. El índice `[0]` representa el primer elemento porque Python comienza a
# contar posiciones desde cero.
if USAR_EJEMPLO:
    import json
    from pathlib import Path

    # Localiza la muestra junto a este script, independientemente de la carpeta actual.
    ruta_ejemplo = Path(__file__).resolve().parent / "datos/ejemplo_respuesta.json"
    data = json.loads(ruta_ejemplo.read_text(encoding="utf-8"))
else:
    try:
        data = response.json()
    except ValueError as error:
        raise ValueError("La respuesta recibida no contiene JSON válido.") from error

# Validamos la estructura antes de acceder con corchetes a una clave.
if not isinstance(data, dict) or "data" not in data:
    raise ValueError("La respuesta debe ser un diccionario con la clave 'data'.")
if not isinstance(data["data"], list):
    raise ValueError("La clave 'data' debe contener una lista de registros.")
for clave in ["deviceID", "days", "hours"]:
    if clave not in data:
        raise ValueError(f"Falta el metadato esperado: {clave}")
    print(clave, ":", data[clave])

if not USAR_EJEMPLO and data["deviceID"] != DEVICE_ID:
    raise ValueError("La respuesta corresponde a un equipo diferente del solicitado.")
for registro in data["data"]:
    if not isinstance(registro, dict):
        raise ValueError("Cada registro debe ser un diccionario.")
    if registro.get("deviceID") != data["deviceID"]:
        raise ValueError("Hay un registro con un ID distinto al de la respuesta.")

# No se puede leer [0] de una lista vacía: primero comprobamos su contenido.
if data["data"]:
    primer_registro = data["data"][0]
    print("Primer registro:", primer_registro)
else:
    print("La API no devolvió registros para esta consulta.")

print("Registros recibidos:", len(data["data"]))
if data["hours"] != len(data["data"]):
    print("Aviso: 'hours' difiere del número de registros; revisa la respuesta.")

# Mantiene el título correcto incluso al cambiar de equipo o usar la muestra.
nombre_dispositivo = "Dispositivo " + str(data["deviceID"])
for ubicacion, identificador in DISPOSITIVOS.items():
    if identificador == data["deviceID"]:
        nombre_dispositivo = ubicacion

# No creamos `pd.DataFrame(data)`: eso mezclaría los metadatos superiores con la lista de
# mediciones. Primero extraemos esa lista. `len` cuenta elementos; `for` recorre una
# colección y `if` ejecuta un bloque si se cumple una condición. La indentación delimita los
# bloques. Una cadena con prefijo `f` inserta valores entre llaves.

# ==================================================================
# Parte 5 — pandas
# Objetivo: Convertir los registros en una tabla que podamos explorar.
# ==================================================================

# `pandas` es una biblioteca para trabajar con tablas. `import pandas as pd` le da el alias
# corto `pd`; no cambia la biblioteca. Un **DataFrame** es una tabla con filas y columnas:
# aquí cada fila representa un registro horario y cada **columna** un campo, como
# `pm25_avg`.
import pandas as pd

records = data["data"]  # Lista de mediciones, sin los metadatos superiores.
df = pd.DataFrame(records)

print(df.head())  # Método: muestra las primeras cinco filas, si existen.
print(df.columns)  # Atributo: muestra los nombres de columnas, sin paréntesis.
df.info()  # Método: informa tamaños, tipos de datos y valores no nulos.

# Un atributo describe un objeto (`df.columns`); un método realiza una operación
# (`df.head()`). `info()` ayuda a detectar columnas incompletas o tipos inesperados antes
# del análisis.

# ==================================================================
# Parte 6 — Selección y organización
# Objetivo: Elegir columnas, convertir el tiempo y ordenar las filas.
# ==================================================================

# Un **Unix timestamp** es la cantidad de segundos transcurridos desde el 1 de enero de 1970
# a las 00:00:00 UTC. **UTC** significa Tiempo Universal Coordinado: permite almacenar y
# comparar instantes usando una referencia común, sin depender de la zona de cada sensor o
# computadora. El campo documentado es `hour_timestamp_utc`, en segundos.
# Primero interpretamos el valor como UTC; después lo convertimos a `America/Guatemala`. Así
# leemos los patrones diarios en hora local. `tz_convert` cambia la representación horaria y
# conserva el instante; no restamos horas manualmente. `.dt` permite acceder a operaciones
# de fecha sobre una columna.
# Conservaremos todos los campos en `df_completo` para revisar la calidad en la siguiente
# parte. `df` tendrá las columnas necesarias para los primeros análisis.
columnas = [
    "hour_timestamp_utc",
    "temperature_avg",
    "humidity_avg",
    "pm25_avg",
    "pm10_avg",
    "co_avg",
    "o3_avg"
]
# Una lista es útil para mantener juntos y en orden los nombres a seleccionar.
df_completo = df.copy()  # Conserva una copia con las variables de calidad.
if df.empty:
    # Define las columnas para que las secciones posteriores reconozcan la tabla vacía.
    df = pd.DataFrame(columns=columnas)
    print("Sin registros: se omitirán las estadísticas y las gráficas.")
else:
    for columna in columnas:
        if columna not in df.columns:
            raise ValueError(f"Falta la columna esperada: {columna}")
    df = df[columnas].copy()

for columna in columnas:
    # errors='raise' impide convertir texto inválido silenciosamente en un dato perdido.
    df[columna] = pd.to_numeric(df[columna], errors="raise")

# unit='s' especifica segundos, utc=True indica la referencia temporal de origen.
df["fecha_utc"] = pd.to_datetime(
    df["hour_timestamp_utc"], unit="s", utc=True, errors="raise"
)
if df["fecha_utc"].isna().any():
    raise ValueError("Hay timestamps vacíos; revisa esos registros antes de continuar.")
if df["fecha_utc"].duplicated().any():
    raise ValueError("Hay horas duplicadas; revísalas antes de calcular estadísticas.")
df["fecha_guatemala"] = df["fecha_utc"].dt.tz_convert("America/Guatemala")
# sort_values ordena las filas por tiempo; reset_index renumera las filas.
df = df.sort_values("fecha_utc").reset_index(drop=True)
print(df[["fecha_utc", "fecha_guatemala", "pm25_avg", "temperature_avg"]].head())

# La fecha UTC y la fecha local representan el mismo instante. Los datos se ordenan de más
# antiguos a más recientes; no se rellenan huecos ni se interpolan mediciones. Una columna
# ausente o un timestamp inválido produce un error visible.

# ==================================================================
# Parte 7 — Revisión de calidad de datos
# Objetivo: Inspeccionar la calidad antes de interpretar las concentraciones.
# ==================================================================

# Hay tres grupos de interés:
# | Grupo | Campos |
# |---|---|
# | Ambientales | `temperature_avg`, `humidity_avg`, `pm25_avg`, `pm10_avg`, `co_avg`,
# `o3_avg`, `noise_avg` |
# | Indicadores de calidad del aire (AQI) | `aqi`, `aqi_category`, `aqi_pollutant`,
# `aqi_pm25`, `aqi_pm10`, `aqi_co`, `aqi_o3` |
# | Calidad y operación del equipo | `quality_status`, `quality_score`, `data_completeness`,
# `data_points`, `battery_avg`, `max_gap_seconds` |
# Un valor ambiental resume las observaciones disponibles. Pocos puntos, huecos grandes o
# menor completitud pueden limitar su representatividad. `quality_status` describe la
# calidad del registro: **no es** la categoría de calidad del aire `aqi_category`. Tampoco
# podemos interpretar un cero como ausencia confirmada de contaminante sin conocer el
# sensor.
# No definimos umbrales, descartes automáticos ni unidades no confirmadas. Consulte [la
# referencia](docs/referencia_variables.md) para los campos y las limitaciones de
# interpretación.
columnas_calidad = [
    "quality_status", "quality_score", "data_completeness",
    "data_points", "max_gap_seconds"
]
if not df_completo.empty:
    for columna in columnas_calidad:
        if columna not in df_completo.columns:
            raise ValueError(f"Falta el campo de calidad esperado: {columna}")
    print(df_completo[["hour_timestamp_utc"] + columnas_calidad].head())
    # Cuenta etiquetas, incluyendo los registros sin etiqueta (dropna=False).
    print(df_completo["quality_status"].value_counts(dropna=False))
    print("Campos de calidad sin dato:")
    print(df_completo[columnas_calidad].isna().sum())
    print("Campos del análisis sin dato:")
    print(df.isna().sum())
    print("Estas son inspecciones; no se ha aplicado ningún filtro de aceptación.")
else:
    print("No hay registros cuya calidad se pueda inspeccionar.")

# Examinamos los campos junto al timestamp para poder localizar el registro. `isna()`
# identifica valores ausentes; `sum()` los cuenta por columna. La API no documenta aquí cómo
# calcula las puntuaciones ni su criterio de aceptación.

# ==================================================================
# Parte 8 — Estadística descriptiva
# Objetivo: Resumir los registros disponibles con medidas sencillas.
# ==================================================================

# El **promedio** suma los valores válidos y divide entre su cantidad; el **mínimo** y el
# **máximo** son los extremos observados. La **desviación estándar** describe la dispersión
# respecto al promedio (pandas usa la versión muestral). Los **percentiles** 25, 50 y 75
# indican posiciones en la distribución; el 50 es la mediana. `count` indica cuántos valores
# no ausentes hay en cada columna.
# Estas estadísticas resumen promedios horarios disponibles: no son el promedio de todas las
# mediciones originales ni una evaluación normativa o sanitaria. pandas omite valores
# ausentes y no los convierte en cero.
if not df.empty:
    print("Promedio horario disponible de PM2.5:", df["pm25_avg"].mean())
    print("Mínimo de los promedios horarios:", df["pm25_avg"].min())
    print("Máximo de los promedios horarios:", df["pm25_avg"].max())
    print(df[[
        "temperature_avg", "humidity_avg", "pm25_avg",
        "pm10_avg", "co_avg", "o3_avg"
    ]].describe())
else:
    print("Sin registros: no se calculan estadísticas.")

# Un par de corchetes selecciona una columna y devuelve una serie; la lista dentro de dos
# pares selecciona varias columnas y conserva una tabla. Cada hora válida tiene el mismo
# peso. `NaN` indica que una estadística no pudo calcularse, por ejemplo por falta de datos.

# ==================================================================
# Parte 9 — Primera gráfica
# Objetivo: Representar PM2.5 a lo largo del tiempo local.
# ==================================================================

# Una **serie temporal** relaciona una variable con el tiempo. La **figura** es el espacio
# de dibujo; el **eje X** mostrará fechas locales y el **eje Y**, PM2.5.
# `matplotlib.pyplot`, abreviado `plt`, permite dibujarla. Las etiquetas usan el nombre del
# campo porque la respuesta no confirma unidades.
# El título identifica el dispositivo realmente consultado. La línea conecta observaciones y
# puede atravesar horas sin datos: no implica que se hayan medido todas las horas
# intermedias.
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from zoneinfo import ZoneInfo

# La zona explícita evita que matplotlib muestre UTC por su configuración predeterminada.
ZONA_GUATEMALA = ZoneInfo("America/Guatemala")
if not df.empty and df["pm25_avg"].notna().any():
    plt.figure(figsize=(12, 5))  # Crea una figura de 12 por 5 pulgadas.
    plt.plot(df["fecha_guatemala"], df["pm25_avg"], marker=".")
    plt.xlabel("Fecha y hora de Guatemala")  # Etiqueta del eje horizontal.
    plt.ylabel("PM2.5 (unidad no confirmada)")  # Etiqueta del eje vertical.
    plt.title("PM2.5 - " + nombre_dispositivo)
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%d/%m %H:%M", tz=ZONA_GUATEMALA)
    )
    plt.xticks(rotation=45)  # Gira las fechas para reducir superposiciones.
    plt.tight_layout()  # Ajusta los márgenes para que las etiquetas se vean completas.
    plt.show()  # Presenta la figura; en el script puede abrir una ventana.
    plt.close()  # Libera la figura después de mostrarla.
else:
    print("No hay valores válidos de PM2.5 para graficar.")

# `gca()` obtiene los ejes actuales; el formateador controla cómo se escriben las fechas. El
# desplazamiento horario no depende de la zona de tu computadora. En el script, cierra cada
# ventana para que continúe.

# ==================================================================
# Parte 10 — Otras variables
# Objetivo: Reutilizar el bloque de dibujo cambiando una columna.
# ==================================================================

# Una variable de Python también puede guardar el nombre de una columna. Así reutilizamos el
# mismo código sin copiar una gráfica para cada contaminante. En la siguiente parte
# aprenderemos a convertir operaciones repetidas en funciones.
# ==========================================================
# CAMBIA SOLAMENTE ESTA VARIABLE
# Opciones: temperature_avg, humidity_avg, pm10_avg, co_avg, o3_avg
# ==========================================================
VARIABLE = "temperature_avg"

if VARIABLE not in df.columns:
    raise ValueError(f"La columna {VARIABLE} no existe. Revisa df.columns.")
if not df.empty and df[VARIABLE].notna().any():
    plt.figure(figsize=(12, 5))
    plt.plot(df["fecha_guatemala"], df[VARIABLE], marker=".")
    plt.xlabel("Fecha y hora de Guatemala")
    plt.ylabel(VARIABLE + " (unidad no confirmada)")
    plt.title(VARIABLE + " - " + nombre_dispositivo)
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%d/%m %H:%M", tz=ZONA_GUATEMALA)
    )
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()
else:
    print(f"No hay valores válidos de {VARIABLE} para graficar.")

# `df[VARIABLE]` usa el texto guardado en VARIABLE como nombre de columna. Los ejes y el
# título cambian con esa elección. No comparamos numéricamente variables con unidades
# diferentes.

# ==================================================================
# Parte 11 — Introducción a funciones
# Objetivo: Agrupar el flujo de consulta para reutilizarlo con otro equipo.
# ==================================================================

# `def` define una función: un bloque con nombre que podemos ejecutar varias veces.
# `consultar_dispositivo` es su nombre; `device_id` y `days` son **parámetros**, nombres que
# recibirán los valores de cada llamada. `days=7` establece un **valor por defecto**. Al
# llamar `consultar_dispositivo("SMAA_005", days=3)`, el texto y el número son los
# **argumentos** concretos.
# `return` devuelve un resultado a quien llamó la función. La indentación indica qué líneas
# pertenecen a la función. Las variables creadas dentro son locales a esa llamada.
# Conservamos los campos de calidad para poder inspeccionarlos junto a cada serie.
def consultar_dispositivo(device_id, days=7):
    """Consulta datos horarios y devuelve una tabla con todas las columnas y fechas."""
    if device_id not in DISPOSITIVOS.values():
        raise ValueError("Selecciona SMAA_006 o SMAA_005.")
    if type(days) is not int or days < 1:
        raise ValueError("days debe ser un entero positivo.")

    # Cada llamada construye sus propios parámetros: el equipo ya no está fijo.
    parametros = {"action": "hourly_history", "deviceID": device_id, "days": days}
    try:
        respuesta = requests.get(BASE_URL, params=parametros, timeout=30)
        respuesta.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"No se pudo consultar {device_id}: revisa la conexión o el servicio.") from error
    try:
        contenido = respuesta.json()
    except ValueError as error:
        raise ValueError(f"{device_id}: la respuesta no es JSON válido.") from error

    if not isinstance(contenido, dict) or "data" not in contenido:
        raise ValueError(f"{device_id}: falta la lista 'data' en la respuesta.")
    if contenido.get("deviceID") != device_id:
        raise ValueError(f"{device_id}: el ID de la respuesta no coincide con el solicitado.")
    registros = contenido["data"]
    if not isinstance(registros, list):
        raise ValueError(f"{device_id}: 'data' debe ser una lista.")
    if not registros:
        print(f"{device_id}: la API no devolvió registros para esta consulta.")
        return pd.DataFrame()  # Devuelve una tabla vacía; el código que llama lo comprobará.

    for registro in registros:
        if not isinstance(registro, dict) or registro.get("deviceID") != device_id:
            raise ValueError(f"{device_id}: registro inválido o de otro equipo.")
    tabla = pd.DataFrame(registros)
    # Se comprueban campos ambientales y de calidad, sin imponer umbrales de aceptación.
    for columna in columnas + columnas_calidad:
        if columna not in tabla.columns:
            raise ValueError(f"{device_id}: falta la columna esperada {columna}.")
    for columna in columnas:
        tabla[columna] = pd.to_numeric(tabla[columna], errors="raise")
    tabla["fecha_utc"] = pd.to_datetime(
        tabla["hour_timestamp_utc"], unit="s", utc=True, errors="raise"
    )
    if tabla["fecha_utc"].isna().any() or tabla["fecha_utc"].duplicated().any():
        raise ValueError(f"{device_id}: revisa timestamps vacíos o duplicados.")
    tabla["fecha_guatemala"] = tabla["fecha_utc"].dt.tz_convert("America/Guatemala")
    return tabla.sort_values("fecha_utc").reset_index(drop=True)

# Definir la función no consulta la red. La ejecutaremos en la Parte 12 dos veces, con
# distintos argumentos. Usa BASE_URL, DISPOSITIVOS y las listas de columnas definidas antes:
# por eso ejecutamos el notebook en orden.

# ==================================================================
# Parte 12 — Comparación Zona 9 vs Zona 16
# Objetivo: Consultar ambos equipos y representar la misma variable.
# ==================================================================

# La misma función sirve para los dos lugares. Solo cambia el argumento del equipo. Una
# **leyenda** identifica las series; no implica que las condiciones, cobertura ni calidad
# sean idénticas. Antes de comparar, revisaremos calidad, cantidad de registros, intervalos
# y horas comunes. No rellenamos horas ausentes ni calculamos diferencias entre filas
# desalineadas.
# Cambia solo esta columna para comparar otra variable de ambos dispositivos.
# Opciones: pm25_avg, temperature_avg, humidity_avg, pm10_avg, o3_avg
VARIABLE_COMPARACION = "pm25_avg"

if USAR_EJEMPLO:
    # La muestra contiene un solo equipo: no inventamos una segunda serie.
    df_zona16 = pd.DataFrame()
    df_zona9 = pd.DataFrame()
    print("Comparación omitida en modo educativo. Usa Internet y USAR_EJEMPLO=False.")
else:
    df_zona16 = consultar_dispositivo("SMAA_006", days=DAYS)
    df_zona9 = consultar_dispositivo("SMAA_005", days=DAYS)

    if df_zona16.empty or df_zona9.empty:
        print("Se necesitan registros de ambos equipos para compararlos.")
    else:
        for etiqueta, tabla in [("Zona 16", df_zona16), ("Zona 9", df_zona9)]:
            if VARIABLE_COMPARACION not in tabla.columns:
                raise ValueError(f"{etiqueta}: falta la columna {VARIABLE_COMPARACION}.")
            print(etiqueta, "registros:", len(tabla))
            print("Periodo local:", tabla["fecha_guatemala"].min(), "a", tabla["fecha_guatemala"].max())
            print(tabla[["fecha_guatemala"] + columnas_calidad].head())
            print(tabla["quality_status"].value_counts(dropna=False))
            print("Valores ausentes:", tabla[columnas_calidad + [VARIABLE_COMPARACION]].isna().sum())

        # intersection obtiene las horas presentes en las dos tablas, sin interpolación.
        horas_comunes = pd.Index(df_zona16["fecha_utc"]).intersection(df_zona9["fecha_utc"])
        print("Horas presentes en ambos equipos:", len(horas_comunes))
        if len(horas_comunes) == 0:
            print("No hay horas coincidentes: la gráfica muestra periodos distintos.")

        if df_zona16[VARIABLE_COMPARACION].notna().any() and df_zona9[VARIABLE_COMPARACION].notna().any():
            plt.figure(figsize=(12, 5))
            plt.plot(
                df_zona16["fecha_guatemala"], df_zona16[VARIABLE_COMPARACION],
                label="Zona 16 - Campus Universidad Rafael Landívar", marker="."
            )
            plt.plot(
                df_zona9["fecha_guatemala"], df_zona9[VARIABLE_COMPARACION],
                label="Zona 9 - Centro Landivariano Integral de Proyección", marker="."
            )
            plt.xlabel("Fecha y hora de Guatemala")
            plt.ylabel(VARIABLE_COMPARACION + " (unidad no confirmada)")
            plt.title("Comparación entre Zona 16 y Zona 9")
            plt.gca().xaxis.set_major_formatter(
                mdates.DateFormatter("%d/%m %H:%M", tz=ZONA_GUATEMALA)
            )
            plt.legend()  # Relaciona cada color con su ubicación.
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            plt.close()
        else:
            print("Faltan valores válidos de la variable en al menos uno de los equipos.")

# Ambas consultas usan los mismos días solicitados, pero cada equipo puede devolver distinta
# cobertura. Las horas comunes cuentan timestamps, no certifican que la variable ni su
# calidad sean válidas en todos ellos. Cambia VARIABLE_COMPARACION para explorar
# temperatura, humedad, PM10 u O3.

# ==================================================================
# Parte 13 — Ejercicio final
# Objetivo: Completar el flujo con tus propias decisiones y describir lo observado.
# ==================================================================

# Las observaciones deben referirse a lo que muestran los datos y reconocer sus límites. Usa
# las partes anteriores como referencia, sin asumir que una diferencia demuestra una causa.
# No hay respuestas resueltas al final de este notebook.
# Espacio de trabajo del participante.
# Escribe aquí tu consulta, revisión de calidad, estadísticas y gráfica.
# No se incluyen soluciones automáticas del ejercicio.

# Puedes añadir celdas de código y texto para documentar tu trabajo.

# Ejercicio final: elige equipo y días; consulta; identifica columnas; convierte
# el tiempo; revisa calidad; calcula estadísticas; elige una variable; grafica;
# redacta 2–3 observaciones con evidencia y una limitación de los datos.
