import csv

# =====================================================================
#                  CAPA DE FUNCIONES AUXILIARES Y LOGICA
# =====================================================================

def remover_acentos(texto):
    """
    Normaliza un texto convirtiéndolo a minúsculas y removiendo tildes básicas.
    Usa estructuras repetitivas tradicionales (Unidad 3).
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
    """Solicita una entrada por teclado y valida que sea un entero positivo."""
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
    """Lee el archivo CSV y convierte cada fila en un diccionario."""
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
    """Sobrescribe el archivo CSV externo con la lista de datos actual."""
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
    """Pide los datos de un pais, valida duplicados y guarda al finalizar."""
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
    """Busca un pais por su nombre y modifica sus valores numericos asociados."""
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
    """Procesa algoritmicamente los datos matematicos y de conteo de la lista."""
    if not lista_paises:
        return None, None, 0, 0, {}

    total_pob = 0
    total_sup = 0
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


# =====================================================================
#                  CAPA DE INTERFAZ DE USUARIO (VISTAS)
# =====================================================================

def mostrar_menu():
    """Imprime el menu de opciones interactivas."""
    print("\n" + "=" * 35)
    print("    SISTEMA DE GESTIÓN DE PAÍSES   ")
    print("=" * 35)
    print("1. Agregar un país")
    print("2. Actualizar población y superficie")
    print("3. Buscar un país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Consultar Listado de Paises")
    print("7. Mostrar estadísticas")
    print("8. Salir")
    print("=" * 35)


def realizar_listar_todos(lista_paises):
    """Presenta el padron completo de registros."""
    print("\n--- LISTADO GENERAL DE PAÍSES ---")
    if not lista_paises:
        print("No existen países registrados en el sistema.")
        return
        
    print(f"\nTotal registrados ({len(lista_paises)}):")
    print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie':<12} | {'Continente':<12}")
    print("-" * 60)
    for p in lista_paises:
        print(f"{p['nombre']:<15} | {p['poblacion']:<12} | {p['superficie']:<12} | {p['continente']:<12}")


def realizar_busqueda(lista_paises):
    """Filtra y muestra los registros mediante coincidencias parciales de nombre."""
    print("\n--- BUSCAR PAÍS ---")
    termino = input("Ingrese el término a buscar: ").strip()
    if not termino:
        print("Error: El término de búsqueda no puede estar vacío.")
        return

    resultados = []
    for pais in lista_paises:
        termino_norm = remover_acentos(termino)
        nombre_norm = remover_acentos(pais["nombre"])
        if termino_norm in nombre_norm:
            resultados.append(pais)

    if not resultados:
        print("No se encontraron países que coincidan con la búsqueda.")
    else:
        print(f"\nResultados encontrados ({len(resultados)}):")
        print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie':<12} | {'Continente':<12}")
        print("-" * 60)
        for p in resultados:
            print(f"{p['nombre']:<15} | {p['poblacion']:<12} | {p['superficie']:<12} | {p['continente']:<12}")


def realizar_filtrado(lista_paises):
    """Gestiona la interfaz de filtros mediante coincidencias parciales con proteccion de errores."""
    print("\n--- FILTRAR PAÍSES ---")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")
    print("4. Volver al menú principal")
    
    while True:
        subopcion = input("Seleccione una opción de filtrado (1-4): ").strip()
        if subopcion in ("1", "2", "3", "4"):
            break
        print("Error: Opción inválida. Ingrese un número del 1 al 4.")

    if subopcion == "4":
        print("Regresando al menú principal...")
        return

    resultados = []

    if subopcion == "1":
        cont_buscar = input("Ingrese el continente a filtrar: ").strip()
        for pais in lista_paises:
            buscar_norm = remover_acentos(cont_buscar)
            cont_norm = remover_acentos(pais["continente"])
            if buscar_norm in cont_norm:
                resultados.append(pais)
                
    elif subopcion in ("2", "3"):
        campo = "poblacion" if subopcion == "2" else "superficie"
        
        while True:
            minimo = solicitar_entero_positivo("Ingrese el valor mínimo: ")
            maximo = solicitar_entero_positivo("Ingrese el valor máximo: ")
            if minimo <= maximo:
                break
            print("Error: El valor mínimo no puede superar al máximo. Intente de nuevo.")

        for pais in lista_paises:
            if minimo <= pais[campo] <= maximo:
                resultados.append(pais)

    if not resultados:
        print("No se encontraron países con el criterio seleccionado.")
    else:
        print(f"\nResultados del filtro ({len(resultados)}):")
        print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie':<12} | {'Continente':<12}")
        print("-" * 60)
        for p in resultados:
            print(f"{p['nombre']:<15} | {p['poblacion']:<12} | {p['superficie']:<12} | {p['continente']:<12}")


def realizar_ordenamiento(lista_paises):
    """Gestiona la interfaz para ordenar con bucles robustos de control."""
    print("\n--- ORDENAR PAÍSES ---")
    print("1. Ordenar por Nombre")
    print("2. Ordenar por Población")
    print("3. Ordenar por Superficie")
    print("4. Volver al menú principal")
    
    while True:
        subopcion = input("Seleccione una opción de ordenamiento (1-4): ").strip()
        if subopcion in ("1", "2", "3", "4"):
            break
        print("Error: Opción inválida. Ingrese un número del 1 al 4.")

    if subopcion == "4":
        print("Regresando al menú principal...")
        return

    if subopcion == "1":
        clave = lambda x: x["nombre"].lower()
    elif subopcion == "2":
        clave = lambda x: x["poblacion"]
    elif subopcion == "3":
        clave = lambda x: x["superficie"]

    print("\n1. Ascendente (Menor a Mayor / A-Z)")
    print("2. Descendente (Mayor a Menor / Z-A)")
    
    while True:
        sentido = input("Seleccione el sentido del orden (1-2): ").strip()
        if sentido in ("1", "2"):
            break
        print("Error: Opción inválida. Ingrese 1 o 2.")

    descendente = True if sentido == "2" else False

    lista_ordenada = sorted(lista_paises, key=clave, reverse=descendente)
    print("\nLista ordenada:")
    print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie':<12} | {'Continente':<12}")
    print("-" * 60)
    for p in lista_ordenada:
        print(f"{p['nombre']:<15} | {p['poblacion']:<12} | {p['superficie']:<12} | {p['continente']:<12}")


def presentar_estadisticas(lista_paises):
    """Muestra en la interfaz los resultados de la capa logica."""
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    mayor, menor, prom_pob, prom_sup, conteo = calcular_metricas(lista_paises)

    if mayor is None:
        print("No hay datos suficientes para procesar indicadores globales.")
        return

    print(f"Pais con mayor poblacion: {mayor['nombre']} ({mayor['poblacion']} hab.)")
    print(f"Pais con menor poblacion: {menor['nombre']} ({menor['poblacion']} hab.)")
    print(f"Promedio de población global: {prom_pob:.2f} hab.")
    print(f"Promedio de superficie global: {prom_sup:.2f} km²")
    print("\nCantidad de paises por continente:")
    for continente, cantidad in conteo.items():
        print(f"- {continente}: {cantidad}")


# =====================================================================
#                      BUCLE PRINCIPAL DEL PROGRAMA
# =====================================================================

datos_paises = cargar_datos("paises.csv")
continuar = True

while continuar:
    mostrar_menu()
    opcion = input("Seleccione una opción (1-8): ").strip()

    if opcion == "1":
        agregar_pais(datos_paises)
    elif opcion == "2":
        actualizar_pais(datos_paises)
    elif opcion == "3":
        realizar_busqueda(datos_paises)
    elif opcion == "4":
        realizar_filtrado(datos_paises)
    elif opcion == "5":
        realizar_ordenamiento(datos_paises)
    elif opcion == "6":
        realizar_listar_todos(datos_paises)
    elif opcion == "7":
        presentar_estadisticas(datos_paises)
    elif opcion == "8":
        print("\nGracias por usar el sistema. Saliendo...")
        continuar = False
    else:
        print("\nOpcion invalida. Por favor, ingrese un número del 1 al 8.")
