from fastapi import FastAPI, HTTPException, Body
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Modelos
class Comentario(BaseModel):
    autor: str
    contenido: str
    fecha: str = datetime.now().strftime("%Y-%m-%d")

class Reporte(BaseModel):
    id: int
    autor: str
    titulo: str
    descripcion: str
    fecha: str
    estado: str
    categoria: str
    comentarios: List[Comentario] = []

class Usuario(BaseModel):
    id: int
    nombre: str
    correo: str
    contrasena: str

# Base de datos en memoria
reportes: List[Reporte] = []
id_actual = 1
usuarios: List[Usuario] = [
    Usuario(id=1, nombre="Juan Pérez", correo="juan@example.com", contrasena="1234"),
    Usuario(id=2, nombre="Ana Gómez", correo="ana@example.com", contrasena="5678")
]

# Endpoints Reportes
@app.get("/reportes", response_model=List[Reporte])
def obtener_reportes():
    return reportes

@app.get("/reportes/{id}", response_model=Reporte)
def obtener_reporte(id: int):
    for r in reportes:
        if r.id == id:
            return r
    raise HTTPException(status_code=404, detail="Reporte no encontrado")

@app.post("/reportes", response_model=Reporte)
def crear_reporte(reporte: Reporte):
    global id_actual
    reporte.id = id_actual
    id_actual += 1
    reportes.append(reporte)
    return reporte

@app.delete("/reportes/{id}", response_model=dict)
def eliminar_reporte(id: int):
    global reportes
    reportes = [r for r in reportes if r.id != id]
    return {"mensaje": f"Reporte {id} eliminado"}

@app.put("/reportes/{id}", response_model=Reporte)
def actualizar_reporte(id: int, reporte_actualizado: Reporte):
    for i, r in enumerate(reportes):
        if r.id == id:
            reporte_actualizado.id = id
            reporte_actualizado.comentarios = r.comentarios  # preserva los comentarios
            reportes[i] = reporte_actualizado
            return reporte_actualizado
    raise HTTPException(status_code=404, detail="Reporte no encontrado")

@app.post("/reportes/{id}/comentarios", response_model=Reporte)
def agregar_comentario(id: int, comentario: Comentario):
    for reporte in reportes:
        if reporte.id == id:
            reporte.comentarios.append(comentario)
            return reporte
    raise HTTPException(status_code=404, detail="Reporte no encontrado")

# Endpoints Usuarios
@app.get("/usuarios", response_model=List[Usuario])
def obtener_usuarios():
    return usuarios

@app.post("/login")
def login(correo: str = Body(...), contrasena: str = Body(...)):
    for usuario in usuarios:
        if usuario.correo == correo and usuario.contrasena == contrasena:
            return {"mensaje": "Login exitoso", "usuario": usuario}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")
