class ValidarMedidaPositiva:

    def __init__(self,nombre_atributo):

        self.nombre_atributo = nombre_atributo



def __get__(self, instance, owner):

    if instance is None:

        return self

    return instance.__dict__.get(self.nombre_atributo)



def __set__(self, instance, value):

    if not isinstance(value,float) or value <= 0:

        raise ValueError(f"{self.nombre_atributo} debe ser un entero mayor que 0")

    instance.__dict__[self.nombre_atributo] = value