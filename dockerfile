# Use uma imagem base com Python
FROM python:3.11-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de requisitos
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto para o container
COPY . /app/

# Expor a porta do FastAPI (geralmente 8000)
EXPOSE 8000

# Comando para rodar a aplicação FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
