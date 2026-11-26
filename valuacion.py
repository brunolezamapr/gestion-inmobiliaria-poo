from abc import ABC,abstractmethod
from typing import TYPE_CHECKING 
if TYPE_CHECKING: from casa import Casa
from habitaciones import Recamara

class EstrategiaRenta(ABC):

    @abstractmethod
    def calcular_renta_mensual(self,casa:"Casa") -> float:
        pass


class RentaResidencial(EstrategiaRenta):

    def calcular_renta_mensual(self, casa) -> float:

        tarifa_base = casa.area_total * 18.0
        recamaras = len(casa.obtener_habitaciones_por_tipo(Recamara))
        bono_fijo = 120 * recamaras
        monto_total = tarifa_base + bono_fijo
        
        return monto_total


class RentaComercial(EstrategiaRenta):

    def calcular_renta_mensual(self, casa:"Casa") -> float:
        tarifa_base_comercial = casa.area_total * 32.0
        recargo_consumo_watts = casa.consumo_total_watts * 0.08
        monto_total = tarifa_base_comercial + recargo_consumo_watts

        return monto_total

    
        

    
        

        
        

    

