from pydantic import BaseModel, Field, ValidationError

# 1. Definimos el "Contrato" (Modelo)
class RegistroEstudiante(BaseModel):
    # El nombre debe tener al menos 3 caracteres
    nombre: str = Field(min_length=3)
    
    # La edad debe estar entre 17 y 30 años
    edad: int = Field(ge=17, le=30)
    
    # El promedio no puede ser menor a 0.0 ni mayor a 5.0
    promedio: float = Field(ge=0.0, le=5.0)

# 2. CASO EXITOSO: Datos correctos
print("--- Intento 1: Datos válidos ---")
try:
    alumno_bueno = RegistroEstudiante(nombre="Andres", edad=20, promedio=4.5)
    print("Validación exitosa:", alumno_bueno.model_dump())
except ValidationError as e:
    print(e.json())

print("\n--- Intento 2: Datos inválidos ---")
# 3. CASO FALLIDO: Datos que rompen las reglas
try:
    # Aquí fallará porque la edad es muy baja y el promedio muy alto
    alumno_error = RegistroEstudiante(nombre="Al", edad=10, promedio=15.0)
except ValidationError as e:
    print("Se encontraron errores de validación:")
    # Pydantic nos dice exactamente qué falló
    for error in e.errors():
        campo = error['loc'][0]
        mensaje = error['msg']
        print(f"❌ Error en el campo '{campo}': {mensaje}")