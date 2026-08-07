from funciones import cargar_datos, generar_reporte_carga
from gestion import (consultar_por_municipio, consultar_por_busqueda_directa, mostrar_estadisticas, consultar_historico)


def main():
    lista_municipios = cargar_datos()
    historial_consultas = []

    # Reporte automático de carga inicial
    generar_reporte_carga(lista_municipios)

    while True:
        print("== SISTEMA METEOROLÓGICO CARACAS ==")
        print("1. Consultar clima por Municipio / Localidad")
        print("2. Búsqueda directa por Localidad")
        print("3. Ver Estadísticas de la Sesión")
        print("4. Consulta Histórica Meteorológica")
        print("5. Salir del sistema")
        
        opcion = input("\nSeleccione una opción (1-5): ").strip()

        if opcion == "1":
            consultar_por_municipio(lista_municipios, historial_consultas)
        elif opcion == "2":
            consultar_por_busqueda_directa(lista_municipios, historial_consultas)
        elif opcion == "3":
            mostrar_estadisticas(lista_municipios, historial_consultas)
        elif opcion == "4":
            consultar_historico(lista_municipios)
        elif opcion == "5":
            print("\n¡Gracias por utilizar MeteoCaracas! Hasta luego.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
