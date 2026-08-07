class Localidad:
    """
    Clase que representa una localidad de un municipio con su nombre y coordenadas.
    """
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
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


class Municipio:
    """
    Clase que representa un municipio y almacena su lista de localidades.
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, localidad):
        """
        Agrega un objeto Localidad a la lista del municipio.
        """
        self.localidades.append(localidad)