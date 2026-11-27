from casa import Casa

class ProveedorMantenimiento:

    def __init__(self,nombre_empresa:str,especialidad:str,tarifa_mensual:float):
        self.nombre_empresa = nombre_empresa
        self.especialidad = especialidad
        if tarifa_mensual <= 0:

            raise ValueError("La tarifa mensual debe ser mayor a 0")
        
        self.tarifa_mensual = float(tarifa_mensual) 

    def __repr__(self):

        return f"Nombre de la empresa: {self.nombre_empresa},especialidad: {self.especialidad}"

class AreaComun:

    def __init__(self,nombre:str,capacidad_personas:int):
        self.nombre = nombre
        self.capacidad_personas = capacidad_personas
        self._proveedor: ProveedorMantenimiento | None = None

    @property
    def proveedor(self):

        return self._proveedor

    @proveedor.setter
    def proveedor(self,nuevo_proveedor:ProveedorMantenimiento):

        if not isinstance(nuevo_proveedor,ProveedorMantenimiento):
            raise TypeError("debe ser instancia de tipo ProveedorMantenimiento")

        self._proveedor = nuevo_proveedor

    @proveedor.deleter
    def proveedor(self):
        
        self._proveedor = None

    @property
    def costo_operativo_mensual(self) -> float:

        if self._proveedor: 
            return self._proveedor.tarifa_mensual

        return 0.0


class Condominio:

    def __init__(self,nombre:str,cuota_base_mantenimiento:float):

        self.nombre = nombre
        self.cuota_base_mantenimiento = cuota_base_mantenimiento
        self._areas_comunes: list[AreaComun] = []
        self._casas: list[Casa] = [] 

    def construir_area_comun(self,nombre:str,capacidad_personas:int) -> AreaComun:

        nombre_normalizado = nombre.strip().lower()
        if any(area.nombre.strip().lower() == nombre_normalizado for area in self._areas_comunes):
            raise ValueError(f"Ya existe un área común registrada con el nombre '{nombre}'")

        nueva_area_comun = AreaComun(nombre,capacidad_personas)
        self._areas_comunes.append(nueva_area_comun)

        return nueva_area_comun


    def incorporar_casa(self,casa:Casa) -> None:

        if not isinstance(casa,Casa):
            raise TypeError("La instancia no es de tipo Casa")
         
        direccion_nueva = casa.direccion.strip().lower()

        if any(c.direccion.strip().lower() == direccion_nueva for c in self._casas):
            raise ValueError(f"La casa en '{casa.direccion} ya esta incorporada en el condominio'")

        self._casas.append(casa)

    def desincorporar_casa(self,direccion:str) -> Casa:

        direccion_del = direccion.strip().lower()

        for i,casa in enumerate(self._casas):
            if casa.direccion.strip().lower() == direccion_del:
                return self._casas.pop(i)
                
        raise ValueError(f"No se encontro ninguna casa con la direccion '{direccion}' en el condominio")

    @property
    def presupuesto_mensual_areas_comunes(self) -> float:
        return sum(area.costo_operativo_mensual for area in self._areas_comunes)  

    @property
    def casas_disponibles(self) -> list[Casa]:
        return [casa for casa in self._casas if not casa.esta_ocupada]

        
    def  __len__(self):
        return len(self._casas)

    def __getitem__(self, key):

        return self._casas[key]
        


    
     





    