from fastapi import FastAPI, HTTPException
from typing import List
from models import Reporte

app = FastAPI()

# Base de datos en memoria
reportes: List[Reporte] = []
id_actual = 1

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
            reportes[i] = reporte_actualizado
            return reporte_actualizado
    raise HTTPException(status_code=404, detail="Reporte no encontrado")
