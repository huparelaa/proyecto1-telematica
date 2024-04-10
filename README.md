# ST0263 - Tópicos Especiales de Telemática
#
## Integrantes:
- Hobarlan Uparela Arroyo (huparelaa@eafit.edu.co)
- Julian David Valencia Restrepo (jdvalencir@eafit.edu.co)
- Andres Prada Rodriguez (apradar@eafit.edu.co)

## Profesor
- **Nombre:** Edwin Nelson Montoya Munera
- **Correo:** emontoya@eafit.edu.co

# Proyecto 1 (Sistema de archivos distribuidos)

## 1. breve descripción de la actividad

La actividad consiste en desarrollar un sistema de almacenamiento distribuido basado en un modelo de arquitectura cliente-servidor utilizando Python para los datanodes y el cliente, FastAPI para el namenode y Docker para todo el tema de contenerización. El sistema está compuesto por un NameNode y varios DataNodes que se comunican entre sí mediante gRPC y se encargan de almacenar y gestionar archivos de manera distribuida. El objetivo es implementar las funcionalidades básicas de un sistema de almacenamiento distribuido, incluyendo la replicación de datos, el manejo de la disponibilidad de nodos y la gestión de errores. El desarrollo se realizará siguiendo buenas prácticas de programación y utilizando contenedores Docker para facilitar el despliegue y la gestión del sistema.

### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Aspectos cumplidos de la actividad propuesta por el profesor:

* Implementación del sistema de archivos distribuido, incluyendo funciones como mkdir, cd y ls para la gestión de directorios.
* Desarrollo del cliente para realizar peticiones al NameNode y obtener la ubicación de los bloques de archivos.
* Implementación del NameNode para gestionar las solicitudes del cliente, incluyendo la ubicación de bloques y la información sobre su almacenamiento.
* Implementación de las funcionalidades de escritura (write) y lectura (read) de archivos en el sistema distribuido.
* Se implemento la función del editlog para registrar todas las creaciones de archivos y directorios.

### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

* La funcionalidad de append de archivos texto.

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

* Componentes Principales:
* Cliente: Aplicación de cliente escrita en Python.
* Namenode: Servidor central que gestiona el sistema de archivos distribuidos.
* Datanode(s): Nodos de almacenamiento distribuido que contienen las particiones de los archivos.

* Patrones Utilizados
* Modelo Cliente-Servidor: Se implementa un modelo cliente-servidor donde el cliente solicita información al servidor (Namenode) y se conecta directamente con los nodos de datos (Datanodes) para realizar operaciones de lectura y escritura.
* API RESTful: La comunicación entre el cliente y el Namenode se realiza utilizando principios de una API RESTful para la transmisión de información sobre la ubicación de las particiones de los archivos.
* Patrón de Acceso Directo a Datanode: Para maximizar la eficiencia en la transferencia de datos, el cliente se conecta directamente al Datanode via grpc para obtener o enviar archivos.

* Mejores Prácticas Utilizadas
* Escalabilidad: El diseño del DFS se ha concebido para ser escalable, permitiendo la adición de nuevos Datanodes para aumentar la capacidad de almacenamiento y la distribución de la carga.
* Tolerancia a Fallos: Se han implementado mecanismos de tolerancia a fallos para garantizar la disponibilidad y la integridad de los datos, como la replicación de particiones de archivos en múltiples Datanodes.
* Optimización de Transferencia de Datos: Se ha optimizado el proceso de transferencia de datos mediante el acceso directo a los Datanodes, minimizando la latencia y maximizando el rendimiento del sistema.

![ArquitecturaProyecto1](https://github.com/huparelaa/proyecto1-telematica/assets/81880485/03f2f639-53b2-454b-94f5-2f2f528bef76)

### 1. Plan de partición de archivos:

Para realizar la partición de archivos en bloques de tamaño 1 MB, utilizaremos un enfoque iterativo que divide el archivo en partes iguales del tamaño especificado. Estas partes serán nombradas como par000x, donde 'x' representa el número secuencial de la parte.

### 2.Mantenimiento de la red:

Utilizaremos Docker para crear contenedores independientes para cada uno de los servicios, como el NameNode y los DataNodes. 

### 3.Mantenimiento del directorio:

Crearemos un volumen en Docker para mantener el directorio compartido donde se almacenarán los bloques de archivos. Este volumen estará montado en cada uno de los contenedores para que puedan acceder y manipular los archivos de manera coherente.
Transmisión y recepción de bloques reales vía gRPC entre el 

### 4.Cliente y los DataNodes:

Implementaremos transmisión y recepción de bloques reales entre el cliente y los DataNodes utilizando gRPC. Esto permitirá una comunicación eficiente y segura entre los distintos componentes del sistema distribuido.

### 5.Estrategia de victoria temprana: transmisión y recepción en serie:

Para maximizar la eficiencia de la transmisión y recepción de bloques, implementaremos un mecanismo de transmisión y recepción en serie en lugar de paralelo. Esto permitirá una mejor gestión de los recursos y evitará problemas de concurrencia.

## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

#### Namenode:
- **Lenguaje de Programación:** Python
- **Librerías y Paquetes:** Incluidas en el archivo requirements.txt de la carpeta `src/namenode/`
- **Cómo Compilar y Ejecutar:**
    - Se deben instalar las dependencias de src/namenode/requirements.txt
    - Luego se debe correr el namenode con el comando `uvicorn Main:app --reload`

#### Datanode:
- **Lenguaje de Programación:** Python
- **Librerías y Paquetes:** Incluidas en el archivo requirements.txt de la carpeta `src/datanode/`
- **Cómo Compilar y Ejecutar:**
    - Se deben instalar las dependencias de src/datanode/requirements.txt
    - Luego se debe correr el namenode con el comando `python server.py` con lo que ya se conectará nuestro datanode al namenode

#### Client
- **Lenguaje de Programación:** Python
- **Librerías y Paquetes:** Incluidas en el archivo requirements.txt de la carpeta 'cli' 
- **Cómo Compilar y Ejecutar:**
    - Se deben instalar las dependencias de src/cli/src/requirements.txt
    - Luego de eso configura la IP Y el puerto del NameNode, esto se encuentra en el .env, también puedes cambiar el tamaño de las particiones si lo deseas.
    - Verás que dentro de la carpeta cli existe la carpeta 'uploads', dentro de esta se deben cargar los archivos que queremos enviar a nuestro sistema de archivos Hadoop.
    - Luego navegar hasta src/cli/src y allí ejecutar el comando ```python client.py```.



## Descripción y como se configura los parámetros del proyecto 

* Para configurar los parámetros del proyecto se hace directamente desde el archivo .env

## Detalles de la organización del código por carpetas o descripción de algún archivo. 
```
src
│   ├── cli
│   │   ├── downloads
│   │   ├── src
│   │   │   ├── client.py
│   │   │   ├── commands
│   │   │   │   ├── cli_commands.py
│   │   │   │   └── __init__.py
│   │   │   ├── connection
│   │   │   │   ├── dataNodeConn.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── nameNodeConn.py
│   │   │   ├── filetransfer_pb2_grpc.py
│   │   │   ├── filetransfer_pb2.py
│   │   │   ├── proto
│   │   │   │   └── filetransfer.proto
│   │   │   ├── README.md
│   │   │   ├── requirements.txt
│   │   │   ├── splits
│   │   │   └── utils
│   │   │       ├── filemanager.py
│   │   │       └── __init__.py
│   │   └── uploads
│   ├── dataNode
│   │   ├── dockerfile
│   │   ├── files
│   │   ├── filetransfer
│   │   │   ├── FileTransferServicer.py
│   │   │   ├── __init__.py
│   │   │   ├── replication.py
|   │   │   └── servicer.py
│   │   ├── filetransfer_pb2_grpc.py
│   │   ├── filetransfer_pb2.py
│   │   ├── protos
│   │   │   ├── filetransfer.proto
│   │   │   └── __init__.py
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── server.py
│   │   ├── services
│   │   │   ├── auth.py
│   │   │   ├── handshake.py
│   │   │   ├── __init__.py
│   │   │   └── scheduler.py
│   │   └── utils
│   │       ├── heartbeat.py
│   │       ├── __init__.py
│   │       └── utils.py
│   └── namenode
│       ├── DirectoryTree.py
│       ├── dockerfile
│       ├── editlog.txt
│       ├── fsimage
│       │   └── fsimage.json
│       ├── Main.py
│       ├── NameNode.py
│       ├── README.md
│       ├── requirements.txt
│       └── schemas
│           ├── fileName.py
│           ├── fileWriteRequest.py
│           ├── handshake.py
│           ├── heartbeat.py
│           ├── __init__.py
│           └── routeRequest.py
└──
``` 

## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

Se utilizó Docker para contenerizar el namenode y los diferentes datanodes. Además se crean volumenes para persistir los datos de los bloques en el sistema de archivos de la VM.

## IP o nombres de dominio en nube o en la máquina servidor.

![Screenshot from 2024-04-09 23-41-31](https://github.com/huparelaa/proyecto1-telematica/assets/88250984/8ac1241b-2cc6-494e-a1f5-2ab02af1e7a5)

Aquí tenemos el namenode que registra todos los moviemientos de los usuarios en el sistema de archivos distribuido. Tenemos tres datanodes que nos permiiten almacenar los bloques correspondientes con un factor de replicación de 3.

## Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

**Antes de iniciar con este proceso, confirmar si en cada una de las maquinas virtuales se tiene docker**

Para el cliente se debe cambiar la IP que se está utilizando para el namenode, por ejemplo:

```bash
NAMENODE_IP="127.0.0.1"
NAMENODE_PORT="8000"
BLOCK_SIZE="1048576" #1 MB
#BLOCK_SIZE="134217728" #128 MB
```

En este apartado, para el namenode debemos configurar lo siguiente: 

```yml
 services:
  namenode:
    image: julianv08/proyecto1-telematica-namenode
    container_name: namenode
    ports:
      - "8000:8000"
    volumes:
      - /home/user/namenode/fsimage/fsimage.json:/app/fsimage/fsimage.json
      - /home/user/namenode/editlog.txt:/app/editlog.txt
```

Se puede personalizar el puerto deseado y la ruta donde se creará el volumen en la maquina host del contendor.

**Se recomienda el uso de IP elastica para el namenode**

Para el datanode: 


```yml
services:
   datanode:
    image: julianv08/proyecto1-telematica-datanode
    ports:
      - "50051:50051"  # You can change the ports as needed
    environment:
      - NAMENODE_IP=127.0.0.0
      - NAMENODE_PORT=8000
      - MY_IP=127.0.0.1
    volumes:
      - /home/jdvalencir/datanode1:/app/files
```

Aquí demos de configurar las variables de entorno con los valores adecuados.

### 1. **¿Cómo se lanza el namenode?**:

El namenode, en un entorno de producción se lanza con el siguiente comando: 

```bash
sudo docker compose up 
```


### 2. **¿Cómo se lanza el datanode?**:

```bash
sudo docker compose up 
```

Con esta implementación nos aseguramos un fácil y rápido despliegue. Con esta implementación podemos asegurarnos de lanzar tantos datanodes como se requieran.

#### 1. Asegurarse que el namenode y los datanodes estén funcionando de manera adecuada

#### 2. Se debe encender el cliente para interacturar con el sistemas de archivos distribuido.

#### 3. Con está cuestión activada, podemos realizar las siguientes operaciones: 

* **ls:** Lista archivos y directorios en nuestra ruta actual.
* **mkdir:** Crea una nueva carpeta en la ruta donde estamos.
* **cd:** Permite navegar entre directorios, para usarlo debes escribir `cd folder` o si quieres retroceder `cd ..`
* **write:** Sube un archivo de la carpeta uploads al sistema de archivos Hajoop además de que lo registra en el directorio del namenode para posteriormente poder descargar este archivo.
* **read:** Lee el archivo en el directorio actual y guarda el archivo ya restaurado en la carpeta `downloads`.
* **clear:** Limpia la terminal

## Resultados o pantallazos 

* Video que muestra como se ejecuta el software: https://youtu.be/93eSnqCkI-U


### Referencias
* [Google File System](https://es.wikipedia.org/wiki/Google_File_System)
* [Hadoop Distributed File System](https://es.wikipedia.org/wiki/Hadoop_Distributed_File_System)
* **The Google File System - Sanjay Ghemawat, Howard Gobioff & Shun-Tak Leung**
* **The Hadoop Distributed File System - Konstantin Shvachko, Hairong Kuang, Sanjay Radia, Robert Chansler**
