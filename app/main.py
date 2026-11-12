"""API de calculadora con FastAPI.

Endpoints:
- GET  /                         -> mensaje de bienvenida
- GET  /calcular/{operacion}     -> calcula con parámetros en la URL (?a=..&b=..)
- POST /calcular                 -> calcula con los datos enviados en un JSON
"""
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Calculadora",
    description="Pequeña API de ejemplo: suma, resta, multiplica y divide dos números.",
    version="1.0.0",
)


class Operacion(str, Enum):
    """Operaciones permitidas. Swagger las muestra como un desplegable."""
    sumar = "sumar"
    restar = "restar"
    multiplicar = "multiplicar"
    dividir = "dividir"


class PeticionCalculo(BaseModel):
    """Cuerpo JSON que espera el endpoint POST."""
    a: float = Field(..., examples=[8])
    b: float = Field(..., examples=[2])
    operacion: Operacion = Field(..., examples=["dividir"])


def calcular(a: float, b: float, operacion: Operacion) -> float:
    """Lógica de la calculadora, compartida por GET y POST."""
    if operacion == Operacion.sumar:
        return a + b
    if operacion == Operacion.restar:
        return a - b
    if operacion == Operacion.multiplicar:
        return a * b
    # dividir
    if b == 0:
        # 400 = error del cliente: ha pedido algo imposible
        raise HTTPException(status_code=400, detail="No se puede dividir entre 0")
    return a / b


@app.get("/")
def inicio():
    """Comprueba que la API está viva."""
    return {
        "mensaje": "Bienvenido a la API Calculadora",
        "operaciones": [op.value for op in Operacion],
        "documentacion": "/docs",
    }


@app.get("/calcular/{operacion}")
def calcular_get(operacion: Operacion, a: float, b: float):
    """Ejemplo: /calcular/sumar?a=5&b=3"""
    resultado = calcular(a, b, operacion)
    return {"operacion": operacion, "a": a, "b": b, "resultado": resultado}


@app.post("/calcular")
def calcular_post(peticion: PeticionCalculo):
    """Ejemplo de cuerpo: {"a": 8, "b": 2, "operacion": "dividir"}"""
    resultado = calcular(peticion.a, peticion.b, peticion.operacion)
    return {
        "operacion": peticion.operacion,
        "a": peticion.a,
        "b": peticion.b,
        "resultado": resultado,
    }
