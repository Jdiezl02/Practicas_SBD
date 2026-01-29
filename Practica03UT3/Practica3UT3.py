import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def extraer_datos_criptomonedas():
    """
    Función principal que extrae los datos de las 500 primeras criptomonedas
    de CoinMarketCap y los guarda en un archivo CSV.
    """
    
    # Configuración inicial
    url_base = "https://coinmarketcap.com/?page={}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Lista para almacenar todos los datos
    datos_criptomonedas = []
    
    for pagina in range(1, 35):
        print(f"Extrayendo datos de la página {pagina}...")
        
        # Construimos la URL de la página actual
        url = url_base.format(pagina)
        
        try:
            # Realizamos la petición HTTP con headers para simular navegador
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verificamos que la petición fue exitosa
            
            # Parseamos el contenido HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscamos la tabla principal que contiene las criptomonedas
            # CoinMarketCap usa una tabla con clase específica
            tabla = soup.find('table', {'class': 'sc-14cb040a-3 dsflYb cmc-table'})
            
            if not tabla:
                # Si no encuentra con esa clase, buscamos alternativas
                tabla = soup.find('table', {'class': 'cmc-table'})
            
            if tabla:
                # Obtenemos todas las filas del cuerpo de la tabla
                filas = tabla.find('tbody').find_all('tr')
                
                # Procesamos cada fila (cada criptomoneda)
                for fila in filas:
                    datos_fila = extraer_datos_fila(fila)
                    if datos_fila:  # Solo agregamos si se extrajeron datos válidos
                        datos_criptomonedas.append(datos_fila)
            
            # Pausa entre peticiones para evitar bloqueos
            time.sleep(2)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a la página {pagina}: {e}")
            continue
        except Exception as e:
            print(f"Error inesperado en la página {pagina}: {e}")
            continue
    
    # Creamos DataFrame con los datos recolectados
    df = pd.DataFrame(datos_criptomonedas)
    
    # Guardamos en archivo CSV
    if not df.empty:
        df.to_csv('cripto_data.csv', index=False, encoding='utf-8')
        print(f"\n✅ Extracción completada exitosamente!")
        print(f"📊 Total de criptomonedas extraídas: {len(df)}")
        print(f"💾 Datos guardados en: cripto_data.csv")
        
        # Mostramos un resumen de los datos
        print("\n📈 Resumen de datos extraídos:")
        print(df.head())
    else:
        print("❌ No se pudieron extraer datos. Verifica la estructura de la página.")

def extraer_datos_fila(fila):
    """
    Extrae los datos específicos de una fila de la tabla.
    
    Args:
        fila: Objeto BeautifulSoup que representa una fila de la tabla
    
    Returns:
        Diccionario con los datos de la criptomoneda o None si hay error
    """
    try:
        # Obtenemos todas las celdas de la fila
        celdas = fila.find_all('td')
        
        if len(celdas) < 10:  # Validación básica de estructura
            return None
        
        # 1. Nombre y Símbolo (generalmente en la segunda celda)
        nombre_celda = celdas[2] if len(celdas) > 2 else celdas[1]
        
        # Buscamos elementos que contengan nombre y símbolo
        nombre_elemento = nombre_celda.find('p', class_=lambda x: x and ('name' in str(x).lower() or 'sc-' in str(x)))
        simbolo_elemento = nombre_celda.find('p', class_=lambda x: x and ('coin-item-symbol' in str(x).lower() or 'sc-' in str(x)))
        
        nombre = nombre_elemento.text.strip() if nombre_elemento else "No disponible"
        simbolo = simbolo_elemento.text.strip() if simbolo_elemento else "No disponible"
        
        # 2. Precio actual (generalmente en la 4ta o 5ta columna)
        precio_celda = celdas[3] if len(celdas) > 3 else None
        if not precio_celda or precio_celda.text.strip() == '--':
            precio_celda = celdas[4] if len(celdas) > 4 else None
        
        precio = limpiar_valor_monetario(precio_celda.text.strip() if precio_celda else "0")
        
        # 3. Market Cap (capitalización de mercado)
        market_cap_celda = celdas[7] if len(celdas) > 7 else None
        if not market_cap_celda or market_cap_celda.text.strip() == '--':
            market_cap_celda = celdas[6] if len(celdas) > 6 else None
        
        market_cap = limpiar_valor_monetario(market_cap_celda.text.strip() if market_cap_celda else "0")
        
        # 4. Volumen (24 horas)
        volumen_celda = celdas[8] if len(celdas) > 8 else None
        if not volumen_celda or volumen_celda.text.strip() == '--':
            volumen_celda = celdas[7] if len(celdas) > 7 else None
        
        volumen = limpiar_valor_monetario(volumen_celda.text.strip() if volumen_celda else "0")
        
        # Creamos diccionario con los datos extraídos
        return {
            'Nombre': nombre,
            'Símbolo': simbolo,
            'Precio_USD': precio,
            'Market_Cap_USD': market_cap,
            'Volumen_24h_USD': volumen
        }
        
    except Exception as e:
        print(f"Error al procesar fila: {e}")
        return None

def limpiar_valor_monetario(valor_str):
    """
    Convierte un valor monetario en texto a un número float.
    Elimina símbolos de moneda, comas y convierte abreviaciones.
    
    Args:
        valor_str: String con el valor monetario (ej: "$90,452.12" o "$1.2B")
    
    Returns:
        float con el valor numérico
    """
    try:
        if not valor_str or valor_str == '--':
            return 0.0
        
        # Eliminamos el símbolo de dólar y espacios
        valor_limpio = valor_str.replace('$', '').replace(',', '').strip()
        
        # Manejo de abreviaciones (B = Billones, M = Millones, K = Miles)
        multiplicador = 1
        if valor_limpio.endswith('B'):
            multiplicador = 1000000000  # Mil millones
            valor_limpio = valor_limpio[:-1]
        elif valor_limpio.endswith('M'):
            multiplicador = 1000000  # Millones
            valor_limpio = valor_limpio[:-1]
        elif valor_limpio.endswith('K'):
            multiplicador = 1000  # Miles
            valor_limpio = valor_limpio[:-1]
        
        # Convertimos a float y aplicamos multiplicador
        return float(valor_limpio) * multiplicador
        
    except ValueError:
        return 0.0

def verificar_estructura_pagina():
    """
    Función de diagnóstico para verificar la estructura actual de CoinMarketCap.
    Útil si el scraping principal falla debido a cambios en la página.
    """
    print("🔍 Verificando estructura de la página...")
    
    url = "https://coinmarketcap.com/?page=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscamos todas las tablas
        tablas = soup.find_all('table')
        print(f"Encontradas {len(tablas)} tablas en la página")
        
        for i, tabla in enumerate(tablas):
            print(f"\n📊 Tabla {i+1}:")
            print(f"   Clases: {tabla.get('class', ['Sin clase'])}")
            
            # Buscamos filas de ejemplo
            filas = tabla.find_all('tr')
            if filas:
                print(f"   Número de filas: {len(filas)}")
                if len(filas) > 1:
                    # Mostramos contenido de la primera fila
                    primera_fila = filas[1]  # Índice 1 para evitar encabezado
                    celdas = primera_fila.find_all(['td', 'th'])
                    print(f"   Celdas en primera fila: {len(celdas)}")
                    for j, celda in enumerate(celdas[:3]):  # Solo primeras 3 celdas
                        print(f"   Celda {j}: {celda.text.strip()[:50]}...")
        
        return tablas
        
    except Exception as e:
        print(f"Error en verificación: {e}")
        return []

if __name__ == "__main__":
    print("=" * 60)
    print("PRÁCTICA 3: EXTRACCIÓN DE DATOS EN COINMARKETCAP")
    print("=" * 60)
    print("\n🔧 Iniciando proceso de extracción...")
    
    # Ejecutamos la extracción principal
    extraer_datos_criptomonedas()
    
    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO")
    print("=" * 60)
    
    # Opcional: Descomentar para verificar estructura si hay problemas
    # print("\n📋 Verificación de estructura (opcional):")
    # verificar_estructura_pagina()