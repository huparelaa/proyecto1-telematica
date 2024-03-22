import os

def dividir_archivo_en_hadoop_style(nombre_archivo, tamano_bloque=1024*1024):  # 1MB por defecto
    base_nombre_archivo = os.path.splitext(os.path.basename(nombre_archivo))[0] +os.path.splitext(os.path.basename(nombre_archivo))[1]
    directorio_destino = f"{base_nombre_archivo}-"
    print(directorio_destino)
    
    # Crea el directorio si no existe
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    bloque_num = 1
    with open(nombre_archivo, 'rb') as archivo:
        bloque = archivo.read(tamano_bloque)
        while bloque:
            nombre_parte = f"{directorio_destino}/part{bloque_num:04d}"
            with open(nombre_parte, 'wb') as archivo_parte:
                archivo_parte.write(bloque)
            print(f"Se creó el bloque {nombre_parte}")
            bloque_num += 1
            bloque = archivo.read(tamano_bloque)

if __name__ == "__main__":
    nombre_archivo = "r1ck.mp4"  # Reemplaza esto con el nombre de tu archivo
    tamano_bloque = 1024 * 1024  # Por ejemplo, para bloques de 64MB
    dividir_archivo_en_hadoop_style(nombre_archivo, tamano_bloque)
