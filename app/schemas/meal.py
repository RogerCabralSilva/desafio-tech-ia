from pydantic import BaseModel
from typing import List

# Modelo para a requisição
class MealRequest(BaseModel):
    ingredientes: List[str]
    calorias: int
    carboidratos: int
    proteinas: int
    gorduras: int

# Modelo para a resposta
class MealResponse(BaseModel):
    classificacao: int
    probabilidade: float
    mensagem: str
