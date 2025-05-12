from fastapi import APIRouter, HTTPException
from app.schemas.meal import MealRequest, MealResponse
from app.models.ml_model import predict_meal
from app.utils.preprocessing import preprocess_input
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict", response_model=MealResponse)
async def predict(meal: MealRequest):
    try:
        # Logando os dados da requisição
        logger.info(f"Recebendo pedido de previsão com os dados: {meal}")

        # Verificando se os ingredientes foram fornecidos
        if not meal.ingredientes:
            raise HTTPException(status_code=400, detail="Ingredientes são obrigatórios.")
        
        # Preprocessando os dados de entrada
        ingredientes_vetor = preprocess_input(
            meal.ingredientes,
            meal.calorias,
            meal.carboidratos,
            meal.proteinas,
            meal.gorduras
        )

        # Realizando a predição
        classificacao, probabilidade = predict_meal(ingredientes_vetor)

        # Definindo a mensagem de retorno
        mensagem = "Refeição classificada como saudável" if classificacao == 1 else "Refeição classificada como não saudável"

        # Retornando a resposta
        return MealResponse(
            classificacao=classificacao,
            probabilidade=round(probabilidade, 2),
            mensagem=mensagem
        )
    
    except Exception as e:
        logger.error(f"Erro durante a previsão: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
