from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Sistema de Gestión de Usuarios y Vehículos")

# --- MODELOS (Pydantic) ---
class Vehiculo(BaseModel):
    id: int
    marca: str
    modelo: str

# --- BASE DE DATOS SIMULADA ---
# Estructura de permisos según tu requerimiento
db_permisos = {
    1: "PUNTUACIONES/LEER",
    2: "PUNTUACIONES/CREAR",
    3: "PUNTUACIONES/ACTUALIZAR",
    4: "PUNTUACIONES/ELIMINAR"
}

# Definición de Roles
db_roles = {
    1: {"nombre": "Rol_1: Solo lectura", "permisos": [1]},
    2: {"nombre": "Rol_2: Solo escritura", "permisos": [2]},
    3: {"nombre": "Rol_3: Actualizar y eliminar", "permisos": [3, 4]}
}

# Usuarios con roles asignados
db_usuarios = {
    1: {"nombre": "Admin", "roles": [1, 2, 3]},
    2: {"nombre": "Editor", "roles": [2, 3]},
    3: {"nombre": "Lector", "roles": [1]}
}

db_vehiculos = [
    {"id": 1, "marca": "Toyota", "modelo": "Hilux"},
    {"id": 2, "marca": "Tesla", "modelo": "Model 3"}
]

# --- ENDPOINTS DE USUARIOS ---

@app.get("/usuarios")
def listar_usuarios():
    return db_usuarios

@app.get("/usuarios/{id}")
def obtener_usuario(id: int):
    if id not in db_usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuarios[id]

@app.get("/usuarios/{id}/roles")
def obtener_roles_usuario(id: int):
    if id not in db_usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return [db_roles[rol_id] for rol_id in db_usuarios[id]["roles"]]

@app.get("/usuarios/{id}/permisos")
def obtener_permisos_usuario(id: int):
    if id not in db_usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    permisos_finales = set()
    for rol_id in db_usuarios[id]["roles"]:
        for perm_id in db_roles[rol_id]["permisos"]:
            permisos_finales.add(db_permisos[perm_id])
    return sorted(list(permisos_finales))

# --- ENDPOINTS DE ROLES Y PERMISOS ---

@app.get("/roles")
def listar_roles():
    return db_roles

@app.get("/roles/{id}/permisos")
def obtener_permisos_del_rol(id: int):
    if id not in db_roles:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return [db_permisos[p_id] for p_id in db_roles[id]["permisos"]]

@app.get("/permisos")
def listar_permisos():
    return db_permisos

# --- CRUD DE VEHICULOS ---

@app.get("/vehiculos")
def listar_vehiculos():
    return db_vehiculos

@app.get("/vehiculos/{id}")
def obtener_vehiculo(id: int):
    vehiculo = next((v for v in db_vehiculos if v["id"] == id), None)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

@app.post("/vehiculos", status_code=201)
def crear_vehiculo(vehiculo: Vehiculo):
    db_vehiculos.append(vehiculo.dict())
    return {"mensaje": "Vehículo registrado con éxito", "data": vehiculo}

@app.put("/vehiculos/{id}")
def actualizar_vehiculo(id: int, vehiculo_data: Vehiculo):
    for index, v in enumerate(db_vehiculos):
        if v["id"] == id:
            db_vehiculos[index] = vehiculo_data.dict()
            return {"mensaje": "Vehículo actualizado"}
    raise HTTPException(status_code=404, detail="Vehículo no encontrado")

@app.delete("/vehiculos/{id}")
def eliminar_vehiculo(id: int):
    global db_vehiculos
    original_size = len(db_vehiculos)
    db_vehiculos = [v for v in db_vehiculos if v["id"] != id]
    if len(db_vehiculos) == original_size:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return {"mensaje": "Vehículo eliminado"}