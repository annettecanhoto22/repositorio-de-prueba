import json
import os
import requests
from clases import Localidad, Municipio, ClimaActual




def cargar_datos():
    
    """Lee el archivo zonas_caracas.json y transforma su estructura en una lista de objetos Municipio, cada uno con su respectiva lista de objetos Localidad."""
    archivo = open("zonas_caracas.json", "r", encoding="utf-8")
    contenido = json.load(archivo)
    archivo.close()

    lista_municipios = []

    for nombre_mun, lista_locs in contenido.items():
        objeto_mun = Municipio(nombre_mun)

        for loc_info in lista_locs:
            nombre_loc = loc_info["nombre"]
            lat = loc_info["latitud"]
            lon = loc_info["longitud"]
            objeto_loc = Localidad(nombre_loc, lat, lon)
            objeto_mun.agregar_localidad(objeto_loc)

        lista_municipios.append(objeto_mun)

    return lista_municipios


def generar_reporte_carga(lista_municipios):
    """ Muestra en pantalla el reporte inicial de carga por cada municipio, apoyándose en los métodos que la propia clase Municipio ofrece."""
    print("\n=== REPORTE DE CARGA DE LOCALIDADES ===\n")

    for mun in lista_municipios:
        total = len(mun)
        con_coord = mun.contar_con_coordenadas()
        sin_coord = mun.contar_sin_coordenadas()
        porcentaje = mun.porcentaje_con_coordenadas()

        print(f"Municipio: {mun.nombre}")
        print(f"  - Cantidad de localidades cargadas: {total}")
        print(f"  - Con coordenadas geográficas: {con_coord}")
        print(f"  - Sin coordenadas geográficas: {sin_coord}")
        print(f"  - Porcentaje con coordenadas: {porcentaje:.2f}%")
        print("-----------------------------------------------------")


def interpretar_codigo_clima(codigo):
    """
    Traduce el código numérico del clima de Open-Meteo a una descripción en texto.
    """
    if codigo == 0:
        return "Despejado"
    elif 1 <= codigo <= 3:
        return "Parcialmente nublado"
    elif 45 <= codigo <= 48:
        return "Neblina"
    elif 51 <= codigo <= 67:
        return "Lluvia moderada"
    elif 71 <= codigo <= 77:
        return "Nieve"
    elif codigo >= 95:
        return "Tormenta eléctrica"
    else:
        return "Nublado / Variable"


def consultar_clima_tiempo_real(nombre_municipio, nombre_localidad, lat, lon):
    """ Consulta en tiempo real la API de Open-Meteo enviando latitud y longitud, y arma un objeto ClimaActual con la respuesta obtenida."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"

    try:
        respuesta = requests.get(url)
    except Exception as e:
        print(f"Ocurrió un error de red al consultar el clima: {e}")
        return None

    if respuesta.status_code != 200:
        print("Error al conectar con la API de Open-Meteo.")
        return None

    datos = respuesta.json()
    actual = datos.get("current", {})
    temp = actual.get("temperature_2m")
    humedad = actual.get("relative_humidity_2m")
    viento = actual.get("wind_speed_10m")
    codigo = actual.get("weather_code", 0)
    descripcion = interpretar_codigo_clima(codigo)

    if temp is None:
        print("La API no devolvió datos de temperatura para esta ubicación.")
        return None

    clima = ClimaActual(nombre_municipio, nombre_localidad, lat, lon, temp, humedad, viento, descripcion)
    return clima


def mostrar_detalles_clima(clima):
    """ Despliega en pantalla los detalles meteorológicos de una consulta en tiempo real."""
    print("\n" + "=" * 45)
    print("          DETALLES METEOROLÓGICOS          ")
    print("=" * 45)
    print(f" i.   Nombre del Municipio: {clima.nombre_municipio}")
    print(f"      Nombre de la Localidad: {clima.nombre_localidad}")
    print(f" ii.  Coordenadas: Lat {clima.lat}, Lon {clima.lon}")
    print(f" iii. Temperatura actual: {clima.temperatura} °C")
    print(f" iv.  Humedad relativa: {clima.humedad} %")
    print(f" v.   Velocidad del viento: {clima.viento} km/h")
    print(f" vi.  Código/Estado del tiempo: {clima.descripcion}")
    print("=" * 45)
