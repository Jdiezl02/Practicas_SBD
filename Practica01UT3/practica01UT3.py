import pandas as pd
from datetime import datetime, timedelta
import re
import os

print("Iniciando limpieza de Joaquin Diez Lopez...")

archivo_entrada = "ventas_big_data_ut3.csv"

if not os.path.exists(archivo_entrada):
    raise FileNotFoundError(f"No se encuentra el archivo: {archivo_entrada}")

df = pd.read_csv(archivo_entrada)
filas_iniciales = len(df)

print("\nInformación inicial del dataset:")
print(df.info())

df_sin_dup = df.drop_duplicates()
duplicados_eliminados = filas_iniciales - len(df_sin_dup)

df_sin_dup["cantidad"] = pd.to_numeric(df_sin_dup["cantidad"], errors="coerce")

num_cantidades_negativas = (df_sin_dup["cantidad"] < 0).sum()

mediana_cantidad = df_sin_dup.loc[df_sin_dup["cantidad"] >= 0, "cantidad"].median()

df_sin_dup.loc[df_sin_dup["cantidad"] < 0, "cantidad"] = mediana_cantidad

def normalizar_producto(texto):
    if pd.isna(texto):
        return texto
    texto = texto.strip()
    return texto.title().replace(" ", "")

df_sin_dup["producto"] = df_sin_dup["producto"].apply(normalizar_producto)

df_sin_dup["precio"] = pd.to_numeric(df_sin_dup["precio"], errors="coerce")
mediana_precio = df_sin_dup["precio"].median()
df_sin_dup["precio"].fillna(mediana_precio, inplace=True)

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


archivo_salida = "ventas_limpias_Joaquin_Diez_Lopez.json"
df_sin_dup.to_json(archivo_salida, orient="records", indent=4, force_ascii=False)

print("\n===== BITÁCORA DE LIMPIEZA =====")
print(f"Total de filas iniciales: {filas_iniciales}")
print(f"Filas eliminadas por duplicidad exacta: {duplicados_eliminados}")
print(f"Valores negativos en cantidad corregidos: {num_cantidades_negativas}")
print(f"Mediana utilizada para cantidades: {mediana_cantidad}")
print(f"Mediana utilizada para precios: {mediana_precio}")
print(f"Total de filas finales: {len(df_sin_dup)}")
print("Archivo generado:", archivo_salida)
