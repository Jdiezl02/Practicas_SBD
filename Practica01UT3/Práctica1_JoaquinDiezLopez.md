
#  Práctica 1
>La práctica 1 consiste en limpiar un csv para que no llenemos de nulos o datos sin valor a 
la inteligencia artificial que querramos entrenar.
## Paso 1

Importamos todas las librerias necesarias, y analizamos el dataset.
```
import pandas as pd
from datetime import datetime, timedelta
import re

print("Iniciando limpieza de Joaquin Diez Lopez...")

archivo_entrada = "ventas_big_data_ut3.csv"
df = pd.read_csv(archivo_entrada)

filas_iniciales = len(df)

print("\nInformación inicial del dataset:")
print(df.info())
```

## Paso 2

Quitamos los duplicados.
```
df_sin_dup = df.drop_duplicates()
duplicados_eliminados = filas_iniciales - len(df_sin_dup)
```

## Paso 3

Hacemos la mediana las cantidades negativas .
```
df_sin_dup["cantidad"] = pd.to_numeric(df_sin_dup["cantidad"], errors="coerce")

num_cantidades_negativas = (df_sin_dup["cantidad"] < 0).sum()

mediana_cantidad = df_sin_dup.loc[df_sin_dup["cantidad"] >= 0, "cantidad"].median()

df_sin_dup.loc[df_sin_dup["cantidad"] < 0, "cantidad"] = mediana_cantidad
```

## Paso 4

Normalizamos los productos.
```
def normalizar_producto(texto):
    if pd.isna(texto):
        return texto
    texto = texto.strip()
    return texto.title().replace(" ", "")

df_sin_dup["producto"] = df_sin_dup["producto"].apply(normalizar_producto)
```

## Paso 5

Convertimos los errores tipo "ERR" a NaN.
```
df_sin_dup["precio"] = pd.to_numeric(df_sin_dup["precio"], errors="coerce")
```

## Paso 6

Procesamos las fechas.
```
def procesar_fecha(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).lower().strip()
    hoy = datetime.now()

    if valor == "ayer":
        return (hoy - timedelta(days=1)).date().isoformat()

    match = re.search(r"hace (\d+) dias", valor)
    if match:
        dias = int(match.group(1))
        return (hoy - timedelta(days=dias)).date().isoformat()

    try:
        return pd.to_datetime(valor).date().isoformat()
    except:
        return None

df_sin_dup["fecha"] = df_sin_dup["fecha"].apply(procesar_fecha)
```

## Paso 7

Se exporta a un json.
```
def procesar_fecha(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).lower().strip()
    hoy = datetime.now()

    if valor == "ayer":
        return (hoy - timedelta(days=1)).date().isoformat()

    match = re.search(r"hace (\d+) dias", valor)
    if match:
        dias = int(match.group(1))
        return (hoy - timedelta(days=dias)).date().isoformat()

    try:
        return pd.to_datetime(valor).date().isoformat()
    except:
        return None

df_sin_dup["fecha"] = df_sin_dup["fecha"].apply(procesar_fecha)
```

## Paso 8

Y por ultimo mostramos la bitacora para ver que este todo bien.
```
print("\n===== BITÁCORA DE LIMPIEZA =====")
print(f"Total de filas iniciales: {filas_iniciales}")
print(f"Filas eliminadas por duplicidad exacta: {duplicados_eliminados}")
print(f"Mediana utilizada para precios: {mediana_precio}")
print(f"Registros con cantidades negativas descartados: {num_cantidades_negativas}")
print(f"Total de filas finales: {len(df_sin_dup)}")
print("Archivo generado:", archivo_salida)
```

Este es el resultado de la Bitácora de Limpieza y todo el programa:
```
PS C:\Users\jdiezl02\Documents\Visual\Practica01UT3> & C:/Users/jdiezl02/AppData/Local/Python/pythoncore-3.14-64/python.exe c:/Users/jdiezl02/Documents/Visual/Practica01UT3/practica01UT3.py
Iniciando limpieza de Joaquin Diez Lopez...

Información inicial del dataset:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 15451 entries, 0 to 15450
Data columns (total 5 columns):
 #   Column    Non-Null Count  Dtype 
---  ------    --------------  ----- 
 0   id        15451 non-null  int64 
 1   fecha     15451 non-null  object
 2   producto  15451 non-null  object
 3   precio    14677 non-null  object
 4   cantidad  15451 non-null  int64 
dtypes: int64(2), object(3)
memory usage: 603.7+ KB
None
c:\Users\jdiezl02\Documents\Visual\Practica01UT3\practica01UT3.py:22: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df_sin_dup["cantidad"] = pd.to_numeric(df_sin_dup["cantidad"], errors="coerce")
c:\Users\jdiezl02\Documents\Visual\Practica01UT3\practica01UT3.py:36: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df_sin_dup["producto"] = df_sin_dup["producto"].apply(normalizar_producto)
c:\Users\jdiezl02\Documents\Visual\Practica01UT3\practica01UT3.py:38: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df_sin_dup["precio"] = pd.to_numeric(df_sin_dup["precio"], errors="coerce")
c:\Users\jdiezl02\Documents\Visual\Practica01UT3\practica01UT3.py:40: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df_sin_dup["precio"].fillna(mediana_precio, inplace=True)
c:\Users\jdiezl02\Documents\Visual\Practica01UT3\practica01UT3.py:58: UserWarning: Parsing dates in %d/%m/%Y format when dayfirst=False (the default) was specified. Pass `dayfirst=True` or specify a format to silence this warning.
  return pd.to_datetime(valor).date().isoformat()
c:\Users\jdiezl02\Documents\Visual\Practica01UT3\practica01UT3.py:62: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df_sin_dup["fecha"] = df_sin_dup["fecha"].apply(procesar_fecha)

===== BITÁCORA DE LIMPIEZA =====
Total de filas iniciales: 15451
Filas eliminadas por duplicidad exacta: 451
Valores negativos en cantidad corregidos: 298
Mediana utilizada para cantidades: 6.0
Mediana utilizada para precios: 755.4100000000001
Total de filas finales: 15000
Archivo generado: ventas_limpias_Joaquin_Diez_Lopez.json
PS C:\Users\jdiezl02\Documents\Visual\Practica01UT3>
```

# Reflexión

>1. Se perdieron 451.

>2. No eliminado el id repetido si el contenido era distinto.

>3. Usar la mediana para reemplazar precios nulos garantiza que los datos imputados sean representativos del conjunto real de precios, evitando que un solo error manual distorsione toda la columna.

# Conclusión

Limpiar y normalizar los datos es importante para que los analisis no salgan mal y no tener duplicados ni cosas que no nos interesen.
