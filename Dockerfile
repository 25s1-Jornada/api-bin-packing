# Imagem base leve com Python
FROM python:3.11-slim-bullseye

# Instala dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Docker CLI para comunicação com o host (opcional)
    docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

COPY ./data ./data

#CMD ["python", "main.py"]

CMD ["tail", "-f", "/dev/null"]
