from fastapi import FastAPI
from app.api.endpoints import router  # Importa o router das rotas definidas em endpoints.py

# Instancia o FastAPI
app = FastAPI()

# Inclui as rotas (importa o router que está no endpoints.py)
app.include_router(router)
