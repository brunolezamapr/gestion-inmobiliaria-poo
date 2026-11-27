"""
main.py - Suite de pruebas directas para el Sistema de Gestión Arquitectónica e Inmobiliaria (v6.0).
Demuestra composición multinivel, agregación, patrón Strategy, Condominio y Dataclasses (frozen, order, __post_init__).
"""

from dataclasses import FrozenInstanceError
from casa import Casa
from habitaciones import Habitacion, Sala, Cocina, Recamara
from exceptions import HabitacionDuplicadaError, CapacidadSuperadaError, CasaOcupadaError
from personas import Inquilino
from valuacion import RentaComercial, RentaResidencial, EstrategiaRenta
from condominio import Condominio, ProveedorMantenimiento
from contratos import ContratoRenta, OrdenMantenimiento

if __name__ == "__main__":
    print("=" * 70)
    print("1. CONSTRUCCIÓN DE CASA Y COMPOSICIÓN MULTINIVEL (EQUIPOS ELÉCTRICOS)")
    print("=" * 70)

    casa_reforma = Casa(direccion="Av. Paseo de la Reforma 450", area_maxima=120.0)

    sala = casa_reforma.construir_sala(nombre="Sala Principal", metros=30.0, tiene_balcon=True)
    cocina = casa_reforma.construir_cocina(nombre="Cocina Integral", metros=18.0, es_integral=True)
    rec1 = casa_reforma.construir_recamara(nombre="Recámara Principal", metros=22.0, tiene_bano_privado=True)
    rec2 = casa_reforma.construir_recamara(nombre="Recámara de Visitas", metros=15.0, tiene_bano_privado=False)

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
    print("2. AGREGACIÓN (INQUILINO) Y PATRÓN STRATEGY (VALUACIÓN DE RENTA)")
    print("=" * 70)

    inquilino1 = Inquilino("Carlos Mendoza", "CURP901215HDF")
    inquilino2 = Inquilino("Carlos Pérez", "INE880410MDF")

    casa_reforma.inquilino = inquilino1
    print(f"Renta Residencial: ${casa_reforma.renta_mensual:,.2f}")

    casa_reforma.estrategia_renta = RentaComercial()
    print(f"Renta Comercial:   ${casa_reforma.renta_mensual:,.2f}")

    # Restauramos estrategia residencial y desocupamos para las pruebas de contratos
    casa_reforma.estrategia_renta = RentaResidencial()
    try:
        casa_reforma.inquilino = inquilino2
    except CasaOcupadaError:
        print("[CAPTURADO - CASA OCUPADA]: La casa ya está ocupada.")

    del casa_reforma.inquilino
    print(f"¿Sigue ocupada tras `del`?: {casa_reforma.esta_ocupada} | Inquilino vivo afuera: {inquilino1}")

    print("\n" + "=" * 70)
    print("3. FILTRADO POLIMÓRFICO POR TIPO DE HABITACIÓN")
    print("=" * 70)

    recamaras = casa_reforma.obtener_habitaciones_por_tipo(Recamara)
    print(f"Recámaras encontradas en la propiedad: {len(recamaras)}")
    for rec in recamaras:
        print(f" - {rec.describir()} | Consumo interno: {rec.consumo_total_watts:.1f} W")

    print("\n" + "=" * 70)
    print("4. CAPTURA DE EXCEPCIONES PERSONALIZADAS DE DOMINIO")
    print("=" * 70)

    try:
        casa_reforma.construir_sala(nombre="Sala Principal", metros=15.0)
    except HabitacionDuplicadaError as err:
        print(f"[CAPTURADO - DUPLICADO]: {err}")

    try:
        casa_reforma.construir_recamara(nombre="Suite Terraza", metros=50.0)
    except CapacidadSuperadaError as err:
        print(f"[CAPTURADO - CAPACIDAD]: {err}")

    try:
        casa_reforma.construir_cocina(nombre="Cocineta Error", metros=-5.0)
    except ValueError as err:
        print(f"[CAPTURADO - DESCRIPTOR]: {err}")

    print("\n" + "=" * 70)
    print("5. SOBRECARGA DE OPERADORES (__lt__, __eq__) Y CATÁLOGO DE CASAS")
    print("=" * 70)

    casa_pequena = Casa(direccion="Calle Roble 12", area_maxima=80.0)
    casa_pequena.construir_sala("Sala Estar", 20.0)
    casa_pequena.construir_recamara("Recámara Única", 14.0)

    casa_grande = Casa(direccion="Lomas de Chapultepec 890", area_maxima=300.0)
    casa_grande.construir_sala("Gran Salón", 65.0, tiene_balcon=True)
    casa_grande.construir_cocina("Cocina Chef", 35.0, es_integral=True)
    casa_grande.construir_recamara("Master Suite", 45.0, tiene_bano_privado=True)

    catalogo = [casa_grande, casa_reforma, casa_pequena]
    print("Catálogo ordenado de menor a mayor área construida (sorted):")
    for pos, propiedad in enumerate(sorted(catalogo), start=1):
        print(f" {pos}. {propiedad}")

    print("\n" + "=" * 70)
    print("6. CONDOMINIO: COMPOSICIÓN PURA VS. AGREGACIÓN")
    print("=" * 70)

    prov_aqua = ProveedorMantenimiento("AquaClean S.A.", "Mantenimiento de Albercas", 450.0)
    residencial = Condominio("Residencial Bosque Real", cuota_base_mantenimiento=250.0)
    alberca = residencial.construir_area_comun("Alberca Olímpica", capacidad_personas=40)
    alberca.proveedor = prov_aqua

    residencial.incorporar_casa(casa_reforma)
    residencial.incorporar_casa(casa_grande)
    print(f"Total de casas en el condominio: {len(residencial)}")

    print("\n" + "=" * 70)
    print("7. CONTRATOS INMUTABLES Y ÓRDENES DE MANTENIMIENTO (@dataclass v6.0)")
    print("=" * 70)

    # A) Firma de contratos (asigna inquilino y genera ContratoRenta inmutable)
    contrato_1 = casa_reforma.firmar_contrato(
        folio="  ctr-2026-01 ",
        inquilino=inquilino1,
        meses_duracion=12,
        deposito_garantia=casa_reforma.renta_mensual,
    )

    contrato_2 = casa_pequena.firmar_contrato(
        folio="ctr-2026-02",
        inquilino=inquilino2,
        meses_duracion=6,
        deposito_garantia=casa_pequena.renta_mensual,
    )

    print(f"Contrato 1: {contrato_1}")
    print(f"Contrato 2: {contrato_2}")

    # B) Ordenamiento automático mediante @dataclass(order=True)
    print("\nContratos ordenados de menor a mayor monto total:")
    for c in sorted([contrato_1, contrato_2]):
        print(f" -> {c.folio} ({c.nombre_inquilino}): ${c.monto_total_contrato:,.2f}")

    # C) Verificación de inmutabilidad (frozen=True) y capacidad de hash (uso en set)
    auditoria_contratos = {contrato_1, contrato_2}
    print(f"\nContratos únicos en set de auditoría: {len(auditoria_contratos)}")
    try:
        contrato_1.renta_mensual_acordada = 500.0
    except FrozenInstanceError as err:
        print(f"[BLOQUEO INMUTABLE]: Imposible alterar contrato firmado ({type(err).__name__}).")

    # D) Orden de Mantenimiento mutable con field(default_factory=list)
    orden_alberca = OrdenMantenimiento(
        codigo_origen="  mnt-099 ",
        nombre_area=alberca.nombre,
        empresa_proveedora=prov_aqua.nombre_empresa,
        costo_base_servicio=250.0,
    )
    orden_alberca.agregar_insumo("Cloro granulado 10kg", 45.0)
    orden_alberca.agregar_insumo("Filtro de arena", 80.0)
    print(f"\nOrden de Mantenimiento: {orden_alberca}")

    print("\n" + "=" * 70)
    print("8. EXPORTACIÓN COMPLETA A JSON")
    print("=" * 70)

    archivo_json = "planos_casa_v6.json"
    casa_reforma.guardar_planos_json(archivo_json)
    print(f"[ÉXITO] Planos arquitectónicos guardados en '{archivo_json}'.")
    print("=" * 70)