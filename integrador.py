import funciones_paises


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
    """Filtra y muestra los registros mediante coincidencias parciales de nombre e inmune a tildes."""
    print("\n--- BUSCAR PAÍS ---")
    termino = input("Ingrese el término a buscar: ").strip()
    if not termino:
        print("Error: El término de búsqueda no puede estar vacío.")
        return

    resultados = []
    for pais in lista_paises:
        termino_norm = funciones_paises.remover_acentos(termino)
        nombre_norm = funciones_paises.remover_acentos(pais["nombre"])
        
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
    
    # Optimizacion: Bucle de validacion indeterminado para evitar salidas abruptas
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
            buscar_norm = funciones_paises.remover_acentos(cont_buscar)
            cont_norm = funciones_paises.remover_acentos(pais["continente"])
            if buscar_norm in cont_norm:
                resultados.append(pais)
                
    elif subopcion in ("2", "3"):
        campo = "poblacion" if subopcion == "2" else "superficie"
        
        # Validacion del rango logico de maximo y minimo
        while True:
            minimo = funciones_paises.solicitar_entero_positivo("Ingrese el valor mínimo: ")
            maximo = funciones_paises.solicitar_entero_positivo("Ingrese el valor máximo: ")
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
    
    # Optimizacion: Proteccion contra carácteres invalidos
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
    
    # Validacion del sentido de ordenacion
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
    mayor, menor, prom_pob, prom_sup, conteo = funciones_paises.calcular_metricas(lista_paises)

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

datos_paises = funciones_paises.cargar_datos("paises.csv")
continuar = True

while continuar:
    mostrar_menu()
    opcion = input("Seleccione una opción (1-8): ").strip()

    if opcion == "1":
        funciones_paises.agregar_pais(datos_paises)
    elif opcion == "2":
        funciones_paises.actualizar_pais(datos_paises)
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
        print("Sistema Cerrado.")
        continuar = False
    else:
        print("\nOpcion invalida. Por favor, ingrese un número del 1 al 8.")
