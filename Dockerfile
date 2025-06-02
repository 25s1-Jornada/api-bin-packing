# Imagem base leve com Python
FROM python:3.11-slim-bullseye
WORKDIR /app

# Instala dependências do sistema (se necessário)
# Docker CLI para comunicação com o host (opcional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

#WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
COPY ./test/ ./test/ 

#RUN mkdir data
COPY ./data /data

EXPOSE 8000

CMD ["python", "main.py"]

#CMD ["tail", "-f", "/dev/null"]
