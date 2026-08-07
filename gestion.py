import requests
import matplotlib.pyplot as plt
from clases import RegistroDiario, ResumenPeriodo, ResumenMensual, ResumenAnual
from funciones import consultar_clima_tiempo_real, mostrar_detalles_clima


def consultar_por_municipio(lista_municipios, historial_consultas):
    """ Permite consultar el clima seleccionando primero el municipio y luego la localidad."""
    
    print("\n--- SELECCIONE UN MUNICIPIO ---")
    for i, mun in enumerate(lista_municipios, start=1):
        print(f"{i}. {mun.nombre}")

    try:
        opcion_mun = int(input("Ingrese el número del municipio: ")) - 1
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")
        return

    if opcion_mun < 0 or opcion_mun >= len(lista_municipios):
        print("Opción inválida.")
        return

    mun_seleccionado = lista_municipios[opcion_mun]
    locs_validas = mun_seleccionado.obtener_localidades_con_coordenadas()

    if not locs_validas:
        print("Este municipio no tiene localidades con coordenadas válidas.")
        return

    print(f"\n--- LOCALIDADES EN {mun_seleccionado.nombre} ---")
    for j, loc in enumerate(locs_validas, start=1):
        print(f"{j}. {loc}")

    try:
        opcion_loc = int(input("Ingrese el número de la localidad: ")) - 1
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")
        return

    if opcion_loc < 0 or opcion_loc >= len(locs_validas):
        print("Opción inválida.")
        return

    loc_seleccionada = locs_validas[opcion_loc]
    clima = consultar_clima_tiempo_real(
        mun_seleccionado.nombre, loc_seleccionada.nombre,
        loc_seleccionada.latitud, loc_seleccionada.longitud
    )

    if clima is not None:
        historial_consultas.append(clima)
        mostrar_detalles_clima(clima)


def consultar_por_busqueda_directa(lista_municipios, historial_consultas):
    """
    Permite buscar una localidad directamente escribiendo su nombre o parte de él.
    """
    busqueda = input("\nIngrese el nombre (o parte del nombre) de la localidad: ").strip().lower()

    coincidencias = []
    municipios_coincidencia = []

    for mun in lista_municipios:
        locs_validas = mun.obtener_localidades_con_coordenadas()
        for loc in locs_validas:
            if busqueda in loc.nombre.lower():
                coincidencias.append(loc)
                municipios_coincidencia.append(mun.nombre)

    if not coincidencias:
        print("No se encontraron localidades con coordenadas válidas que coincidan con la búsqueda.")
        return

    print("\n--- COINCIDENCIAS ENCONTRADAS ---")
    for idx, loc in enumerate(coincidencias, start=1):
        print(f"{idx}. {loc.nombre} (Municipio: {municipios_coincidencia[idx - 1]})")

    try:
        seleccion = int(input("Seleccione el número de la localidad: ")) - 1
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")
        return

    if seleccion < 0 or seleccion >= len(coincidencias):
        print("Selección inválida.")
        return

    loc_elegida = coincidencias[seleccion]
    mun_elegido = municipios_coincidencia[seleccion]

    clima = consultar_clima_tiempo_real(mun_elegido, loc_elegida.nombre, loc_elegida.latitud, loc_elegida.longitud)

    if clima is not None:
        historial_consultas.append(clima)
        mostrar_detalles_clima(clima)


def mostrar_estadisticas(lista_municipios, historial_consultas):
    """
    Muestra el módulo de estadísticas: Ranking de temperatura, Cobertura geográfica y Promedio general.
    """
    print("\n========================================")
    print("         MÓDULO DE ESTADÍSTICAS         ")
    print("========================================")

    # a. Ranking de Temperatura
    if not historial_consultas:
        print("a) Ranking de Temperatura: No hay consultas registradas en la sesión.")
    else:
        mas_calida = historial_consultas[0]
        mas_fria = historial_consultas[0]
        for consulta in historial_consultas:
            if consulta.temperatura > mas_calida.temperatura:
                mas_calida = consulta
            if consulta.temperatura < mas_fria.temperatura:
                mas_fria = consulta

        print("a) Ranking de Temperatura (según la sesión):")
        print(f"   - Localidad más cálida: {mas_calida.nombre_localidad} ({mas_calida.nombre_municipio}) con {mas_calida.temperatura} °C")
        print(f"   - Localidad más fría: {mas_fria.nombre_localidad} ({mas_fria.nombre_municipio}) con {mas_fria.temperatura} °C")

    # b. Cobertura Geográfica
    print("\nb) Cobertura Geográfica - Localidades sin coordenadas registradas:")
    for mun in lista_municipios:
        print(f"   * Municipio: {mun.nombre}")
        hay_sin_coordenadas = False
        for loc in mun.localidades:
            if not loc.tiene_coordenadas():
                print(f"     - {loc.nombre}")
                hay_sin_coordenadas = True
        if not hay_sin_coordenadas:
            print("     (Todas las localidades tienen coordenadas)")

    # c. Promedio General
    if not historial_consultas:
        print("\nc) Promedio General: No hay datos para calcular.")
    else:
        suma_temp = 0
        for consulta in historial_consultas:
            suma_temp += consulta.temperatura
        promedio = suma_temp / len(historial_consultas)
        print(f"\nc) Promedio General de Temperatura (sesión activa): {promedio:.2f} °C")
    print("========================================")


def buscar_resumen_mensual(lista_resumenes, anio, mes):
    """
    Busca en la lista un ResumenMensual que corresponda al año y mes indicados.
    """
    for resumen in lista_resumenes:
        if resumen.anio == anio and resumen.mes == mes:
            return resumen
    return None


def buscar_resumen_anual(lista_resumenes, anio):
    """
    Busca en la lista un ResumenAnual que corresponda al año indicado.
    """
    for resumen in lista_resumenes:
        if resumen.anio == anio:
            return resumen
    return None


def consultar_historico(lista_municipios):
    """
    Módulo histórico: consulta por período de tiempo, muestra promedios
    mensuales y anuales, el año más caluroso/fresco/lluvioso/húmedo, y un
    gráfico comparativo de la evolución de cada magnitud por año.
    """
    print("\n--- CONSULTA HISTÓRICA ---")

    print("Seleccione un municipio:")
    for i, mun in enumerate(lista_municipios, start=1):
        print(f"{i}. {mun.nombre}")

    try:
        op_mun = int(input("Municipio: ")) - 1
    except ValueError:
        print("Entrada inválida.")
        return

    if op_mun < 0 or op_mun >= len(lista_municipios):
        print("Municipio inválido.")
        return

    mun_sel = lista_municipios[op_mun]
    locs_validas = mun_sel.obtener_localidades_con_coordenadas()

    if not locs_validas:
        print("No hay localidades con coordenadas en este municipio.")
        return

    for j, loc in enumerate(locs_validas, start=1):
        print(f"{j}. {loc.nombre}")

    try:
        op_loc = int(input("Localidad: ")) - 1
    except ValueError:
        print("Entrada inválida.")
        return

    if op_loc < 0 or op_loc >= len(locs_validas):
        print("Localidad inválida.")
        return

    loc_sel = locs_validas[op_loc]
    print ("\n 
    fecha_inicio = input("Ingrese fecha de inicio (AAAA-MM-DD): ").strip()
    fecha_fin = input("Ingrese fecha de fin (AAAA-MM-DD): ").strip()

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?latitude={loc_sel.latitud}"
        f"&longitude={loc_sel.longitud}&start_date={fecha_inicio}&end_date={fecha_fin}"
        f"&daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max"
    )

    try:
        print("Consultando datos históricos...")
        resp = requests.get(url)
    except Exception as e:
        print(f"Ocurrió un error de red: {e}")
        return

    if resp.status_code != 200:
        print("Error al obtener los datos históricos de la API.")
        return

    data = resp.json()
    daily = data.get("daily", {})
    tiempos = daily.get("time", [])
    temps = daily.get("temperature_2m_mean", [])
    humedades = daily.get("relative_humidity_2m_mean", [])
    precipitaciones = daily.get("precipitation_sum", [])
    vientos = daily.get("wind_speed_10m_max", [])

    if not tiempos:
        print("No se encontraron registros para el rango de fechas indicado.")
        return

    # Transformamos la respuesta cruda de la API en una lista de objetos RegistroDiario
    lista_registros = []
    for k in range(len(tiempos)):
        registro = RegistroDiario(tiempos[k], temps[k], humedades[k], vientos[k], precipitaciones[k])
        lista_registros.append(registro)

    # Agrupamos los registros diarios en resúmenes mensuales y anuales
    # (siempre usando listas de objetos, nunca diccionarios, para guardar la información de la API)
    lista_resumenes_mensuales = []
    lista_resumenes_anuales = []

    for registro in lista_registros:
        anio = registro.obtener_anio()
        mes = registro.obtener_mes()

        resumen_mes = buscar_resumen_mensual(lista_resumenes_mensuales, anio, mes)
        if resumen_mes is None:
            resumen_mes = ResumenMensual(anio, mes)
            lista_resumenes_mensuales.append(resumen_mes)
        resumen_mes.agregar_registro(registro)

        resumen_anio = buscar_resumen_anual(lista_resumenes_anuales, anio)
        if resumen_anio is None:
            resumen_anio = ResumenAnual(anio)
            lista_resumenes_anuales.append(resumen_anio)
        resumen_anio.agregar_registro(registro)

    # i, ii, iii, iv: reporte mes a mes
    print(f"\n--- RESUMEN MENSUAL PARA {loc_sel.nombre.upper()} ---")
    for resumen_mes in lista_resumenes_mensuales:
        print(f"\n  Periodo {resumen_mes.etiqueta}:")
        print(f"    i.   Temperatura promedio: {resumen_mes.promedio_temperatura():.2f} °C")
        print(f"    ii.  Humedad relativa promedio: {resumen_mes.promedio_humedad():.2f} %")
        print(f"    iii. Precipitación acumulada: {resumen_mes.precipitacion_total():.2f} mm")
        print(f"    iv.  Velocidad del viento promedio: {resumen_mes.promedio_viento():.2f} km/h")

    # b. Promedios generales de todo el periodo consultado
    resumen_total = ResumenPeriodo(f"{fecha_inicio} a {fecha_fin}")
    for registro in lista_registros:
        resumen_total.agregar_registro(registro)

    print(f"\n--- PROMEDIOS GENERALES DEL PERIODO ({resumen_total.etiqueta}) ---")
    print(f"  - Temperatura promedio: {resumen_total.promedio_temperatura():.2f} °C")
    print(f"  - Humedad relativa promedio: {resumen_total.promedio_humedad():.2f} %")
    print(f"  - Velocidad del viento promedio: {resumen_total.promedio_viento():.2f} km/h")
    print(f"  - Precipitación acumulada total: {resumen_total.precipitacion_total():.2f} mm")

    # c. Año más caluroso, más fresco, más lluvioso y más húmedo
    if lista_resumenes_anuales:
        anio_caluroso = lista_resumenes_anuales[0]
        anio_fresco = lista_resumenes_anuales[0]
        anio_lluvioso = lista_resumenes_anuales[0]
        anio_humedo = lista_resumenes_anuales[0]

        for resumen_anio in lista_resumenes_anuales:
            if resumen_anio.promedio_temperatura() > anio_caluroso.promedio_temperatura():
                anio_caluroso = resumen_anio
            if resumen_anio.promedio_temperatura() < anio_fresco.promedio_temperatura():
                anio_fresco = resumen_anio
            if resumen_anio.precipitacion_total() > anio_lluvioso.precipitacion_total():
                anio_lluvioso = resumen_anio
            if resumen_anio.promedio_humedad() > anio_humedo.promedio_humedad():
                anio_humedo = resumen_anio

        print(f"\n  - Año más caluroso: {anio_caluroso.anio}")
        print(f"  - Año más fresco: {anio_fresco.anio}")
        print(f"  - Año con mayor precipitación: {anio_lluvioso.anio}")
        print(f"  - Año con mayor humedad relativa: {anio_humedo.anio}")

        # d. Gráfico comparativo de la evolución de cada magnitud por año
        print("\nGenerando gráfico comparativo...")
        anios_lista = []
        temp_por_anio = []
        hum_por_anio = []
        prec_por_anio = []
        viento_por_anio = []

        for resumen_anio in lista_resumenes_anuales:
            anios_lista.append(resumen_anio.anio)
            temp_por_anio.append(resumen_anio.promedio_temperatura())
            hum_por_anio.append(resumen_anio.promedio_humedad())
            prec_por_anio.append(resumen_anio.precipitacion_total())
            viento_por_anio.append(resumen_anio.promedio_viento())

        figura, graficos = plt.subplots(2, 2, figsize=(11, 7))
        figura.suptitle(f"Evolución Climática Anual - {loc_sel.nombre}")

        graficos[0, 0].plot(anios_lista, temp_por_anio, marker='o', color='tab:red')
        graficos[0, 0].set_title("Temperatura promedio (°C)")
        graficos[0, 0].grid(True)

        graficos[0, 1].plot(anios_lista, hum_por_anio, marker='o', color='tab:blue')
        graficos[0, 1].set_title("Humedad relativa promedio (%)")
        graficos[0, 1].grid(True)

        graficos[1, 0].plot(anios_lista, prec_por_anio, marker='o', color='tab:green')
        graficos[1, 0].set_title("Precipitación acumulada (mm)")
        graficos[1, 0].grid(True)

        graficos[1, 1].plot(anios_lista, viento_por_anio, marker='o', color='tab:orange')
        graficos[1, 1].set_title("Viento promedio (km/h)")
        graficos[1, 1].grid(True)

        plt.tight_layout()
        plt.show()
