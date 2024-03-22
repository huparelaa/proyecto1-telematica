# PROYECTO 1: SISTEMA DE ARCHIVOS DISTRIBUIDOS
### Integrantes:
* Julián David Valencia Restrepo.
* Hobarlan Uparela Arroyo.
* Andrés Prada Rodríguez.
## Marco teórico de los sistemas distribuidos de archivos por bloques y por objetos.
### Introducción
En la era actual de la informática, los sistemas distribuidos de archivos han sido cruciales por su capacidad para manejar datos eficientes y confiablemente. En un mundo donde la generación de datos se ha incrementado exponencialmente, gracias a internet y a la proliferación de dispositivos conectados, la necesidad de sistemas capaces de almacenar, procesar y recuperar grandes volúmenes de información es más crítica que nunca. Los sistemas distribuidos de archivos, como Google File System (GFS) y Hadoop Distributed File System (HDFS), son ejemplos sobresalientes de esta tecnología, proporcionando soluciones robustas para el almacenamiento y manejo de datos en entornos informáticos modernos.

Un sistema de archivos distribuido es un sistema que permite el almacenamiento de archivos en múltiples servidores o nodos, a diferencia de los sistemas de archivos tradicionales que se limitan a un solo dispositivo de almacenamiento. Estos sistemas están diseñados para ser altamente escalables, confiables y accesibles, permitiendo así la gestión eficiente de grandes conjuntos de datos distribuidos geográficamente. Además, facilitan el acceso concurrente a los datos por parte de múltiples usuarios o aplicaciones, mejorando significativamente el rendimiento y la disponibilidad. 

### Sistemas Distribuidos de Archivos por Bloques

Los sistemas distribuidos de archivos por bloques son aquellos que almacenan datos en unidades fijas conocidas como "bloques". En estos sistemas, cada archivo se divide en bloques, que se distribuyen y replican a través de una red de nodos. Esta estructura ofrece una forma eficiente y escalable de manejar grandes volúmenes de datos. 

Los sistemas distribuidos de archivos por bloques son aquellos que almacenan datos en unidades fijas conocidas como "bloques". En estos sistemas, cada archivo se divide en bloques, que se distribuyen y replican a través de una red de nodos. Esta estructura ofrece una forma eficiente y escalable de manejar grandes volúmenes de datos. 

Estos sistemas funcionan mediante la distribución de datos en múltiples nodos, lo que permite un procesamiento paralelo y un acceso rápido. Los componentes principales incluyen: 

* **Nodos de Datos**: Almacenan los bloques de datos. 

* **Nodo Maestro**: Gestiona la ubicación de los bloques y las operaciones sobre los archivos. 

* **Protocolos de Red**: Permiten la comunicación y transferencia de datos entre nodos. 

* **Aplicaciones y Ejemplos**:

* **Almacenamiento en la Nube**: Como en sistemas de procesamiento de datos a gran escala. 

* **Ejemplos**: Hadoop Distributed File System (HDFS), Google File System (GFS). 

### Sistemas Distribuidos de Archivos por Objetos

A diferencia de los sistemas por bloques, los sistemas de archivos por objetos gestionan los datos como "objetos", cada uno con un identificador único y metadatos que describen el contenido. 

Estos sistemas utilizan una estructura plana de almacenamiento donde cada objeto es independiente. Los objetos incluyen datos y metadatos, permitiendo una gestión más flexible y eficiente. 

* **Aplicaciones y Ejemplos**:
    Almacenamiento de objetos en la nube (por ejemplo, Amazon S3, Google Cloud Storage).
    Uso en sistemas de Big Data y análisis de datos distribuidos.

### Comparación entre Sistemas por Bloques y por Objetos

| Característica | Sistemas por Bloques	| Sistemas por Objetos |
|----------------|----------------------|---------------------|
| Modelo de datos | Organiza los datos en bloques de tamaño fijo  | Organiza los datos en objetos, cada uno con metadatos |
| Escalabilidad	 | Escalabilidad vertical limitada	| Escalabilidad horizontal y vertical |
| Latencia | Baja latencia en operaciones de lectura y escritura | Mayor latencia debido al acceso a través de metadatos |
| Tamaño de archivo máximo | Limitado por el tamaño del bloque | No hay limitación en el tamaño de los objetos |
| Operaciones | Eficiente para operaciones de lectura y escritura | Más eficiente para operaciones de lectura y objetos grandes |
| Metadatos | 	Almacenados en un sistema de metadatos separado | Almacenados junto con el objeto en sí |
| Consistencia | Mayor consistencia debido a la estructura de bloque | Puede haber mayor complejidad en la consistencia de datos |

* **Sistemas por Bloques**:

Son más apropiados cuando se requiere un acceso eficiente a datos secuenciales o cuando se trabaja con grandes volúmenes de datos que se leen o escriben en bloques.
Se utilizan comúnmente en aplicaciones de análisis de datos como Hadoop, donde se procesan grandes conjuntos de datos distribuidos en clústeres.

* **Sistemas por Objetos**:

Son más adecuados para aplicaciones que requieren una alta escalabilidad y flexibilidad en el acceso a los datos, como el almacenamiento en la nube, servicios de CDN (Content Delivery Network) y sistemas de Big Data.
Son ideales cuando se necesita almacenar grandes cantidades de datos no estructurados o semi-estructurados, como imágenes, videos, documentos y archivos de registro.

### Glosario
- **Sistema de Archivos Distribuido (DFS)**: Un sistema que permite el almacenamiento y acceso a archivos en múltiples servidores o nodos, mejorando la escalabilidad, confiabilidad y acceso concurrente a los datos.
- **NFS (Network File System)**: Un protocolo de sistema de archivos distribuido desarrollado por Sun Microsystems para permitir el acceso a archivos sobre una red de manera transparente.
- **AFS (Andrew File System)**: Un sistema de archivos distribuido que ofrece una gestión de archivos eficiente y segura, basada en un modelo de coherencia de caché.
- **SMB (Server Message Block)**, también conocido como CIFS (Common Internet File System): Un protocolo de compartición de archivos que permite a los usuarios acceder a archivos o impresoras en redes locales o sobre Internet.
- **Bloque**: La unidad de almacenamiento más pequeña en sistemas de archivos por bloques, que se distribuyen y replican a través de nodos en la red.
- **Objeto**: En sistemas de archivos por objetos, representa una unidad de datos que incluye el propio dato y metadatos, y tiene un identificador único.
- **NameNode**: En sistemas como HDFS, es el componente que gestiona el espacio de nombres del sistema de archivos y regula el acceso a los archivos por parte de los clientes.
- **DataNode**: Componente que almacena datos en un sistema de archivos distribuido, como HDFS, trabajando bajo la coordinación del NameNode.
- **Cliente**: Un usuario o aplicación que accede y opera sobre los archivos almacenados en el sistema de archivos distribuido.
- **WORM (Write Once, Read Many)**: Un enfoque de almacenamiento que permite la escritura de datos una sola vez y la lectura múltiple de estos sin permitir modificaciones.
- **API/SDK**: Conjunto de herramientas y protocolos que permiten la creación de aplicaciones que interactúan con el sistema de archivos distribuido.
- **CLI (Interfaz de Línea de Comandos)**: Una interfaz de usuario que permite a los usuarios interactuar con el sistema operativo o so
---
## Arquitectura
![ArquitecturaProyecto1](https://github.com/huparelaa/proyecto1-telematica/assets/81880485/03f2f639-53b2-454b-94f5-2f2f528bef76)

### 1. **Cliente <-> NameNode**: 
 El cliente realiza una petición por medio de API REST al NameNode para poder obtener las direcciones en donde se encuentran los DataNodes para poder escribir un archivo, o para obtener las distintas particiones que puede tener un archivo.

### 2. **NameNode <-> NameNode**: 

Un NameNode escribe en otro NameNode a forma de copia de seguridad el archivo que se le subió a este para así tener una mejor tolerancia a fallos. Está comunicación será por medio de API REST.

### 3. **NameNode <-> DataNode**: 

El NameNode indica al DataNode que archivos o particiones de estos tiene para que el NameNode le pueda proveer a los clients las direcciones en donde pueden subir o bien leer los archivos que buscan. Esta comunicación se hará por medio de API REST. 

### 4. **DataNode <-> NameNode**:

El DataNode indicará al NameNode la lista de DataNodes que tienen el archivo particionado. Esta comunicación se hará por medio de API REST. 

### 5. **Cliente <-> DataNode**:
El cliente por medio de gRPC se comunica con el o los DataNodes indicados por el NameNode para realizar escritura o lectura de archivos según desee.

### 6. **DataNode <-> DataNode**:

Cuando un DataNode recibe un archivo de parte de un cliente aparte de almacenarlo en sí mismo realiza una réplica hacia otro DataNode del sistema para aumentar la tolerancia a fallos al tener varias copias de un mismo archivo en distintas ubicaciones

## Conclusiones

En este estudio, hemos explorado dos tipos importantes de sistemas distribuidos de archivos: los sistemas por bloques y los sistemas por objetos. Al recapitular los puntos clave, se destaca que cada tipo de sistema tiene sus propias características distintivas, ventajas y desventajas.

Los sistemas por bloques son eficientes en el manejo de grandes volúmenes de datos que requieren un acceso secuencial y predecible. Son ideales para aplicaciones como el procesamiento de datos en clústeres y análisis de big data. Por otro lado, los sistemas por objetos ofrecen una mayor escalabilidad y flexibilidad en el acceso a los datos, lo que los hace más adecuados para aplicaciones en la nube, servicios de almacenamiento de objetos y distribución de contenido.

La importancia de los sistemas distribuidos de archivos en la computación moderna es innegable. Permiten el almacenamiento y acceso eficiente a grandes cantidades de datos distribuidos en entornos heterogéneos y a través de redes de comunicación. Estos sistemas son la columna vertebral de muchas aplicaciones críticas, desde el análisis de big data hasta el almacenamiento de contenido multimedia en la nube, y su desarrollo continuo es esencial para satisfacer las crecientes demandas de la era digital.

### Referencias
* [Google File System
](https://es.wikipedia.org/wiki/Google_File_System)
* [Hadoop Distributed File System
](https://es.wikipedia.org/wiki/Hadoop_Distributed_File_System)
* The Google File System - Sanjay Ghemawat, Howard Gobioff & Shun-Tak Leung
* The Hadoop Distributed File System - Konstantin Shvachko, Hairong Kuang, Sanjay Radia, Robert Chansler
