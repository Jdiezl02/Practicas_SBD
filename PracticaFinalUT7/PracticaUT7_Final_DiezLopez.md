# Informe de Inteligencia – Centro de la Alianza Shinobi

## Introducción

Este sistema ha sido desarrollado como una herramienta de análisis de datos orientada a la comparación de perfiles de jugadores. Su objetivo principal es identificar jugadores similares en base a su rendimiento, utilizando técnicas de normalización y cálculo de distancias.

La idea es poder encontrar “perfiles equivalentes” o sustitutos potenciales dentro del conjunto de datos, facilitando la toma de decisiones.

---

## Lógica de similitud

### Representación de los jugadores

Cada jugador se representa como un conjunto de variables numéricas que describen su rendimiento deportivo:

- Goles  
- Asistencias  
- Pases_%  
- Regates  
- Recuperaciones  
- Duelos_Aereos  
- xG  
- Potencial  

Estas variables forman un vector que permite comparar jugadores en un espacio multidimensional.

---

### Normalización de datos

Antes de realizar cualquier comparación, los datos se normalizan utilizando MinMaxScaler, transformando todas las variables a un rango entre 0 y 1.

Este paso es importante porque:

- Evita que variables con escalas grandes dominen el análisis  
- Permite comparar todas las métricas en igualdad de condiciones  
- Mejora la precisión del cálculo de similitud  

---

### Distancia euclidiana

La similitud entre jugadores se calcula mediante la distancia euclidiana, que mide la diferencia entre dos puntos en un espacio multidimensional.

La fórmula utilizada es:

\[
d(p, q) = \sqrt{\sum (q_i - p_i)^2}
\]

Donde:

- p representa el jugador objetivo  
- q representa un jugador candidato  
- i representa cada una de las variables  

Cuanto menor es la distancia, mayor es la similitud entre ambos jugadores.

---

### Proceso de comparación

El sistema sigue los siguientes pasos:

1. Se selecciona un jugador como referencia  
2. Se obtiene su vector de características normalizadas  
3. Se calcula la distancia con todos los jugadores del dataset  
4. Se ordenan los resultados de menor a mayor distancia  
5. Se seleccionan los cinco jugadores más similares  

---

## Especializaciones implementadas

### Rastreo de cantera

Esta funcionalidad permite identificar jugadores jóvenes con alto potencial.

Se aplica un filtro basado en dos condiciones:

- Edad menor o igual a 25 años  
- Potencial superior a 70  

El objetivo es detectar jugadores con capacidad de desarrollo futuro.

---

### Agrupamiento táctico (clustering)

Se ha implementado un modelo de clustering utilizando el algoritmo K-Means.

Este algoritmo agrupa jugadores en diferentes conjuntos en función de sus características de rendimiento.

Funcionamiento:

- Se utilizan las variables normalizadas  
- Se define un número de grupos (k = 4)  
- Cada jugador se asigna al cluster más cercano  

El objetivo es identificar perfiles de juego similares de forma automática.

---

## Visualización de resultados

El sistema ofrece diferentes representaciones para facilitar el análisis:

- Perfil del jugador mediante gráfico radar  
- Ranking de jugadores más similares  
- Agrupación en clusters tácticos  
- Filtro de jugadores jóvenes con potencial  

---

## Conclusión

Este sistema permite transformar datos deportivos en información útil para el análisis de rendimiento. A través de técnicas de normalización, distancia euclidiana y clustering, se pueden identificar patrones, similitudes entre jugadores y posibles talentos emergentes dentro del dataset.