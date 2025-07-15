from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Reporte(BaseModel):
    id: int
    autor: str = Field(..., example="Juan Pérez")
    titulo: str = Field(..., example="Luz rota en pasillo")
    descripcion: str = Field(..., example="La luz del segundo piso no enciende desde ayer")
    fecha: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    estado: Optional[str] = Field(default="pendiente", example="pendiente")  # pendiente | abierto | cerrado
    categoria: Optional[str] = Field(default="general", example="mantenimiento")
