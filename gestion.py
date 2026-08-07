import requests
import matplotlib.pyplot as plt
from funciones import ClimaConsultado, consultar_clima_api, mostrar_detalles_clima


def consultar_por_municipio(lista_municipios, historial_consultas):
    """
    Permite consultar el clima seleccionando primero el municipio y luego la localidad.
    """
    print("\n--- SELECCIONE UN MUNICIPIO ---")
    for i, mun in enumerate(lista_municipios, start=1):
        print(f"{i}. {mun.nombre}")
        
    try:
        opcion_mun = int(input("Ingrese el número del municipio: ")) - 1
        if opcion_mun < 0 or opcion_mun >= len(lista_municipios):
            print("Opción inválida.")
            return
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")
        return
        
    mun_seleccionado = lista_municipios[opcion_mun]
    locs_validas = [loc for loc in mun_seleccionado.localidades if loc.tiene_coordenadas()]
            
    if not locs_validas:
        print("Este municipio no tiene localidades con coordenadas válidas.")
        return
        
    print(f"\n--- LOCALIDADES EN {mun_seleccionado.nombre} ---")
    for j, loc in enumerate(locs_validas, start=1):
        print(f"{j}. {loc.nombre} (Lat: {loc.latitud}, Lon: {loc.longitud})")
        
    try:
        opcion_loc = int(input("Ingrese el número de la localidad: ")) - 1
        if opcion_loc < 0 or opcion_loc >= len(locs_validas):
            print("Opción inválida.")
            return
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")
        return
        
    loc_seleccionada = locs_validas[opcion_loc]
    temp, humedad, viento, desc = consultar_clima_api(loc_seleccionada.latitud, loc_seleccionada.longitud)
    
    if temp is not None:
        objeto_clima = ClimaConsultado(mun_seleccionado.nombre, loc_seleccionada.nombre, loc_seleccionada.latitud, loc_seleccionada.longitud, temp, humedad, viento, desc)
        historial_consultas.append(objeto_clima)
        mostrar_detalles_clima(objeto_clima)


def consultar_por_busqueda_directa(lista_municipios, historial_consultas):
    """
    Permite buscar una localidad directamente escribiendo su nombre o parte de él.
    """
    busqueda = input("\nIngrese el nombre (o parte del nombre) de la localidad: ").strip().lower()
    
    coincidencias = []
    municipios_coincidencia = []
    
    for mun in lista_municipios:
        for loc in mun.localidades:
            if busqueda in loc.nombre.lower() and loc.tiene_coordenadas():
                coincidencias.append(loc)
                municipios_coincidencia.append(mun.nombre)
                    
    if not coincidencias:
        print("No se encontraron localidades con coordenadas válidas que coincidan con la búsqueda.")
        return
        
    print("\n--- COINCIDENCIAS ENCONTRADAS ---")
    for idx, (loc, mun_nombre) in enumerate(zip(coincidencias, municipios_coincidencia), start=1):
        print(f"{idx}. {loc.nombre} (Municipio: {mun_nombre})")
        
    try:
        seleccion = int(input("Seleccione el número de la localidad: ")) - 1
        if seleccion < 0 or seleccion >= len(coincidencias):
            print("Selección inválida.")
            return
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")
        return
        
    loc_elegida = coincidencias[seleccion]
    mun_elegido = municipios_coincidencia[seleccion]
    
    temp, humedad, viento, desc = consultar_clima_api(loc_elegida.latitud, loc_elegida.longitud)
    
    if temp is not None:
        objeto_clima = ClimaConsultado(mun_elegido, loc_elegida.nombre, loc_elegida.latitud, loc_elegida.longitud, temp, humedad, viento, desc)
        historial_consultas.append(objeto_clima)
        mostrar_detalles_clima(objeto_clima)


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
        mas_calida = max(historial_consultas, key=lambda c: c.temp)
        mas_fria = min(historial_consultas, key=lambda c: c.temp)
        
        print("a) Ranking de Temperatura (según la sesión):")
        print(f"   - Localidad más cálida: {mas_calida.nombre_localidad} ({mas_calida.nombre_municipio}) con {mas_calida.temp} °C")
        print(f"   - Localidad más fría: {mas_fria.nombre_localidad} ({mas_fria.nombre_municipio}) con {mas_fria.temp} °C")
        
    # b. Cobertura Geográfica
    print("\nb) Cobertura Geográfica - Localidades sin coordenadas registradas:")
    for mun in lista_municipios:
        print(f"   * Municipio: {mun.nombre}")
        sin_coords = [loc.nombre for loc in mun.localidades if not loc.tiene_coordenadas()]
        if sin_coords:
            for nombre_loc in sin_coords:
                print(f"     - {nombre_loc}")
        else:
            print("     (Todas las localidades tienen coordenadas)")
            
    # c. Promedio General
    if not historial_consultas:
        print("\nc) Promedio General: No hay datos para calcular.")
    else:
        promedio = sum(c.temp for c in historial_consultas) / len(historial_consultas)
        print(f"\nc) Promedio General de Temperatura (sesión activa): {promedio:.2f} °C")
    print("========================================")


def consultar_historico(lista_municipios):
    """
    Módulo histórico: consulta por período de tiempo, muestra promedios, año más caluroso/frío y gráfico.
    """
    print("\n--- CONSULTA HISTÓRICA ---")
    
    print("Seleccione un municipio:")
    for i, mun in enumerate(lista_municipios, start=1):
        print(f"{i}. {mun.nombre}")
        
    try:
        op_mun = int(input("Municipio: ")) - 1
        if op_mun < 0 or op_mun >= len(lista_municipios):
            print("Municipio inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
        
    mun_sel = lista_municipios[op_mun]
    locs_validas = [loc for loc in mun_sel.localidades if loc.tiene_coordenadas()]
            
    if not locs_validas:
        print("No hay localidades con coordenadas en este municipio.")
        return
        
    for j, loc in enumerate(locs_validas, start=1):
        print(f"{j}. {loc.nombre}")
        
    try:
        op_loc = int(input("Localidad: ")) - 1
        if op_loc < 0 or op_loc >= len(locs_validas):
            print("Localidad inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
        
    loc_sel = locs_validas[op_loc]
    
    fecha_inicio = input("Ingrese fecha de inicio (AAAA-MM-DD): ").strip()
    fecha_fin = input("Ingrese fecha de fin (AAAA-MM-DD): ").strip()
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={loc_sel.latitud}&longitude={loc_sel.longitud}&start_date={fecha_inicio}&end_date={fecha_fin}&daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max"
    
    try:
        print("Consultando datos históricos...")
        resp = requests.get(url)
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
            
        valid_temps = [t for t in temps if t is not None]
        valid_hum = [h for h in humedades if h is not None]
        valid_prec = [p for p in precipitaciones if p is not None]
        valid_vientos = [v for v in vientos if v is not None]
        
        print(f"\n--- RESULTADOS HISTÓRICOS PARA {loc_sel.nombre.upper()} ---")
        if valid_temps: print(f"  - Temperatura promedio: {sum(valid_temps)/len(valid_temps):.2f} °C")
        if valid_hum: print(f"  - Humedad relativa promedio: {sum(valid_hum)/len(valid_hum):.2f} %")
        if valid_prec: print(f"  - Precipitación acumulada total: {sum(valid_prec):.2f} mm")
        if valid_vientos: print(f"  - Velocidad del viento promedio: {sum(valid_vientos)/len(valid_vientos):.2f} km/h")
        
        anos_dict_temps = {}
        anos_dict_hum = {}
        anos_dict_prec = {}
        
        for k in range(len(tiempos)):
            ano = tiempos[k].split("-")[0]
            
            if ano not in anos_dict_temps:
                anos_dict_temps[ano] = []
                anos_dict_hum[ano] = []
                anos_dict_prec[ano] = []
                
            if temps[k] is not None: anos_dict_temps[ano].append(temps[k])
            if humedades[k] is not None: anos_dict_hum[ano].append(humedades[k])
            if precipitaciones[k] is not None: anos_dict_prec[ano].append(precipitaciones[k])
            
        anos_lista = []
        proms_temp_anos = []
        proms_hum_anos = []
        totales_prec_anos = []
        
        for ano in anos_dict_temps:
            if anos_dict_temps[ano]:
                anos_lista.append(ano)
                proms_temp_anos.append(sum(anos_dict_temps[ano]) / len(anos_dict_temps[ano]))
                proms_hum_anos.append(sum(anos_dict_hum[ano]) / len(anos_dict_hum[ano]))
                totales_prec_anos.append(sum(anos_dict_prec[ano]))
            
        if anos_lista:
            idx_caluroso = proms_temp_anos.index(max(proms_temp_anos))
            idx_fresco = proms_temp_anos.index(min(proms_temp_anos))
            idx_lluvioso = totales_prec_anos.index(max(totales_prec_anos))
            idx_humedo = proms_hum_anos.index(max(proms_hum_anos))
                    
            print(f"\n  - Año más caluroso: {anos_lista[idx_caluroso]}")
            print(f"  - Año más fresco: {anos_lista[idx_fresco]}")
            print(f"  - Año con mayor precipitación: {anos_lista[idx_lluvioso]}")
            print(f"  - Año con mayor humedad relativa: {anos_lista[idx_humedo]}")
            
            print("\nGenerando gráfico comparativo...")
            plt.figure(figsize=(9, 4))
            plt.plot(anos_lista, proms_temp_anos, marker='o', label='Temp Promedio (°C)')
            plt.plot(anos_lista, proms_hum_anos, marker='s', label='Humedad Promedio (%)')
            plt.title(f"Evolución Climática - {loc_sel.nombre}")
            plt.xlabel("Año")
            plt.ylabel("Magnitud")
            plt.legend()
            plt.grid(True)
            plt.show()
            
    except Exception as e:
        print(f"Ocurrió un error en la consulta histórica: {e}")