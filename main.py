"""
main.py - Suite de pruebas directas para el Sistema de Gestión Arquitectónica e Inmobiliaria (v2.0).
Demuestra composición multinivel (Casa -> Habitacion -> EquipoElectrico),
excepciones de dominio, filtrado polimórfico, sobrecarga de operadores y exportación JSON.
 """

from casa import Casa
from habitaciones import Habitacion, Sala, Cocina, Recamara
from exceptions import HabitacionDuplicadaError, CapacidadSuperadaError,CasaOcupadaError
from personas import Inquilino
from valuacion import RentaComercial,RentaResidencial,EstrategiaRenta
from condominio import Condominio,ProveedorMantenimiento

print("=" * 70)
print("1. CONSTRUCCIÓN DE CASA Y COMPOSICIÓN MULTINIVEL (EQUIPOS ELÉCTRICOS)")
print("=" * 70)

# Creamos la casa con dirección y límite máximo de terreno (120.0 m²)
casa_reforma = Casa(direccion="Av. Paseo de la Reforma 450", area_maxima=120.0)

# Construimos habitaciones internamente (Composición nivel 1)
sala = casa_reforma.construir_sala(nombre="Sala Principal", metros=30.0, tiene_balcon=True)
cocina = casa_reforma.construir_cocina(nombre="Cocina Integral", metros=18.0, es_integral=True)
rec1 = casa_reforma.construir_recamara(nombre="Recámara Principal", metros=22.0, tiene_bano_privado=True)
rec2 = casa_reforma.construir_recamara(nombre="Recámara de Visitas", metros=15.0, tiene_bano_privado=False)

inquilino1 = Inquilino("Carlos Mendoza","CURP901215HDF")
inquilino2 = Inquilino("Carlos Pérez","CURP901215HDF")

casa_reforma.inquilino = inquilino1
print(casa_reforma.renta_mensual)
casa_reforma.estrategia_renta = RentaComercial()
print(casa_reforma.renta_mensual)
try:
    casa_reforma.inquilino = inquilino2

except CasaOcupadaError as err:
    print("La casa ya esta ocupada")

del casa_reforma.inquilino
print(casa_reforma.esta_ocupada)
print(inquilino1)

# Instalamos equipos eléctricos dentro de cada habitación (Composición nivel 2)
sala.instalar_equipo("Smart TV 65 OLED", 180.0)
sala.instalar_equipo("Aire Acondicionado Inverter", 1200.0)

cocina.instalar_equipo("Refrigerador Duplex", 250.0)
cocina.instalar_equipo("Horno Eléctrico", 1800.0)

rec1.instalar_equipo("Calefactor Ambiental", 1500.0)

print(f"[OK] Propiedad creada: {casa_reforma}")
print(f" -> Área total construida (@property): {casa_reforma.area_total:.2f} m²")
print(f" -> Mantenimiento mensual (@property): ${casa_reforma.costo_mantenimiento_mensual:,.2f}")
print(f" -> Consumo eléctrico total (@property): {casa_reforma.consumo_total_watts:,.2f} Watts")

print("\n" + "=" * 70)
print("2. FILTRADO POLIMÓRFICO POR TIPO DE HABITACIÓN")
print("=" * 70)

recamaras = casa_reforma.obtener_habitaciones_por_tipo(Recamara)
print(f"Recámaras encontradas en la propiedad: {len(recamaras)}")
for rec in recamaras:
    print(f" - {rec.describir()} | Consumo interno: {rec.consumo_total_watts:.1f} W")

print("\n" + "=" * 70)
print("3. CAPTURA DE EXCEPCIONES PERSONALIZADAS DE DOMINIO")
print("=" * 70)

# A) Prueba de HabitacionDuplicadaError
try:
    casa_reforma.construir_sala(nombre="Sala Principal", metros=15.0)
except HabitacionDuplicadaError as err:
    print(f"[CAPTURADO - DUPLICADO]: {err}")

# B) Prueba de CapacidadSuperadaError (actual: 85 m² + 50 m² > 120 m²)
try:
    casa_reforma.construir_recamara(nombre="Suite Terraza", metros=50.0)
except CapacidadSuperadaError as err:
    print(f"[CAPTURADO - CAPACIDAD]: {err}")

# C) Prueba del descriptor ValidarMedidaPositiva
try:
    casa_reforma.construir_cocina(nombre="Cocineta Error", metros=-5.0)
except ValueError as err:
    print(f"[CAPTURADO - DESCRIPTOR]: {err}")

print("\n" + "=" * 70)
print("4. SOBRECARGA DE OPERADORES (__lt__, __eq__) Y CATÁLOGO DE CASAS")
print("=" * 70)

casa_pequena = Casa(direccion="Calle Roble 12", area_maxima=80.0)
casa_pequena.construir_sala("Sala Estar", 20.0)
casa_pequena.construir_recamara("Recámara Única", 14.0)

casa_grande = Casa(direccion="Lomas de Chapultepec 890", area_maxima=300.0)
casa_grande.construir_sala("Gran Salón", 65.0, tiene_balcon=True)
casa_grande.construir_cocina("Cocina Chef", 35.0, es_integral=True)
casa_grande.construir_recamara("Master Suite", 45.0, tiene_bano_privado=True)

# Ordenamiento nativo usando __lt__
catalogo = [casa_grande, casa_reforma, casa_pequena]
print("Catálogo ordenado de menor a mayor área construida (sorted):")
for pos, propiedad in enumerate(sorted(catalogo), start=1):
    print(f" {pos}. {propiedad}")

# Comparación de igualdad usando __eq__
casa_clon = Casa(direccion="  av. paseo de la reforma 450  ", area_maxima=120.0)
casa_clon.construir_sala("A", 10.0)
casa_clon.construir_cocina("B", 10.0)
casa_clon.construir_recamara("C", 10.0)
casa_clon.construir_recamara("D", 10.0)

print(f"\n¿casa_reforma == casa_clon (misma dirección y 4 cuartos)?: {casa_reforma == casa_clon}")

print("\n" + "=" * 70)
print("5. EXPORTACIÓN COMPLETA A JSON (CON EQUIPOS ELÉCTRICOS)")
print("=" * 70)

archivo_json = "planos_casa_v2.json"
casa_reforma.guardar_planos_json(archivo_json)
print(f"[ÉXITO] Planos arquitectónicos y carga eléctrica guardados en '{archivo_json}'.")
print("=" * 70)

print("\n" + "=" * 70)
print("6. CONDOMINIO: COMPOSICIÓN PURA VS. AGREGACIÓN DE PROVEEDORES Y CASAS")
print("=" * 70)

# 1. Crear proveedores externos (Agregación: nacen afuera de AreaComun)
prov_aqua = ProveedorMantenimiento("AquaClean S.A.", "Mantenimiento de Albercas", 450.0)
prov_gym = ProveedorMantenimiento("FitTech Pro", "Equipos de Gimnasio", 320.0)

# 2. Instanciar Condominio y construir áreas comunes internamente (Composición pura)
residencial = Condominio("Residencial Bosque Real", cuota_base_mantenimiento=250.0)
alberca = residencial.construir_area_comun("Alberca Olímpica", capacidad_personas=40)
gimnasio = residencial.construir_area_comun("Gimnasio Panorámico", capacidad_personas=25)

# 3. Vincular proveedores mediante @proveedor.setter (Agregación)
alberca.proveedor = prov_aqua
gimnasio.proveedor = prov_gym

print(f"Presupuesto mensual de áreas comunes: ${residencial.presupuesto_mensual_areas_comunes:,.2f}")

# Desvincular proveedor con `del` (@proveedor.deleter): el objeto sigue vivo afuera
del alberca.proveedor
print(f"Tras cancelar contrato en alberca -> Presupuesto: ${residencial.presupuesto_mensual_areas_comunes:,.2f}")
print(f"¿El proveedor externo sigue existiendo en memoria?: {prov_aqua}")

# 4. Incorporar casas existentes al condominio (Agregación)
residencial.incorporar_casa(casa_reforma)
residencial.incorporar_casa(casa_grande)

print(f"\nTotal de casas en el condominio (__len__): {len(residencial)}")
print(f"Casas disponibles para rentar (@property): {len(residencial.casas_disponibles)}")

# Desincorporar una casa y verificar que conserva sus habitaciones y equipos intactos
casa_retirada = residencial.desincorporar_casa("Av. Paseo de la Reforma 450")
print(f"Casa desincorporada: {casa_retirada} | Cuartos intactos: {len(casa_retirada)}")
print(f"Casas restantes en el condominio: {len(residencial)}")

