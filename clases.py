class EntidadGeografica:
    """
    Clase madre que agrupa el comportamiento común de cualquier entidad
    geográfica del sistema (por ahora, simplemente tiene un nombre y se
    puede mostrar como texto).
    """
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre


class Localidad(EntidadGeografica):
    """
    Representa una localidad puntual dentro de un municipio, con sus
    coordenadas geográficas (si las tiene). Hereda de EntidadGeografica
    porque una localidad también es, en esencia, un lugar con nombre.
    """
    def __init__(self, nombre, latitud, longitud):
        super().__init__(nombre)
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenadas(self):
        """
        Verifica si la localidad tiene coordenadas geográficas válidas.
        """
        if self.latitud is not None and self.longitud is not None:
            return True
        else:
            return False

    def __str__(self):
        if self.tiene_coordenadas():
            return f"{self.nombre} (Lat: {self.latitud}, Lon: {self.longitud})"
        else:
            return f"{self.nombre} (sin coordenadas)"


class Municipio(EntidadGeografica):
    """
    Representa un municipio del área metropolitana de Caracas y guarda
    la lista de localidades que le pertenecen. También hereda de
    EntidadGeografica por compartir el atributo nombre.
    """
    def __init__(self, nombre):
        super().__init__(nombre)
        self.localidades = []

    def agregar_localidad(self, localidad):
        """
        Agrega un objeto Localidad a la lista del municipio.
        """
        self.localidades.append(localidad)

    def obtener_localidades_con_coordenadas(self):
        """
        Devuelve una lista con las localidades del municipio que sí
        tienen coordenadas válidas.
        """
        lista_validas = []
        for loc in self.localidades:
            if loc.tiene_coordenadas():
                lista_validas.append(loc)
        return lista_validas

    def contar_con_coordenadas(self):
        """
        Cuenta cuántas localidades del municipio tienen coordenadas válidas.
        """
        return len(self.obtener_localidades_con_coordenadas())

    def contar_sin_coordenadas(self):
        """
        Cuenta cuántas localidades del municipio no tienen coordenadas.
        """
        return len(self.localidades) - self.contar_con_coordenadas()

    def porcentaje_con_coordenadas(self):
        """
        Calcula el porcentaje de localidades del municipio que tienen
        coordenadas geográficas registradas.
        """
        if len(self.localidades) == 0:
            return 0.0
        return (self.contar_con_coordenadas() / len(self.localidades)) * 100

    def __len__(self):
        return len(self.localidades)


class DatoMeteorologico:
    """
    Clase madre que agrupa las magnitudes climáticas que comparten tanto
    una consulta en tiempo real como un registro histórico diario:
    temperatura, humedad relativa y velocidad del viento.
    """
    def __init__(self, temperatura, humedad, viento):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento

    def __str__(self):
        return f"Temp: {self.temperatura} °C | Humedad: {self.humedad}% | Viento: {self.viento} km/h"


class ClimaActual(DatoMeteorologico):
    """
    Guarda el resultado de una consulta de clima en tiempo real para una
    localidad específica. Hereda de DatoMeteorologico para reutilizar los
    atributos climáticos básicos.
    """
    def __init__(self, nombre_municipio, nombre_localidad, lat, lon, temperatura, humedad, viento, descripcion):
        super().__init__(temperatura, humedad, viento)
        self.nombre_municipio = nombre_municipio
        self.nombre_localidad = nombre_localidad
        self.lat = lat
        self.lon = lon
        self.descripcion = descripcion


class RegistroDiario(DatoMeteorologico):
    """
    Representa un registro meteorológico histórico de un día puntual,
    obtenido de la API de archivo histórico de Open-Meteo. También hereda
    de DatoMeteorologico y agrega la fecha y la precipitación del día.
    """
    def __init__(self, fecha, temperatura, humedad, viento, precipitacion):
        super().__init__(temperatura, humedad, viento)
        self.fecha = fecha
        self.precipitacion = precipitacion

    def obtener_anio(self):
        """
        Extrae el año (AAAA) a partir de la fecha del registro (AAAA-MM-DD).
        """
        return self.fecha.split("-")[0]

    def obtener_mes(self):
        """
        Extrae el mes (MM) a partir de la fecha del registro (AAAA-MM-DD).
        """
        return self.fecha.split("-")[1]


class ResumenPeriodo:
    """
    Clase madre que acumula los datos meteorológicos de varios registros
    diarios pertenecientes a un mismo periodo (un mes, un año, o el rango
    completo consultado) y calcula sus promedios.
    """
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.temperaturas = []
        self.humedades = []
        self.vientos = []
        self.precipitaciones = []

    def agregar_registro(self, registro):
        """
        Agrega los valores de un objeto RegistroDiario a las listas del periodo.
        """
        if registro.temperatura is not None:
            self.temperaturas.append(registro.temperatura)
        if registro.humedad is not None:
            self.humedades.append(registro.humedad)
        if registro.viento is not None:
            self.vientos.append(registro.viento)
        if registro.precipitacion is not None:
            self.precipitaciones.append(registro.precipitacion)

    def promedio_temperatura(self):
        """
        Calcula la temperatura promedio del periodo.
        """
        if len(self.temperaturas) == 0:
            return 0.0
        return sum(self.temperaturas) / len(self.temperaturas)

    def promedio_humedad(self):
        """
        Calcula la humedad relativa promedio del periodo.
        """
        if len(self.humedades) == 0:
            return 0.0
        return sum(self.humedades) / len(self.humedades)

    def promedio_viento(self):
        """
        Calcula la velocidad del viento promedio del periodo.
        """
        if len(self.vientos) == 0:
            return 0.0
        return sum(self.vientos) / len(self.vientos)

    def precipitacion_total(self):
        """
        Calcula la precipitación acumulada del periodo.
        """
        return sum(self.precipitaciones)


class ResumenMensual(ResumenPeriodo):
    """
    Resumen de las magnitudes climáticas para un mes de un año específico.
    """
    def __init__(self, anio, mes):
        etiqueta = f"{anio}-{mes}"
        super().__init__(etiqueta)
        self.anio = anio
        self.mes = mes


class ResumenAnual(ResumenPeriodo):
    """
    Resumen de las magnitudes climáticas para un año completo.
    """
    def __init__(self, anio):
        super().__init__(anio)
        self.anio = anio
