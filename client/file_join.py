import os

def unir_archivos_divididos(directorio_dividido, nombre_archivo_destino):
    """
    Une los archivos divididos, previamente almacenados en un directorio, en un solo archivo.

    :param directorio_dividido: El directorio donde se almacenan los archivos divididos.
    :param nombre_archivo_destino: El nombre del archivo reconstruido.
    """
    partes = sorted(os.listdir(directorio_dividido))
    with open(nombre_archivo_destino, 'wb') as archivo_destino:
        for parte in partes:
            path_parte = os.path.join(directorio_dividido, parte)
            with open(path_parte, 'rb') as archivo_parte:
                archivo_destino.write(archivo_parte.read())
            print(f"Se agregó la parte {parte} al archivo {nombre_archivo_destino}")

if __name__ == "__main__":
    # Asumiendo que dividiste el archivo r1ck.mp4 y quieres reconstruirlo
    directorio_dividido = "r1ck.mp4-"
    nombre_archivo_destino = "r1ck_reconstruido.mp4"
    unir_archivos_divididos(directorio_dividido, nombre_archivo_destino)
