
#  Práctica 1
>La práctica 1 consiste en limipiar el registros_misiones y hacer una busqueda.
## Paso 1

Importamos todas las librerias necesarias.
```
import pandas as pd
```

## Paso 2

Creamos el metodo limpiar_registro() y limpiamos el csv.
```
def limpiar_registro(df):
    """
    Reto 1: Elimina filas duplicadas.
    Reto 2: Estandariza la columna 'aldea' (quitar espacios, solventar mayúsculas/minúsculas).
    Reto 3: Si 'nin_id' es nulo y la 'aldea' es 'Kiri', rellena con 'Ninja de la Niebla Anonimo'.
    Reto 4: Convierte 'ts' a datetime.
    Reto 5: Filtra o corrige niveles de chakra imposibles (<= 0 o > 100.000).
    Reto 6: Renombra las columnas:
            'id_reg' -> 'ID', 'ts' -> 'Fecha', 'nin_id' -> 'Ninja', 'status' -> 'Estado', 'desc' -> 'Descripcion'
    """
    # Reto 1: Elimina filas duplicadas
    duplicados = df.duplicated().sum()
    print(f"Clones detectados y eliminados: {duplicados}")
    df = df.drop_duplicates()

    # Reto 2: Estandariza la columna 'aldea'
    df['aldea'] = df['aldea'].astype(str).str.strip().str.title()

    # Reto 3: Rellena ninjas anónimos de Kiri
    condicion = df['nin_id'].isna() & (df['aldea'] == 'Kiri')
    df.loc[condicion, 'nin_id'] = 'Ninja de la Niebla Anonimo'

    # Reto 4: Convierte 'ts' a datetime
    df['ts'] = pd.to_datetime(df['ts'], errors='coerce')

    # Reto 5: Control de chakra
    antes = len(df)
    df = df[(df['chakra'] > 0) & (df['chakra'] <= 100000)]
    despues = len(df)
    print(f"Registros eliminados por chakra imposible: {antes - despues}")

    # Reto 6: Renombrar columnas
    df = df.rename(columns={
        'id_reg': 'ID',
        'ts': 'Fecha',
        'nin_id': 'Ninja',
        'status': 'Estado',
        'desc': 'Descripcion'
    })

    return df
```

## Paso 3

Ahora buscamos espía,sospechoso y enemigo y hacemos los demas retos.
```
def realizar_consultas(df):
    """
    Reto 7: Busca descripciones con las palabras 'espía', 'sospechoso' o 'enemigo'.
    Reto 8: Filtra ninjas de la 'Aldea de la Lluvia' (Amegakure) con chakra > 5000 y rango != 'D'.
    Reto 9: Encuentra los accesos ocurridos de madrugada (entre las 23:00 y las 05:00).
    Reto 10: Obtén el Top 5 ninjas con más chakra de cada aldea.
    Reto 11: Lista misiones de ninjas que NO pertenecen a la alianza (Konoha, Suna, Kumo).
    Reto 12: Cuenta cuántas misiones de estado 'Fallo' hay por cada aldea.
    """
    print("\n--- PALABRAS CLAVE SOSPECHOSAS ---")
    amenazas = df[df['Descripcion'].str.contains('espía|sospechoso|enemigo', case=False, na=False)]
    print(amenazas.head())

    print("\n--- INFILTRADOS DE AMEGAKURE ---")
    lluvia = df[
        (df['aldea'].str.contains('Lluvia|Amegakure', case=False, na=False)) &
        (df['chakra'] > 5000) &
        (df['rango'] != 'D')
    ]
    print(lluvia.head())

    print("\n--- MOVIMIENTOS DE MADRUGADA ---")
    madrugada = df[(df['Fecha'].dt.hour >= 23) | (df['Fecha'].dt.hour <= 5)]
    print(madrugada.head())

    print("\n--- TOP 5 NINJAS POR ALDEA ---")
    top_ninjas = df.sort_values('chakra', ascending=False).groupby('aldea').head(5)
    print(top_ninjas[['aldea', 'Ninja', 'chakra']])

    print("\n--- NINJAS FUERA DE LA ALIANZA ---")
    extranjeros = df[~df['aldea'].isin(['Konoha', 'Suna', 'Kumo'])]
    print(extranjeros.head())

    print("\n--- MAPA DE FALLOS POR ALDEA ---")
    fallos = df[df['Estado'] == 'Fallo'].groupby('aldea').size()
    print(fallos)
```

## Paso 4

hacemos que se ejecuten los metodos y guardamos el csv limipo.
```
# --- EJECUCIÓN ---
df_limpio = limpiar_registro(df)
realizar_consultas(df_limpio)

# Guardado final obligatorio
df_limpio.to_csv('misiones_limpias_JoaquinDiezLopez.csv', index=False)
print("\n📜 Pergamino restaurado guardado como misiones_limpias_JoaquinDiezLopez.csv")
```

## Preguntas de reflexión

>1.46 registros duplicados, pues que daria errores y sesgos si lo usaramos para entrenar una ia.
>2.Los valores en texto no permiten filtrar correctamente por horas, minutos o días.
>3.Se eliminaron porque no puede ser aunque yo creo que si tuviera a kurama si podria tener eso.

## Conclusión

>Te facilita mucho la busqueda al hacerla y ya tenerla para proximas busquedas.

