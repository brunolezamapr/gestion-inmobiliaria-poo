# 🏠 Sistema de Gestión Arquitectónica e Inmobiliaria (POO en Python)

Un proyecto modular desarrollado en **Python** que demuestra la aplicación práctica de principios avanzados de **Programación Orientada a Objetos (POO)**, centrado en el patrón de **Composición Pura**, acompañado de Herencia, Polimorfismo, Descriptores de validación y Serialización JSON.

---

## 📌 ¿Por qué este proyecto? (Conceptos Clave de POO)

Al modelar sistemas donde los objetos complejos están formados por partes internas (como una casa y sus habitaciones), aplicar **Composición sobre Herencia** evita jerarquías rígidas y garantiza un ciclo de vida cohesivo. En este proyecto integramos los siguientes pilares técnicos:

### 1. Composición Pura (`Casa` y `Habitacion`)
* **Ciclo de vida acoplado:** La clase contenedora `Casa` recibe únicamente su `direccion` (un `str`) al instanciarse. Nunca recibe objetos `Habitacion` creados externamente.
* **Construcción encapsulada:** A través de métodos constructores internos (`construir_sala()`, `construir_cocina()`, `construir_recamara()`), `Casa` instancia y administra exclusivamente sus propios componentes. Si la casa se elimina de memoria, sus habitaciones desaparecen con ella.

### 2. Herencia, Clases Base Abstractas y Polimorfismo (`ABC`)
* **`Habitacion(ABC)`:** Define el contrato obligatorio para cualquier espacio arquitectónico mediante `@abstractmethod` (`calcular_costo_mantenimiento()` y `describir()`).
* **Subclases Especializadas (`Sala`, `Cocina`, `Recamara`):** Extienden la clase base usando `super()` e implementan sus propias reglas de cálculo de mantenimiento y serialización (`to_dict()`).
* **Despacho Polimórfico:** `Casa` calcula el presupuesto mensual recorriendo sus habitaciones e invocando `hab.calcular_costo_mantenimiento()` sin importar el tipo concreto de cada habitación.

### 3. Descriptores de Validación Reusables (`ValidarMedidaPositiva`)
* Implementa el protocolo descriptor (`__get__` y `__set__`) a nivel de clase para actuar como guardián de `metros_cuadrados`.
* Garantiza que cualquier dimensión asignada sea un número (`int` o `float`) estrictamente mayor a `0`, lanzando un `ValueError` en caso contrario y almacenando el dato limpiamente en `instance.__dict__`.

### 4. Propiedades Calculadas (`@property`) y Métodos Estáticos (`@staticmethod`)
* **`@property` (`area_total` y `costo_mantenimiento_mensual`):** Atributos de solo lectura calculados dinámicamente en tiempo real a partir de las habitaciones compuestas.
* **`@staticmethod` (`es_dimension_habitacional_valida`):** Función utilitaria pura en `Habitacion` (independiente de `self` y `cls`) que verifica si una medida cumple con el mínimo reglamentario ($\ge 4.0\text{ m}^2$).

### 5. Protocolo de Colección (Métodos Dunder) y Serialización JSON
* **`__len__` y `__getitem__`:** Permiten consultar el número de habitaciones con `len(mi_casa)`, acceder por índice (`mi_casa[0]`) e iterar directamente sobre la instancia (`for hab in mi_casa:`).
* **`guardar_planos_json()`:** Exporta la estructura completa de la propiedad y el detalle polimórfico de cada habitación a un archivo `.json`.

---

## 📁 Arquitectura del Proyecto

```text
gestion_inmobiliaria/
│
├── descriptors.py    # Descriptor reusable ValidarMedidaPositiva (__get__ / __set__)
├── habitaciones.py   # Clase base abstracta Habitacion(ABC) y subclases Sala, Cocina, Recamara
├── casa.py           # Clase contenedora Casa con Composición Pura, @property y Dunder methods
├── main.py           # Suite de pruebas integrales y exportación a JSON
├── .gitignore        # Exclusión de archivos compilados (__pycache__) y salidas *.json
└── README.md         # Documentación técnica del proyecto
```

---

## 🚀 Guía de Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/brunolezamapr/gestion-inmobiliaria-poo.git
cd gestion-inmobiliaria-poo
```

### 2. Ejecutar la suite de pruebas
```bash
python3 main.py
```

### 3. Ejemplo de Uso
```python
from casa import Casa

# 1. Crear la casa (Composición pura: inicia sin habitaciones externas)
mi_casa = Casa("Av. Paseo de la Reforma 450, CDMX")

# 2. Construir habitaciones internamente
mi_casa.construir_sala(nombre="Sala Principal", metros=28.0, tiene_balcon=True)
mi_casa.construir_cocina(nombre="Cocina Integral", metros=14.5, es_integral=True)
mi_casa.construir_recamara(nombre="Recámara Principal", metros=20.0, tiene_bano_privado=True)

# 3. Consultar propiedades calculadas y protocolo de colección
print(f"Total de espacios: {len(mi_casa)}")
print(f"Área total: {mi_casa.area_total:.2f} m²")
print(f"Mantenimiento mensual: ${mi_casa.costo_mantenimiento_mensual:,.2f}")

# 4. Exportar planos arquitectónicos a JSON
mi_casa.guardar_planos_json("planos_casa.json")
```