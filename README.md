# Workshop AireGuate

## Acceso y análisis de datos de calidad del aire con Python

Workshop práctico. Los datos se obtienen de sensores mediante la API de **Smability**, alojada en AWS.

## Objetivo

Aprender a consultar la API de Smability, interpretar su respuesta JSON, organizar registros horarios con pandas, revisar variables básicas de calidad de datos, realizar análisis descriptivo y construir gráficas sencillas. El material explica los conceptos de Python al utilizarlos; no es un curso de programación desde cero.

```text
API → JSON → pandas → limpieza → análisis → visualización
```

Aquí la limpieza consiste en comprobar estructura y tipos, organizar columnas y ordenar fechas. No se imputan valores, no se interpolan huecos ni se aplican umbrales de calidad inventados.

## Requisitos

- Python **3.10 o superior** recomendado. La validación inicial se realizó con Python 3.13.2 en macOS.
- Jupyter Notebook o JupyterLab (incluidos al instalar las dependencias).
- Conexión a Internet para instalar dependencias y consultar la API.
- Git es opcional: también puedes descargar el repositorio desde **Code → Download ZIP** y descomprimirlo.

## Instalación

Si tienes Git:

```bash
git clone https://github.com/daperezmora/Workshop-AireGuate.git
cd Workshop-AireGuate
python -m venv .venv
```

Si descargaste el ZIP, abre una terminal dentro de la carpeta descomprimida y ejecuta `python -m venv .venv`. El nombre de esa carpeta puede terminar en `-main`. En macOS/Linux, usa `python3` si `python` no está disponible para crear el entorno.

Activa el entorno en **Windows, símbolo del sistema (cmd.exe)**:

```bat
.venv\Scripts\activate
```

En **Windows PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell impide ejecutar ese script por la configuración institucional, utiliza cmd.exe con el comando anterior.

En **macOS/Linux**:

```bash
source .venv/bin/activate
```

Después, con el entorno activo:

```bash
pip install -r requirements.txt
jupyter notebook
```

Abre **workshop_aireguate.ipynb** y selecciona el kernel Python del entorno recién instalado. También puedes iniciar `jupyter lab`. Mantén el notebook en la raíz del repositorio para que encuentre `datos/ejemplo_respuesta.json`.

## Cómo trabajar

El **notebook es el documento principal**. Ejecuta las celdas en orden con **Shift + Enter**. Cada parte incluye objetivo, concepto, código, explicación, resultado esperado y una actividad. El ejercicio final queda abierto, sin respuestas resueltas debajo.

Para ejecutar todo el notebook desde cero, usa **Kernel → Restart & Run All** (reiniciar y ejecutar todas). Si modificas las variables de consulta, vuelve a ejecutar desde la Parte 3. El notebook se distribuye sin resultados guardados para evitar que cifras antiguas se confundan con consultas actuales.

En la Parte 3 encontrarás:

```python
# ==========================================================
# CAMBIA SOLAMENTE ESTAS VARIABLES
# ==========================================================
DEVICE_ID = "SMAA_006"
DAYS = 7
USAR_EJEMPLO = False
```

1. Empieza con `SMAA_006` y siete días.
2. Después cambia `DEVICE_ID` a `"SMAA_005"` y vuelve a ejecutar desde la consulta. El título de las gráficas se actualizará.
3. En la Parte 10 cambia `VARIABLE` para explorar otro campo.
4. En la Parte 12 cambia `VARIABLE_COMPARACION` para comparar ambas ubicaciones con los mismos días solicitados.

El script recorre el mismo flujo básico, con comentarios en español:

```bash
python workshop_aireguate.py
```

Edita sus variables de configuración igual que en el notebook. En una sesión de escritorio, **cierra cada ventana de gráfica para continuar**. Si trabajas en un servidor sin pantalla, puedes ejecutar `MPLBACKEND=Agg python workshop_aireguate.py` en macOS/Linux para verificar el cálculo y dibujo sin abrir ventanas; esa variante no guarda imágenes.

## Contenido

```text
Workshop-AireGuate/
├── README.md
├── requirements.txt
├── .gitignore
├── workshop_aireguate.ipynb
├── workshop_aireguate.py
├── datos/
│   └── ejemplo_respuesta.json
└── docs/
    └── referencia_variables.md
```

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Instalación, ruta de trabajo, alcance y resultados de validación. |
| `requirements.txt` | Cuatro dependencias directas con versiones fijadas para repetir el entorno de referencia. Sus dependencias transitivas las resuelve pip. |
| `.gitignore` | Excluye entorno virtual, cachés, archivos locales y archivos `.env`. |
| `workshop_aireguate.ipynb` | Material docente con las 13 partes, preguntas y espacio para el ejercicio. |
| `workshop_aireguate.py` | Flujo ejecutable y comentado de consulta, análisis y comparación. |
| `datos/ejemplo_respuesta.json` | Muestra educativa de cuatro registros de SMAA_006 para estudiar el JSON sin Internet. |
| `docs/referencia_variables.md` | Campos, tipos observados, categorías y precauciones sobre unidades y significado. |

## Dispositivos

| ID | Ubicación |
|---|---|
| SMAA_006 | Campus Universidad Rafael Landívar, Zona 16 |
| SMAA_005 | Centro Landivariano Integral de Proyección, Zona 9 |

```python
DISPOSITIVOS = {
    "Zona 16 - Campus Universidad Rafael Landívar": "SMAA_006",
    "Zona 9 - Centro Landivariano Integral de Proyección": "SMAA_005"
}
```

## Variables disponibles y unidades

Las gráficas usan exclusivamente los seis campos ambientales disponibles en SMAA_005 y SMAA_006. Las unidades corresponden a la referencia visual de estos equipos, confirmada para esta actualización.

| Variable | Campo | Unidad |
|---|---|---|
| PM2.5 | `pm25_avg` | µg/m³ |
| PM10 | `pm10_avg` | µg/m³ |
| Monóxido de carbono | `co_avg` | ppb |
| Ozono | `o3_avg` | ppb |
| Temperatura | `temperature_avg` | °C |
| Humedad | `humidity_avg` | % |

`µg/m³` significa microgramos por metro cúbico y `ppb`, partes por mil millones. La batería (`battery_avg`) se expresa en **%** y es un indicador de operación, no una variable ambiental.

La API también puede incluir `no2_avg`, `ch4_avg`, `noise_avg` y `aqi_no2`, pero estos equipos no tienen sensores de NO2, CH4 ni ruido. Esos campos se conservan al explorar la respuesta original y en la muestra JSON, sin tratarlos como mediciones disponibles ni ofrecerlos para las gráficas. El diccionario `ETIQUETAS_VARIABLES` mantiene los nombres y las unidades de las seis opciones válidas.

## API y estructura de la respuesta

Endpoint:

```text
https://jciiy1ok97.execute-api.us-east-1.amazonaws.com/default/getData
```

Consulta de ejemplo, dividida únicamente para facilitar su lectura:

```text
https://jciiy1ok97.execute-api.us-east-1.amazonaws.com/default/getData
?action=hourly_history
&deviceID=SMAA_006
&days=7
```

`action` solicita historial horario; `deviceID` selecciona el equipo; `days` indica los días solicitados. `?` inicia los parámetros y `&` los separa. La dirección base es independiente de esos parámetros. `requests` construye automáticamente la URL desde un diccionario `params`; el notebook muestra `response.url` para comprobarla.

El JSON tiene dos niveles: los metadatos `deviceID`, `days`, `hours` y la lista de mediciones `data`. Por eso la tabla se construye así:

```python
records = data["data"]
df = pd.DataFrame(records)
```

No se convierte directamente el diccionario superior con `pd.DataFrame(data)`: sus metadatos no son filas de mediciones. `hours` coincidió con el número de registros en las consultas de validación, pero no debe confundirse con las horas teóricamente esperadas para `days`.

El tiempo viene en `hour_timestamp_utc`, como segundos Unix en UTC. Primero se convierte con `pd.to_datetime(..., unit="s", utc=True)` y después con `.dt.tz_convert("America/Guatemala")`. Los ejes de las gráficas también se formatean explícitamente en esa zona.

## Recorrido de las 13 partes

1. Qué estamos haciendo: API, HTTP GET, AWS, Smability y JSON.
2. Entender la URL y sus parámetros.
3. Primera llamada a la API con SMAA_006.
4. JSON: metadatos, listas y registros.
5. pandas: construir y explorar un DataFrame.
6. Selección y organización: columnas, timestamp, UTC y Guatemala.
7. Revisión de calidad de datos antes del análisis ambiental.
8. Estadística descriptiva sobre valores disponibles.
9. Primera gráfica de PM2.5.
10. Otras variables cambiando el nombre de una columna.
11. Introducción a funciones para reutilizar la consulta.
12. Comparación Zona 9 vs Zona 16, con diagnóstico de cobertura.
13. Ejercicio final y observaciones propias.

## Practicar sin Internet

Después de instalar las dependencias, cambia `USAR_EJEMPLO = True` en la Parte 3 o al inicio del script. Así se carga `datos/ejemplo_respuesta.json` y se ejecutan las actividades con esa muestra sin consultar la red.

El archivo es un **ejemplo educativo**, no un historial completo ni una respuesta actual. Contiene los primeros cuatro registros de SMAA_006 recibidos en la validación del **15 de octubre de 2026**. Se conservaron sus valores y campos; `hours` se ajustó a 4 para describir el subconjunto. `days=7` documenta la solicitud original, no la cobertura de la muestra. Cambiar `DEVICE_ID` o `DAYS` no modifica esta muestra fija.

La comparación se omite explícitamente en este modo porque no hay una muestra de SMAA_005. Para realizar la Parte 12 y el ejercicio completo, vuelve a `USAR_EJEMPLO = False` y usa Internet. El código no cambia al modo educativo automáticamente ante un fallo de red.

## Uso responsable

Estos datos provienen de sensores ambientales. Revisa `quality_status`, `quality_score`, `data_completeness`, `data_points` y `max_gap_seconds` antes de interpretarlos. `quality_status` describe la calidad del registro, mientras que `aqi_category` describe una categoría AQI; no son equivalentes.

El **AQI es un dato calculado por Smability**. Su metodología está pendiente de revisión y se documentará en una actualización posterior; en esta versión no se recalcula ni se grafica. Las gráficas ambientales y los resúmenes muestran las unidades de la tabla anterior. La [referencia de variables](docs/referencia_variables.md) distingue los sensores disponibles de otros campos del esquema. Un cero no prueba por sí solo la ausencia de un contaminante ni que el canal esté operativo.

Las estadísticas describen los **promedios horarios disponibles**, con igual peso por hora válida. No representan automáticamente todo el periodo solicitado ni todas las mediciones originales. `NaN` significa dato o estadística no disponible. Las líneas de las gráficas conectan observaciones y pueden atravesar huecos: no son evidencia de medición continua. Compara los periodos, las horas comunes y la calidad de ambos equipos antes de interpretar diferencias; las gráficas por sí solas no establecen causas.

## Errores habituales

| Situación | Qué hace el material y cómo proceder |
|---|---|
| Error HTTP, conexión o espera agotada | Muestra un error claro. Revisa la conexión y el servicio; reintenta o activa conscientemente el modo educativo. |
| Respuesta no JSON o sin `data` | Detiene el análisis con un mensaje; no trata una respuesta inválida como mediciones. |
| Lista vacía | Avisa y omite los análisis y gráficas que requieren registros. |
| Campo ambiental o de calidad ausente | Indica el nombre del campo faltante; revisa el esquema real. |
| Timestamp inválido, vacío o duplicado | Detiene la preparación para que revises la fuente antes de continuar. |
| Valores ausentes | Los conteos los hacen visibles; pandas los excluye de las estadísticas. |
| `ModuleNotFoundError` | Activa `.venv`, instala `requirements.txt` y usa el kernel de ese entorno. |
| No aparece el archivo de ejemplo | Abre el notebook desde la raíz del repositorio; el script localiza el archivo junto a sí mismo. |

## Validación inicial

Verificación del **15 de octubre de 2026**, con solicitudes `days=7`:

| Equipo | Resultado | Registros | Intervalo UTC recibido |
|---|---|---:|---|
| SMAA_006 | HTTP 200; estructura esperada | 144 | 2026-10-09 15:00 a 2026-10-15 14:00 |
| SMAA_005 | HTTP 200; estructura esperada | 142 | 2026-10-09 17:00 a 2026-10-15 14:00 |

Ambos dispositivos devolvieron las mismas 34 claves por registro, incluidos todos los campos del JSON suministrado. Los cuatro campos adicionales fueron `ttl`, `mode`, `processed_at` y `fixed_gps_saved_at`. No se asume su significado exacto. Estos resultados son una fotografía de la validación; futuras consultas pueden cambiar.

Comprobaciones realizadas antes de publicar:

- Instalación desde cero en `.venv` usando únicamente `requirements.txt`; `pip check` sin conflictos.
- Script completo ejecutado contra la API con salida correcta. Se usó el backend `Agg` para dibujar sin ventanas; los avisos de que `show()` no puede abrir una ventana con ese backend son esperados.
- Notebook completo ejecutado en un kernel nuevo de Jupyter, sin errores; tres gráficas generadas y revisadas visualmente.
- Validación del formato del notebook y del JSON; conversión de timestamps y orden cronológico correctos.
- Modo educativo comprobado en ambos formatos, sin llamadas de red y con comparación omitida explícitamente.
- Pruebas controladas de errores HTTP, conexión, timeout, JSON inválido, `data` ausente o de tipo incorrecto, listas vacías, columnas faltantes y timestamps vacíos; mensajes y comportamiento esperados.
- Cambio del dispositivo inicial a SMAA_005 comprobado, incluido el título de las gráficas.
- Revisión de los siete archivos que se publican, enlaces internos, comandos de instalación y ausencia de secretos. Las instrucciones de activación de Windows se revisaron, pero no se ejecutaron en Windows.

Las versiones directas están fijadas; no se garantiza una resolución idéntica de las dependencias transitivas en todos los sistemas. Python 3.10 es la versión mínima recomendada; esta validación ejecutable corresponde a Python 3.13.2.

## Validación de la actualización de unidades

Se volvieron a ejecutar el script y el notebook completos contra la API. Se revisaron las gráficas y se comprobó que las seis variables muestran su unidad tanto en la gráfica individual como en la comparación. También se verificaron el modo educativo y el rechazo de campos fuera de esas seis opciones (incluidos NO2, CH4, ruido, AQI y batería).

## Credenciales

La API usada no requiere una API key en estos ejemplos. No se incluyen claves, tokens ni credenciales. Si se incorporan en el futuro, usa variables de entorno y nunca las almacenes en Git. `.gitignore` excluye `.env` y sus variantes; esto complementa, pero no sustituye, la revisión de archivos antes de publicarlos.
