import csv


def remover_acentos(texto):
    """
    Normaliza un texto convirtiendolo a minusculas y removiendo tildes basicas.

    Argumentos:
        texto (str): Cadena de texto a procesar.

    Retorna:
        str: Cadena de texto normalizada sin acentos y en minusculas.
    """
    texto_limpio = texto.lower()
    reemplazos = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u")
    )
    for con_tilde, sin_tilde in reemplazos:
        texto_limpio = texto_limpio.replace(con_tilde, sin_tilde)
    return texto_limpio


def solicitar_entero_positivo(mensaje_input):
    """
    Solicita una entrada por teclado y valida que sea un entero positivo.

    Argumentos:
        mensaje_input (str): El mensaje que se le muestra al usuario.

    Retorna:
        int: El numero entero positivo validado.
    """
    while True:
        try:
            valor = int(input(mensaje_input))
            if valor < 0:
                print("Error: El valor no puede ser un numero negativo.")
                continue
            return valor
        except ValueError:
            print("Error: Debe ingresar un numero entero valido.")


def cargar_datos(nombre_archivo):
    """
    Lee el archivo CSV y convierte cada fila en un diccionario de datos.

    Argumentos:
        nombre_archivo (str): Ruta del archivo CSV a leer.

    Retorna:
        list: Lista que contiene los diccionarios de cada pais.
    """
    lista_paises = []
    try:
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                pais = {
                    "nombre": fila["nombre"].strip(),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"].strip()
                }
                lista_paises.append(pais)
        print("Datos cargados con exito.")
        return lista_paises
    except FileNotFoundError:
        print(f"Alerta: No se encontro el archivo '{nombre_archivo}'.")
        print("Se iniciara con una lista vacia.")
        return []
    except (ValueError, KeyError):
        print("Error: El formato del archivo CSV es invalido o esta corrupto.")
        return []
def guardar_datos(nombre_archivo, lista_paises):
    """
    Sobrescribe el archivo CSV externo con la lista de datos actual.

    Argumentos:
        nombre_archivo (str): Ruta del archivo CSV donde se guardara.
        lista_paises (list): Lista de diccionarios con los datos actualizados.
    """
    try:
        with open(nombre_archivo, mode="w", encoding="utf-8", newline="") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(lista_paises)
        print("Cambios resguardados exitosamente en el archivo CSV.")
    except Exception:
        print("Error: No se pudieron resguardar los datos en el archivo.")


def agregar_pais(lista_paises):
    """
    Pide los datos de un pais y lo añade tras validar que no este duplicado.

    Argumentos:
        lista_paises (list): Lista de diccionarios donde se añadira el registro.
    """
    print("\n--- AGREGAR NUEVO PAÍS ---")
    nombre = input("Ingrese el nombre del país: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return

    for pais in lista_paises:
        if remover_acentos(pais["nombre"]) == remover_acentos(nombre):
            print(f"Error: El pais '{pais['nombre']}' ya existe.")
            return

    poblacion = solicitar_entero_positivo("Ingrese la población: ")
    superficie = solicitar_entero_positivo("Ingrese la superficie en km²: ")

    continente = input("Ingrese el continente: ").strip()
    if not continente:
        print("Error: El continente no puede estar vacío.")
        return

    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    lista_paises.append(nuevo_pais)
    print(f"Pais '{nombre}' agregado exitosamente en memoria.")
    guardar_datos("paises.csv", lista_paises)


def actualizar_pais(lista_paises):
    """
    Busca un pais por su nombre y modifica sus valores numericos asociados.

    Argumentos:
        lista_paises (list): Lista de diccionarios que contiene los registros.
    """
    print("\n--- ACTUALIZAR DATOS DE PAÍS ---")
    nombre_buscar = input("Ingrese el nombre a modificar: ").strip()
    if not nombre_buscar:
        print("Error: El nombre de búsqueda no puede estar vacío.")
        return

    pais_encontrado = None
    for pais in lista_paises:
        if remover_acentos(pais["nombre"]) == remover_acentos(nombre_buscar):
            pais_encontrado = pais
            break

    if pais_encontrado is None:
        print("Error: El país ingresado no se encuentra registrado.")
        return

    print(f"País seleccionado: {pais_encontrado['nombre']}")
    print(f"Población actual: {pais_encontrado['poblacion']}")
    print(f"Superficie actual: {pais_encontrado['superficie']} km²")

    nueva_pob = solicitar_entero_positivo("Ingrese la nueva población: ")
    nueva_sup = solicitar_entero_positivo("Ingrese la nueva superficie: ")

    pais_encontrado["poblacion"] = nueva_pob
    pais_encontrado["superficie"] = nueva_sup
    print(f"Datos de '{pais_encontrado['nombre']}' modificados con exito.")
    guardar_datos("paises.csv", lista_paises)


def calcular_metricas(lista_paises):
    """
    Procesa algoritmicamente los datos matematicos y de conteo de la lista.

    Argumentos:
        lista_paises (list): Lista de diccionarios a analizar.

    Retorna:
        tuple: Contiene mayor_pob, menor_pob, prom_pob, prom_sup, conteo_cont.
    """
    if not lista_paises:
        return None, None, 0, 0, {}

    total_pob = 0
    total_sup = 0
    
    # LINEAS CORREGIDAS: Se indexa el primer elemento de la lista de forma segura
    pais_mayor_pob = lista_paises[0]
    pais_menor_pob = lista_paises[0]
    conteo_continentes = {}

    for pais in lista_paises:
        total_pob += pais["poblacion"]
        total_sup += pais["superficie"]

        if pais["poblacion"] > pais_mayor_pob["poblacion"]:
            pais_mayor_pob = pais
        if pais["poblacion"] < pais_menor_pob["poblacion"]:
            pais_menor_pob = pais

        cont = pais["continente"]
        conteo_continentes[cont] = conteo_continentes.get(cont, 0) + 1

    cantidad_paises = len(lista_paises)
    promedio_pob = total_pob / cantidad_paises
    promedio_sup = total_sup / cantidad_paises

    return pais_mayor_pob, pais_menor_pob, promedio_pob, promedio_sup, conteo_continentes
