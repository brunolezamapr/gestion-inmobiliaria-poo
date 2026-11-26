
class Inquilino:

    def __init__(self,nombre:str,identificacion:str):
        
        self.nombre = nombre.strip()
        if not self.es_identificacion_valida(identificacion):
            raise ValueError("La identificacion no es valida")
        self.identificacion = identificacion.strip().upper()

    @staticmethod
    def es_identificacion_valida(identificacion:str) -> bool:
        return 8 <= len(identificacion.strip()) <= 18 and isinstance(identificacion,str) 


    def __repr__(self):
        return f"Nombre inquilino: {self.nombre},Identificacion (DNI,INE): {self.identificacion}" 



        

    