import joblib
import logging
from fastapi import HTTPException

# Configuração do logger
logger = logging.getLogger(__name__)

# Carrega o modelo com tratamento de exceções
try:
    model = joblib.load("app/models/best_model.pkl")
    logger.info("Modelo carregado com sucesso.")
except (joblib.externals.loky.processes.TimeoutError, IOError) as e:
    logger.error(f"Erro ao carregar o modelo: {str(e)}")
    raise HTTPException(status_code=500, detail="Erro ao carregar o modelo.")

def predict_meal(features_final):
    try:
        # Verificando se os dados de entrada são válidos
        if any(feature is None for feature in features_final):
            logger.warning("Dados de entrada para o modelo contêm valores nulos ou inválidos.")
            raise HTTPException(status_code=400, detail="Dados de entrada inválidos para o modelo.")
        
        # Fazendo a predição
        pred = model.predict(features_final)[0]
        proba = model.predict_proba(features_final).max()

        return pred, proba
    
    except Exception as e:
        logger.error(f"Erro durante a previsão: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao realizar a predição.")
