from dataclasses import dataclass,field
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from casa import Casa
    from personas import Inquilino

@dataclass(frozen=True,order=True)
class ContratoRenta:

    monto_total_contrato: float = field(init=False) 
    folio: str = field(compare=False)
    direccion_propiedad: str = field(compare=False)
    nombre_inquilino: str = field(compare=False)
    identificacion_inquilino: str = field(compare=False)
    renta_mensual_acordada: float = field(compare=False)
    meses_duracion: int = field(compare=False)
    deposito_garantia: float = field(compare=False)
    fecha_firma: str = field(default_factory=lambda:datetime.now().strftime("%Y-%m-%d"),compare=False)

    def __post_init__(self):
        if not (self.meses_duracion >= 6 and self.deposito_garantia >= self.renta_mensual_acordada):
            raise ValueError("La duracion de la renta debe ser mayor a 6 meses,el deposito debe ser mayor que la renta mensual")

        folio_norm = self.folio.strip().upper()
        object.__setattr__(self,'folio',folio_norm)
        total = round(self.renta_mensual_acordada * self.meses_duracion,2)
        object.__setattr__(self,'monto_total_contrato',total)

    @classmethod
    def crear_desde_casa(cls,folio:str,casa:"Casa",
                         inquilino:"Inquilino",
                         meses_duracion:str,deposito_garantia:float) -> "ContratoRenta": 
        
        
        return cls(folio=folio,direccion_propiedad=casa.direccion,nombre_inquilino=inquilino.nombre,
                   identificacion_inquilino=inquilino.identificacion,
                   renta_mensual_acordada=casa.renta_mensual,
                   meses_duracion=meses_duracion,deposito_garantia=deposito_garantia)
     
@dataclass
class OrdenMantenimiento:

    codigo_origen: str
    nombre_area: str
    empresa_proveedora: str
    costo_base_servicio: float
    costo_extra_materiales: float = 0.0
    insumos: list[str] = field(default_factory=list)
    costo_total: float = field(init=False)

    def __post_init__(self):
        if  not (self.costo_base_servicio > 0  and self.costo_extra_materiales >= 0):
            raise ValueError("Costo base servicio y el costo de material es igual o menor que 0")

        self.codigo_origen = self.codigo_origen.strip().upper()
        self.costo_total = round(self.costo_base_servicio + self.costo_extra_materiales,2)

    def agregar_insumo(self,insumo:str,costo_insumo:float=0.0) -> None:
        if not costo_insumo >= 0:
            raise ValueError("El costo insumo tiene que ser mayor que 0")

        self.insumos.append(insumo)
        self.costo_total = round(self.costo_base_servicio + self.costo_extra_materiales,2)