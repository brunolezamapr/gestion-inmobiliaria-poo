"""
Módulo de la Clase Contenedora `Casa`.

Implementa el principio de Composición Pura: las instancias de `Sala`, `Cocina`
y `Recamara` son creadas exclusivamente dentro de los métodos de `Casa` y comparten
su ciclo de vida. Además, expone propiedades calculadas (`@property`), protocolos
de colección mediante métodos dunder (`__len__`, `__getitem__`) y serialización JSON.
"""

import json
from habitaciones import Habitacion, Sala, Cocina, Recamara
from exceptions import HabitacionDuplicadaError,InmobiliariaError,CapacidadSuperadaError

class Casa:
    """
    Representa una propiedad inmobiliaria compuesta internamente por habitaciones.
    """

    def __init__(self, direccion: str,area_maxima:float=500.0):
        """
        Inicializa una casa vacía a partir de su dirección.
        Nota: No recibe objetos `Habitacion` externos para garantizar composición pura.
        """
        if area_maxima <= 0:
            raise ValueError("El área máxima de la casa debe ser mayor a 0 m2")
        self.direccion = direccion
        self._habitaciones: list[Habitacion] = []
        self.area_maxima = float(area_maxima)
    # --- MÉTODOS CONSTRUCTORES INTERNOS (Composición Pura) ---

    def _validar_nueva_habitacion(self,nombre:str,metros:float) -> None:

        nombre_normalizado = nombre.strip().lower()
        if any(hab.nombre.strip().lower() == nombre_normalizado for hab in self._habitaciones):
            raise HabitacionDuplicadaError(
                f"Ya existe una habitacion registrada con el nombre '{nombre}'."
            )

        if self.area_total + metros > self.area_maxima:
            raise CapacidadSuperadaError(
                f"No se puede construir '{nombre}' ({metros} m2): se excede el límite"
                f"del terreno ({self.area_total + metros:.2f} m2 / {self.area_maxima:.2f})"
            )
        
    def construir_sala(
        self, nombre: str, metros: float, tiene_balcon: bool = False
    ) -> None:
        """Instancia una `Sala` internamente y la incorpora a la casa."""
        self._validar_nueva_habitacion(nombre,metros)
        nueva_sala = Sala(nombre, metros, tiene_balcon)
        self._habitaciones.append(nueva_sala)
        return nueva_sala

    def construir_cocina(
        self, nombre: str, metros: float, es_integral: bool = True
    ) -> None:
        """Instancia una `Cocina` internamente y la incorpora a la casa."""
        self._validar_nueva_habitacion(nombre,metros)
        nueva_cocina = Cocina(nombre, metros, es_integral)
        self._habitaciones.append(nueva_cocina)
        return nueva_cocina

    def construir_recamara(
        self, nombre: str, metros: float, tiene_bano_privado: bool = False
    ) -> None:
        """Instancia una `Recamara` internamente y la incorpora a la casa."""
        self._validar_nueva_habitacion(nombre,metros)
        nueva_recamara = Recamara(nombre, metros, tiene_bano_privado)
        self._habitaciones.append(nueva_recamara)
        return nueva_recamara
    # --- PROPIEDADES CALCULADAS (@property) ---

    @property
    def area_total(self) -> float:
        """Calcula dinámicamente la suma de metros cuadrados de todas las habitaciones."""
        return sum(hab.metros_cuadrados for hab in self._habitaciones)

    @property
    def costo_mantenimiento_mensual(self) -> float:
        """
        Calcula el costo total de mantenimiento invocando polimórficamente
        `calcular_costo_mantenimiento()` en cada habitación compuesta.
        """
        return sum(hab.calcular_costo_mantenimiento() for hab in self._habitaciones)

    

    @property
    def consumo_total_watts(self) -> float:
        return sum(hab.consumo_total_watts for hab in self._habitaciones)

    # --- SERIALIZACIÓN A DISCO ---
    def guardar_planos_json(self, ruta_archivo: str) -> None:
        """Serializa la dirección y todas las habitaciones polimórficas a un archivo JSON."""
        dict_casa = {
            "direccion": self.direccion,
            "area_total_m2": self.area_total,
            "costo_mantenimiento_mensual": self.costo_mantenimiento_mensual,
            "consumo_total_watts": self.consumo_total_watts,
            "habitaciones": [hab.to_dict() for hab in self._habitaciones],
        }

        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(dict_casa, f, indent=4, ensure_ascii=False)

    def obtener_habitaciones_por_tipo(self,clase_habitacion:type) -> list[Habitacion]:
        if not isinstance(clase_habitacion,type) or not  issubclass(
            clase_habitacion,Habitacion):
            raise TypeError("El argumento debe ser una subclase válida de Habitación")
        return [hab for hab in self._habitaciones if isinstance(hab,clase_habitacion)]

    # --- PROTOCOLO DE COLECCIÓN Y REPRESENTACIÓN (Métodos Dunder) ---

    def __lt__(self, otra_casa:"Casa") -> bool:
        if not isinstance(otra_casa,Casa):
            return NotImplemented
        return self.area_total < otra_casa.area_total

    def __eq__(self, otra_casa:"Casa"):
        if not isinstance(otra_casa,Casa):
            return NotImplemented
        return self.direccion.strip().lower() == otra_casa.direccion.strip().lower() and len(self) == len(otra_casa)
    def __len__(self) -> int:
        """Permite consultar el total de habitaciones con `len(mi_casa)`."""
        return len(self._habitaciones)

    def __getitem__(self, key: int) -> Habitacion:
        """Permite acceder por índice (`mi_casa[0]`) e iterar con `for hab in mi_casa`."""
        return self._habitaciones[key]

    def __repr__(self) -> str:
        return (
            f"Casa(direccion='{self.direccion}', "
            f"habitaciones={len(self)}, area_total={self.area_total:.2f} m²)"
        )