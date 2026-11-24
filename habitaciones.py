from abc import ABC,abstractmethod
from descriptors import ValidarMedidaPositiva
from dataclasses import dataclass

@dataclass(frozen=True)
class EquipoElectrico:
    nombre: str
    consumo_watts: float


class Habitacion(ABC):

    metros_cuadrados = ValidarMedidaPositiva("metros_cuadrados")

    def __init__(self,nombre:str,metros_cuadrados:float):

        self.nombre = nombre
        self.metros_cuadrados = metros_cuadrados
        self._equipos: list[EquipoElectrico] = []

    def instalar_equipo(self,nombre:str,consumo_watts:float):
        nuevo_equipo_electrico = EquipoElectrico(nombre,consumo_watts)
        self._equipos.append(nuevo_equipo_electrico)

    @property
    def consumo_total_watts(self) -> float:
        return sum(equipo.consumo_watts for equipo in self._equipos)
        
    @abstractmethod
    def calcular_costo_mantenimiento(self) -> float:
        pass

    @abstractmethod
    def describir(self) -> str:
        return f"{self.nombre} - {self.metros_cuadrados}"

    @staticmethod
    def es_dimension_habitacional_valida(metros:float) -> bool:
        return metros >= 4.0

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "metros_cuadrados": self.metros_cuadrados,
            "tipo_clase": self.__class__.__name__
        }
    


class Sala(Habitacion):

    def __init__(self, nombre, metros_cuadrados,tiene_balcon:bool=False):
        super().__init__(nombre, metros_cuadrados)
        self.tiene_balcon = tiene_balcon

    def calcular_costo_mantenimiento(self):
        if self.tiene_balcon:
            return (self.metros_cuadrados * 12.0) + 50
        else:
            return self.metros_cuadrados * 12.0

    def describir(self):
        return super().describir()

    def to_dict(self):
        datos = super().to_dict()
        datos["tiene_balcon"] = self.tiene_balcon
        return datos


class Cocina(Habitacion):

    def __init__(self, nombre, metros_cuadrados,es_integral:bool=False):
        super().__init__(nombre, metros_cuadrados)
        self.es_integral = es_integral

    def calcular_costo_mantenimiento(self):
        if self.es_integral:
            return self.metros_cuadrados * 18.0
        else:
            return self.metros_cuadrados * 14.0

    def describir(self):
        return super().describir()

    def to_dict(self):
        datos = super().to_dict()
        datos["es_integral"] = self.es_integral
        return datos


class Recamara(Habitacion):

    def __init__(self, nombre, metros_cuadrados,tiene_bano_privado:bool=False):
        super().__init__(nombre, metros_cuadrados)
        self.tiene_bano_privado = tiene_bano_privado

    def calcular_costo_mantenimiento(self):
        if self.tiene_bano_privado:
            return (self.metros_cuadrados * 10.0) + 35
        else:
            return self.metros_cuadrados * 10.0

    def describir(self):
        return super().describir()

    def to_dict(self):
        datos = super().to_dict()
        datos["tiene_bano_privado"] = self.tiene_bano_privado
        return datos