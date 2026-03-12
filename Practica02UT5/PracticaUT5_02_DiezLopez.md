
#  Práctica 2

# Modelo de Datos
## 1 Creación de la Tabla Principal

>Creamos la tabla
![alt text](image.png)

## 2 Ingesta de Dados Críticos

>Nos vamos a createitem y cremos un item
![alt text](image-1.png) 

>Creamos 5 diferentes
![alt text](image-2.png)

## 3 Simulación de Búsqueda ANBU

>Query buscando por un ID_Ninja específico
![alt text](image-3.png)

>Scan buscando a todos los ninjas de un “Clan” específico
![alt text](image-4.png)

## 4 Actualización Dinámica

>Modifico un registro existente añadiendo un atributo nuevo llamado Nivel_Amenaza
![alt text](image-5.png)

# Análisis Técnico
>Partition Key: Es el atributo que organiza los datos. Si buscas mucho por “Aldea”, conviene usar Aldea como Partition Key para consultas rápidas.

>Global Secondary Index (GSI): Es un índice adicional que permite buscar por otros atributos distintos de la clave principal, sin modificar la tabla.

# Captura
![alt text](image-6.png)

# Adicional
>Creamos una copia de uno nuestro y lo exportamos al gold con los filtros aplicados en csv.
![alt text](image-7.png)

>Importamos en el csv filtrado.
![alt text](image-8.png)
![alt text](image-9.png)
![alt text](image-10.png)

>Y ya lo hemos creado pero da error.
![alt text](image-11.png)