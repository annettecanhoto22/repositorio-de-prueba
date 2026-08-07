import json
import os
import requests
from clases import Localidad, Municipio


class ClimaConsultado:
    """
    Clase para guardar los datos del clima consultados en la sesión (evita diccionarios).
    """
    def __init__(self, nombre_municipio, nombre_localidad, lat, lon, temp, humedad, viento, descripcion):
        self.nombre_municipio = nombre_municipio
        self.nombre_localidad = nombre_localidad
        self.lat = lat
        self.lon = lon
        self.temp = temp
        self.humedad = humedad
        self.viento = viento
        self.descripcion = descripcion


def crear_archivo_json_si_no_existe():
    """
    Crea un archivo zonas_caracas.json de ejemplo si no existe, para que el programa corra perfecto.
    """
    if not os.path.exists("zonas_caracas.json"):
        datos_ejemplo = {
            "Chacao": [
                {"nombre": "Altamira", "latitud": 10.5012, "longitud": -66.8512},
                {"nombre": "Challacao", "latitud": None, "longitud": None},
                {"nombre": "Los Palos Grandes", "latitud": 10.5003, "longitud": -66.8431}
            ],
            "Baruta": [
                {"nombre": "Las Mercedes", "latitud": 10.4856, "longitud": -66.8645},
                {"nombre": "El Peñón", "latitud": None, "longitud": None},
                {"nombre": "Baruta Centro", "latitud": 10.4347, "longitud": -66.8794}
            ],
            "El Hatillo": [
                {"nombre": "Pueblo El Hatillo", "latitud": 10.4267, "longitud": -66.8289},
                {"nombre": "La Lagunita", "latitud": 10.4391, "longitud": -66.8123}
            ],
            "Sucre": [
                {"nombre": "Petare", "latitud": 10.4833, "longitud": -66.8167},
                {"nombre": "La Urbina", "latitud": 10.4891, "longitud": -66.8052},
                {"nombre": "Caurimare", "latitud": None, "longitud": None}
            ],
            "Libertador": [
                {"nombre": "Catedral", "latitud": 10.5061, "longitud": -66.9143},
                {"nombre": "El Paraíso", "latitud": 10.4900, "longitud": -66.9333},
                {"nombre": "23 de Enero", "latitud": None, "longitud": None}
            ]
        }
        with open("zonas_caracas.json", "w", encoding="utf-8") as archivo:
            json.dump(datos_ejemplo, archivo, indent=4)


def cargar_datos():
    """
    Lee el archivo zonas_caracas.json y transforma su estructura en una lista de objetos.
    """
    crear_archivo_json_si_no_existe()
    with open("zonas_caracas.json", "r", encoding="utf-8") as archivo:
        contenido = json.load(archivo)

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
    """
    Muestra en pantalla el reporte inicial por cada municipio según los requerimientos.
    """
    print("\n========================================")
    print("      REPORTE DE CARGA DE LOCALIDADES   ")
    print("========================================")
    
    for mun in lista_municipios:
        total = len(mun.localidades)
        con_coord = sum(1 for loc in mun.localidades if loc.tiene_coordenadas())
        sin_coord = total - con_coord
        porcentaje = (con_coord / total * 100) if total > 0 else 0.0
            
        print(f"Municipio: {mun.nombre}")
        print(f"  - Cantidad de localidades cargadas: {total}")
        print(f"  - Con coordenadas geográficas: {con_coord}")
        print(f"  - Sin coordenadas geográficas: {sin_coord}")
        print(f"  - Porcentaje con coordenadas: {porcentaje:.2f}%")
        print("-" * 40)


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


def consultar_clima_api(lat, lon):
    """
    Consulta en tiempo real la API de Open-Meteo enviando latitud y longitud.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            actual = datos.get("current", {})
            temp = actual.get("temperature_2m")
            humedad = actual.get("relative_humidity_2m")
            viento = actual.get("wind_speed_10m")
            codigo = actual.get("weather_code", 0)
            descripcion = interpretar_codigo_clima(codigo)
            return temp, humedad, viento, descripcion
        else:
            print("Error al conectar con la API de Open-Meteo.")
            return None, None, None, None
    except Exception as e:
        print(f"Ocurrió un error de red: {e}")
        return None, None, None, None


def mostrar_detalles_clima(clima):
    """
    Despliega en pantalla los detalles meteorológicos de la localidad.
    """
    print("\n" + "="*45)
    print("          DETALLES METEOROLÓGICOS          ")
    print("="*45)
    print(f" i.   Nombre del Municipio: {clima.nombre_municipio}")
    print(f"      Nombre de la Localidad: {clima.nombre_localidad}")
    print(f" ii.  Coordenadas: Lat {clima.lat}, Lon {clima.lon}")
    print(f" iii. Temperatura actual: {clima.temp} °C")
    print(f" iv.  Humedad relativa: {clima.humedad} %")
    print(f" v.   Velocidad del viento: {clima.viento} km/h")
    print(f" vi.  Código/Estado del tiempo: {clima.descripcion}")
    print("="*45)