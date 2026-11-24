class InmobiliariaError(Exception):
    pass


class CapacidadSuperadaError(InmobiliariaError):

    """Capacidad sobrepasa el terreno máximo de la casa"""

class HabitacionDuplicadaError(InmobiliariaError):
    """No puede haber 2 habitaciones con el mismo nombre"""

    