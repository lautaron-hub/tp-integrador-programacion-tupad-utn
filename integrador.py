import csv

def cargar_datos(nombre_archivo):
    """
    Lee el archivo CSV y convierte cada fila en un diccionario.
    Devuelve una lista con todos los países cargados.
    """
    lista_paises = []
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
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
        print(f"Alerta: No se encontro el archivo '{nombre_archivo}'. Se iniciara con una lista vacia.")
        return []
    except (ValueError, KeyError):
        print("Error: El formato del archivo CSV es invalido o contiene datos corruptos.")
        return []

def mostrar_menu():
    """
    Imprime las opciones disponibles en la consola.
    """
    print("\n" + "="*35)
    print("    SISTEMA DE GESTIÓN DE PAÍSES   ")
    print("="*35)
    print("1. Agregar un país")
    print("2. Actualizar población y superficie")
    print("3. Buscar un país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("7. Salir")
    print("="*35)

def agregar_pais(lista_paises):
    """
    Pide los datos de un nuevo país, valida que no esté vacío,
    que no esté duplicado y que los números sean correctos.
    """
    print("\n--- AGREGAR NUEVO PAÍS ---")
    nombre = input("Ingrese el nombre del país: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return

    # NUEVA VALIDACIÓN: Verificar si el país ya existe en la lista (Unidad 3 y 5)
    for pais in lista_paises:
        if pais["nombre"].lower() == nombre.lower():
            print(f"Error: El pais '{pais['nombre']}' ya se encuentra registrado.")
            return

    try:
        poblacion = int(input("Ingrese la población: "))
        if poblacion < 0:
            print("Error: La población no puede ser un número negativo.")
            return
    except ValueError:
        print("Error: La población debe ser un número entero válido.")
        return

    try:
        superficie = int(input("Ingrese la superficie en km²: "))
        if superficie < 0:
            print("Error: La superficie no puede ser un número negativo.")
            return
    except ValueError:
        print("Error: La superficie debe ser un número entero válido.")
        return

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

def actualizar_pais(lista_paises):
    """
    Busca un país por nombre y permite modificar su población y superficie.
    """
    print("\n--- ACTUALIZAR DATOS DE PAÍS ---")
    nombre_buscar = input("Ingrese el nombre del país a modificar: ").strip().lower()
    if not nombre_buscar:
        print("Error: El nombre de búsqueda no puede estar vacío.")
        return
    pais_encontrado = None
    for pais in lista_paises:
        if pais["nombre"].lower() == nombre_buscar:
            pais_encontrado = pais
            break
    if pais_encontrado is None:
        print("Error: El país ingresado no se encuentra registrado.")
        return
    print(f"País seleccionado: {pais_encontrado['nombre']}")
    print(f"Valores actuales -> Población: {pais_encontrado['poblacion']} | Superficie: {pais_encontrado['superficie']} km²")
    try:
        nueva_poblacion = int(input("Ingrese la nueva población: "))
        if nueva_poblacion < 0:
            print("Error: La población no puede ser un número negativo.")
            return
    except ValueError:
        print("Error: La población debe ser un número entero válido.")
        return
    try:
        nueva_superficie = int(input("Ingrese la nueva superficie en km²: "))
        if nueva_superficie < 0:
            print("Error: La superficie no puede ser un número negativo.")
            return
    except ValueError:
        print("Error: La superficie debe ser un número entero válido.")
        return
    pais_encontrado["poblacion"] = nueva_poblacion
    pais_encontrado["superficie"] = nueva_superficie
    print(f"Datos de '{pais_encontrado['nombre']}' actualizados correctamente en memoria.")
def buscar_pais(lista_paises):
    """
    Busca países cuyo nombre contenga el texto ingresado por el usuario.
    """
    print("\n--- BUSCAR PAÍS ---")
    termino_busqueda = input("Ingrese el nombre o parte del nombre a buscar: ").strip().lower()
    if not termino_busqueda:
        print("Error: El término de búsqueda no puede estar vacío.")
        return
    resultados = []
    for pais in lista_paises:
        if termino_busqueda in pais["nombre"].lower():
            resultados.append(pais)
    if not resultados:
        print("No se encontraron países que coincidan con la búsqueda.")
    else:
        print(f"\nResultados encontrados ({len(resultados)}):")
        print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie (km²)':<16} | {'Continente':<12}")
        print("-" * 65)
        for pais in resultados:
            print(f"{pais['nombre']:<15} | {pais['poblacion']:<12} | {pais['superficie']:<16} | {pais['continente']:<12}")

def filtrar_paises(lista_paises):
    """
    Permite filtrar la lista de países por continente, rango de población o superficie.
    """
    print("\n--- FILTRAR PAÍSES ---")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")
    subopcion = input("Seleccione una opción de filtrado (1-3): ").strip()
    resultados = []
    if subopcion == "1":
        continente_buscar = input("Ingrese el continente a filtrar: ").strip().lower()
        for pais in lista_paises:
            if pais["continente"].lower() == continente_buscar:
                resultados.append(pais)
    elif subopcion == "2" or subopcion == "3":
        campo = "poblacion" if subopcion == "2" else "superficie"
        try:
            minimo = int(input("Ingrese el valor mínimo: "))
            maximo = int(input("Ingrese el valor máximo: "))
            if minimo < 0 or maximo < 0:
                print("Error: Los rangos no pueden ser negativos.")
                return
            if minimo > maximo:
                print("Error: El valor mínimo no puede ser mayor al máximo.")
                return
        except ValueError:
            print("Error: Los valores ingresados deben ser números enteros.")
            return
        for pais in lista_paises:
            if minimo <= pais[campo] <= maximo:
                resultados.append(pais)
    else:
        print("Error: Opción de filtrado inválida.")
        return
    if not resultados:
        print("No se encontraron países que cumplan con el criterio de filtrado.")
    else:
        print(f"\nResultados del filtro ({len(resultados)}):")
        print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie (km²)':<16} | {'Continente':<12}")
        print("-" * 65)
        for pais in resultados:
            print(f"{pais['nombre']:<15} | {pais['poblacion']:<12} | {pais['superficie']:<16} | {pais['continente']:<12}")

def ordenar_paises(lista_paises):
    """
    Ordena la lista de países por nombre, población o superficie.
    """
    print("\n--- ORDENAR PAÍSES ---")
    print("1. Ordenar por Nombre")
    print("2. Ordenar por Población")
    print("3. Ordenar por Superficie")
    subopcion = input("Seleccione una opción de ordenamiento (1-3): ").strip()

    if subopcion == "1":
        clave = lambda x: x["nombre"].lower()
    elif subopcion == "2":
        clave = lambda x: x["poblacion"]
    elif subopcion == "3":
        clave = lambda x: x["superficie"]
    else:
        print("Error: Opción de ordenamiento inválida.")
        return

    print("\n1. Ascendente (Menor a Mayor / A-Z)")
    print("2. Descendente (Mayor a Menor / Z-A)")
    sentido = input("Seleccione el sentido del orden (1-2): ").strip()

    if sentido == "1":
        descendente = False
    elif sentido == "2":
        descendente = True
    else:
        print("Error: Opción de sentido inválida.")
        return

    lista_ordenada = sorted(lista_paises, key=clave, reverse=descendente)

    print(f"\nLista ordenada:")
    print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie (km²)':<16} | {'Continente':<12}")
    print("-" * 65)
    for pais in lista_ordenada:
        print(f"{pais['nombre']:<15} | {pais['poblacion']:<12} | {pais['superficie']:<16} | {pais['continente']:<12}")
def mostrar_estadisticas(lista_paises):
    """
    Calcula y muestra los promedios, máximos, mínimos y totales por continente.
    """
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    if not lista_paises:
        print("No hay datos disponibles para calcular estadísticas.")
        return

    total_poblacion = 0
    total_superficie = 0
    pais_mayor_pob = lista_paises[0]
    pais_menor_pob = lista_paises[0]
    conteo_continentes = {}

    for pais in lista_paises:
        total_poblacion += pais["poblacion"]
        total_superficie += pais["superficie"]
        
        if pais["poblacion"] > pais_mayor_pob["poblacion"]:
            pais_mayor_pob = pais
        if pais["poblacion"] < pais_menor_pob["poblacion"]:
            pais_menor_pob = pais
            
        cont = pais["continente"]
        if cont in conteo_continentes:
            conteo_continentes[cont] += 1
        else:
            conteo_continentes[cont] = 1

    cantidad_paises = len(lista_paises)
    promedio_pob = total_poblacion / cantidad_paises
    promedio_sup = total_superficie / cantidad_paises

    print(f"Pais con mayor poblacion: {pais_mayor_pob['nombre']} ({pais_mayor_pob['poblacion']} hab.)")
    print(f"Pais con menor poblacion: {pais_menor_pob['nombre']} ({pais_menor_pob['poblacion']} hab.)")
    print(f"Promedio de población global: {promedio_pob:.2f} hab.")
    print(f"Promedio de superficie global: {promedio_sup:.2f} km²")
    print("\nCantidad de paises por continente:")
    for continente, cantidad in conteo_continentes.items():
        print(f"- {continente}: {cantidad}")

def guardar_datos(nombre_archivo, lista_paises):
    """
    Sobrescribe el archivo CSV con la información actualizada de la lista.
    """
    try:
        with open(nombre_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            
            escritor.writeheader()
            escritor.writerows(lista_paises)
        print("Cambios guardados exitosamente en el archivo CSV.")
    except Exception:
        print("Error: No se pudieron guardar los datos en el archivo.")


# =====================================================================
#                      BUCLE PRINCIPAL DEL PROGRAMA
# =====================================================================

datos_paises = cargar_datos("paises.csv")

continuar = True
while continuar:
    mostrar_menu()
    opcion = input("Seleccione una opción (1-7): ").strip()
    
    if opcion == "1":
        agregar_pais(datos_paises)
    elif opcion == "2":
        actualizar_pais(datos_paises)
    elif opcion == "3":
        buscar_pais(datos_paises)
    elif opcion == "4":
        filtrar_paises(datos_paises)
    elif opcion == "5":
        ordenar_paises(datos_paises)
    elif opcion == "6":
        mostrar_estadisticas(datos_paises)
    elif opcion == "7":
        print("\nGuardando cambios antes de salir...")
        # AHORA SÍ: Guardamos la lista en el disco de la PC antes de cerrar
        guardar_datos("paises.csv", datos_paises)
        print("Gracias por usar el sistema. Saliendo...")
        continuar = False
    else:
        print("\nOpcion invalida. Por favor, ingrese un número del 1 al 7.")
