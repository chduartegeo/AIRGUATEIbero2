# Referencia rápida de variables

Esta referencia corresponde al esquema suministrado y a las consultas de SMAA_006 y SMAA_005 realizadas el **15 de octubre de 2026**, con `days=7`. Es una guía de lectura, no una especificación oficial del proveedor. Los tipos son los observados; una respuesta futura podría contener valores nulos o variaciones.

## Dos niveles del JSON

| Campo superior | Descripción | Tipo observado | Categoría |
|---|---|---|---|
| `deviceID` | ID del equipo consultado. | string | operación |
| `days` | Número de días indicado en la consulta. No garantiza cobertura completa. | integer | tiempo |
| `hours` | Coincidió con el número de registros devueltos en la validación; confirmar semántica contractual con el proveedor. | integer | tiempo |
| `data` | Lista de diccionarios con las mediciones horarias. | array de objetos | ambiental, AQI, calidad de datos, operación, geolocalización y tiempo |

En Python, un `string` es texto, un `integer` es un entero y un `float` es un número con decimales. Un array JSON se convierte en lista y un objeto JSON en diccionario. `data["data"]` selecciona la lista de registros; `data["data"][0]` selecciona su primer elemento, si existe.

## Tres grupos para el workshop

1. **Ambientales disponibles en estos equipos:** PM2.5, PM10, CO, O3, temperatura y humedad.
2. **Indicadores calculados por Smability:** AQI total, categoría, contaminante y subíndices. La metodología está pendiente de revisión y se documentará posteriormente.
3. **Calidad y operación:** campos que ayudan a revisar la disponibilidad y calidad del registro y el funcionamiento del equipo.

Tiempo y geolocalización aportan el contexto de las mediciones. El sufijo `_avg` sugiere un promedio del periodo horario; `_min` y `_max`, extremos del periodo. No conocemos aquí el algoritmo de agregación ni calibración.

## Sensores disponibles y unidades

Las unidades siguientes corresponden a la referencia visual confirmada para SMAA_005 y SMAA_006. Son los únicos seis campos ambientales que se ofrecen en las gráficas.

| Variable | Campo | Unidad |
|---|---|---|
| PM2.5 | `pm25_avg` | µg/m³ |
| PM10 | `pm10_avg` | µg/m³ |
| Monóxido de carbono | `co_avg` | ppb |
| Ozono | `o3_avg` | ppb |
| Temperatura | `temperature_avg` | °C |
| Humedad | `humidity_avg` | % |

`µg/m³` significa microgramos por metro cúbico y `ppb`, partes por mil millones. La batería (`battery_avg`) se expresa en **%** y es un indicador de operación, no una variable ambiental.

Estos equipos **no tienen sensores de NO2, CH4 ni ruido**. Que `no2_avg`, `ch4_avg`, `noise_avg` o `aqi_no2` aparezcan en el JSON no acredita una medición de esos canales. Se documentan para comprender el esquema, pero se excluyen del análisis y de las opciones de gráficas.

## Campos dentro de cada registro

| Campo | Descripción de lectura | Tipo observado | Categoría |
|---|---|---|---|
| `temperature_avg` | Temperatura media del registro horario, en °C. | float | ambiental |
| `temperature_min` | Temperatura mínima del registro, en °C. | float | ambiental |
| `temperature_max` | Temperatura máxima del registro, en °C. | float | ambiental |
| `humidity_avg` | Humedad media, en %. | float | ambiental |
| `pm25_avg` | Valor medio del canal PM2.5, en µg/m³. | float | ambiental |
| `pm25_min` | Valor mínimo del canal PM2.5, en µg/m³. | float | ambiental |
| `pm25_max` | Valor máximo del canal PM2.5, en µg/m³. | float | ambiental |
| `pm10_avg` | Valor medio del canal PM10, en µg/m³. | float | ambiental |
| `co_avg` | Valor medio del canal de monóxido de carbono (CO), en ppb. | float | ambiental |
| `o3_avg` | Valor medio del canal de ozono (O3), en ppb. | float | ambiental |
| `no2_avg` | Campo del esquema para NO2; sensor no instalado en estos equipos. Excluido del análisis. | float | ambiental |
| `ch4_avg` | Campo del esquema para CH4; sensor no instalado en estos equipos. Excluido del análisis. | float | ambiental |
| `noise_avg` | Campo del esquema para ruido; sensor no instalado en estos equipos. Excluido del análisis. | float | ambiental |
| `aqi` | Índice de calidad del aire calculado por Smability; metodología pendiente de revisión. No es una concentración. | float | AQI |
| `aqi_category` | Etiqueta de categoría AQI reportada, por ejemplo `Moderate`. | string | AQI |
| `aqi_pollutant` | Contaminante asociado al AQI reportado, por ejemplo `PM2.5`. | string | AQI |
| `aqi_pm25` | Subíndice AQI asociado a PM2.5. | float | AQI |
| `aqi_pm10` | Subíndice AQI asociado a PM10. | float | AQI |
| `aqi_co` | Subíndice AQI asociado a CO. | float | AQI |
| `aqi_o3` | Subíndice AQI asociado a O3. | float | AQI |
| `aqi_no2` | Campo AQI del esquema asociado a NO2; estos equipos no tienen ese sensor. Excluido del análisis. | float | AQI |
| `quality_status` | Estado de calidad del registro, como `good` o `excellent`. No equivale a `aqi_category`. | string | calidad de datos |
| `quality_score` | Puntuación de calidad calculada por el proveedor; fórmula y criterios no confirmados. | float | calidad de datos |
| `data_completeness` | Indicador de completitud; confirmar escala y denominador antes de interpretarlo como porcentaje. | float | calidad de datos |
| `data_points` | Número de puntos reportados para el registro; viene como decimal aunque represente un conteo. | float | calidad de datos |
| `max_gap_seconds` | Intervalo máximo entre datos, en segundos según el nombre; método exacto de cálculo por confirmar. | float | calidad de datos |
| `battery_avg` | Estado medio de batería del registro horario, en %. | float | operación |
| `deviceID` | Identificador del dispositivo al que pertenece el registro. | string | operación |
| `fixed_gps` | Par textual con apariencia de latitud,longitud; sistema de referencia y procedimiento de fijación por confirmar. | string | geolocalización |
| `hour_timestamp_utc` | Instante de referencia del registro horario: segundos Unix en UTC, según la especificación suministrada. | float | tiempo |
| `fixed_gps_saved_at` | Campo adicional de apariencia temporal relacionado por nombre con el guardado de GPS; semántica y unidad por confirmar. | float | tiempo |
| `processed_at` | Campo adicional de apariencia temporal relacionado por nombre con procesamiento; semántica y unidad por confirmar. | float | tiempo |
| `ttl` | Campo adicional de posible gestión de vigencia; no se usa como fecha de medición ni se interpreta sin documentación. | float | operación |
| `mode` | Campo adicional de modo del equipo o procesamiento; significado de sus códigos no confirmado. | float | operación |

## Unidades e interpretación

- **Confirmado por las instrucciones de la API:** `hour_timestamp_utc` es un Unix timestamp en segundos UTC. Se convierte a `America/Guatemala` para interpretar patrones diarios. No confundas `processed_at` con la hora de medición.
- **Sugerido por el nombre:** `max_gap_seconds` está expresado en segundos; el cálculo exacto del hueco requiere documentación del proveedor.
- **Unidades confirmadas para estos equipos:** PM2.5 y PM10 en µg/m³; CO y O3 en ppb; temperatura en °C; humedad y batería en %. Las etiquetas no convierten ni escalan los datos.
- **Pendiente de confirmar:** escala de completitud, cálculo de puntuaciones de calidad y detalles del método de agregación.
- **AQI:** es un dato calculado por Smability. La metodología está pendiente de revisión y se documentará en una actualización posterior. Por ahora se identifican los campos, sin recalcularlos ni graficarlos y sin asumir una fórmula, un estándar o puntos de corte.
- **Ceros y ausencias:** un cero puede ser una medición, redondeo o una condición del canal. Sin documentación adicional no equivale a «contaminante ausente». Un valor nulo se representa como ausente; no se rellena con cero.
- **Calidad:** no se inventan umbrales de aceptación. Inspecciona conjuntamente estado, puntuación, completitud, conteo y hueco antes de describir un valor ambiental.

## Columnas derivadas en el workshop

| Columna | Cómo se obtiene | Tipo | Categoría |
|---|---|---|---|
| `fecha_utc` | `pd.to_datetime(df["hour_timestamp_utc"], unit="s", utc=True)` | datetime con zona UTC | tiempo |
| `fecha_guatemala` | `df["fecha_utc"].dt.tz_convert("America/Guatemala")` | datetime con zona America/Guatemala | tiempo |

Ambas representan el mismo instante. La conversión de zona no agrega ni resta tiempo a la medición: cambia su representación local. Para inspeccionar todos los campos, usa `print(df_completo.columns)` después de la selección, o `print(df.columns)` antes de ella.

## Diferencias con el JSON suministrado

La respuesta real incluyó los mismos campos del ejemplo y cuatro adicionales: `fixed_gps_saved_at`, `processed_at`, `ttl` y `mode`. Ambos dispositivos presentaron las mismas 34 claves. Variaron los valores, coordenadas, estados de calidad y número de registros (144 y 142); no se observó una diferencia de esquema entre los dos equipos.

El archivo educativo conserva cuatro registros reales de SMAA_006 y todos sus campos. Es un subconjunto con `hours=4`, no evidencia de que la API solo devolviera cuatro horas en siete días.
