"""
main.py - Suite de pruebas para el Sistema de Gestión Arquitectónica e Inmobiliaria.
Demuestra composición pura, herencia, polimorfismo, descriptores, @property, @staticmethod y dunder methods.
"""

from casa import Casa
from habitaciones import Habitacion


if __name__ == "__main__":
    print("=" * 65)
    print("1. CONSTRUCCIÓN DE CASA MEDIANTE COMPOSICIÓN PURA")
    print("=" * 65)

    # Instanciamos la casa únicamente con su dirección (sin pasar objetos Habitacion externos)
    mi_casa = Casa("Av. Paseo de la Reforma 450, CDMX")

    # Las habitaciones nacen directamente dentro de los métodos de Casa
    mi_casa.construir_sala(nombre="Sala Principal", metros=28.0, tiene_balcon=True)
    mi_casa.construir_cocina(nombre="Cocina Integral", metros=14.5, es_integral=True)
    mi_casa.construir_recamara(nombre="Recámara Principal", metros=20.0, tiene_bano_privado=True)
    mi_casa.construir_recamara(nombre="Recámara de Visitas", metros=12.0, tiene_bano_privado=False)

    print(f"[OK] Casa creada en: {mi_casa.direccion}")
    print(f"[OK] Total de habitaciones construidas (__len__): {len(mi_casa)}")

    print("\n" + "=" * 65)
    print("2. POLIMORFISMO, ITERACIÓN (__getitem__) Y PROPIEDADES (@property)")
    print("=" * 65)

    # Iteramos directamente sobre la instancia `mi_casa` gracias a __getitem__
    print("Desglose de espacios y mantenimiento mensual:")
    for indice, habitacion in enumerate(mi_casa, start=1):
        # Polimorfismo: cada subclase ejecuta su propia versión de describir() y calcular_costo_mantenimiento()
        costo = habitacion.calcular_costo_mantenimiento()
        print(f" {indice}. {habitacion.describir()} -> Mantenimiento: ${costo:,.2f}/mes")

    # Consultamos las propiedades calculadas de solo lectura (@property)
    print(f"\nÁrea total construida (@property): {mi_casa.area_total:.2f} m²")
    print(f"Costo total de mantenimiento mensual (@property): ${mi_casa.costo_mantenimiento_mensual:,.2f}")

    print("\n" + "=" * 65)
    print("3. MÉTODOS ESTÁTICOS (@staticmethod) Y VALIDACIÓN CON DESCRIPTORES")
    print("=" * 65)

    # Prueba del @staticmethod en la clase base Habitacion
    print(f"¿3.5 m² es dimensión habitacional válida?: {Habitacion.es_dimension_habitacional_valida(3.5)}")
    print(f"¿12.0 m² es dimensión habitacional válida?: {Habitacion.es_dimension_habitacional_valida(12.0)}")

    # Prueba de captura de error disparado por el descriptor ValidarMedidaPositiva
    print("\n--- Prueba de seguridad del Descriptor ---")
    try:
        mi_casa.construir_sala(nombre="Sala Imposible", metros=-10.0)
    except ValueError as error:
        print(f"[CAPTURADO] Error esperado en descriptor: {error}")

    print("\n" + "=" * 65)
    print("4. SERIALIZACIÓN Y EXPORTACIÓN A DISCO (JSON)")
    print("=" * 65)

    archivo_salida = "planos_casa.json"
    mi_casa.guardar_planos_json(archivo_salida)
    print(f"[ÉXITO] Planos arquitectónicos exportados correctamente a '{archivo_salida}'.")
    print("=" * 65)