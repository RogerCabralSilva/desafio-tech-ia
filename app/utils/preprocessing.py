import joblib
import numpy as np
from fastapi import HTTPException
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

# Carrega o vectorizer
try:
    vectorizer = joblib.load("app/models/vectorizer.pkl")
    logger.info("Vectorizer carregado com sucesso.")
except (joblib.externals.loky.processes.TimeoutError, IOError) as e:
    logger.error(f"Erro ao carregar o vectorizer: {str(e)}")
    raise HTTPException(status_code=500, detail="Erro ao carregar o vectorizer.")

def preprocess_input(ingredientes, calorias, carboidratos, proteinas, gorduras):
    # Validação de dados de entrada
    if not ingredientes or not all(isinstance(i, str) for i in ingredientes):
        logger.warning(f"Dados inválidos para ingredientes: {ingredientes}")
        raise HTTPException(status_code=400, detail="Ingredientes devem ser uma lista de strings válidas.")
    
    if any(not isinstance(i, (int, float)) for i in [calorias, carboidratos, proteinas, gorduras]):
        logger.warning(f"Dados inválidos para as características nutricionais: {calorias}, {carboidratos}, {proteinas}, {gorduras}")
        raise HTTPException(status_code=400, detail="As características nutricionais devem ser números válidos.")

    # Preprocessa os ingredientes
    texto = " ".join(ingredientes)
    try:
        ingredientes_vector = vectorizer.transform([texto]).toarray()
    except Exception as e:
        logger.error(f"Erro ao vetorizar ingredientes: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar os ingredientes.")
    
    # Prepara as outras features numéricas
    outras_features = np.array([calorias, carboidratos, proteinas, gorduras]).reshape(1, -1)

    # Concatena todas as features
    features_final = np.concatenate([outras_features, ingredientes_vector], axis=1)

    return features_final
