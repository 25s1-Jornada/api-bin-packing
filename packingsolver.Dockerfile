FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive

# Atualiza, instala dependências essenciais e pacotes de certificados SSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    git \
    wget \
    liblapack-dev \
    zlib1g-dev \
    coinor-libclp-dev \
    coinor-libcbc-dev \
    coinor-libcgl-dev \
    coinor-libcoinutils-dev \
    coinor-libosi-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala CMake 3.28 manualmente
RUN wget https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3-linux-x86_64.sh && \
    chmod +x cmake-3.28.3-linux-x86_64.sh && \
    ./cmake-3.28.3-linux-x86_64.sh --skip-license --prefix=/usr/local && \
    rm cmake-3.28.3-linux-x86_64.sh

# Define diretório de trabalho
WORKDIR /app

# Clona o projeto
RUN git clone https://github.com/fontanf/packingsolver.git .

# Cria diretório de build
#RUN mkdir build

RUN rm -rf ./data

RUN rm -rf ./test

#RUN find ./src -mindepth 1 -maxdepth 1 -type d ! -name 'irregular' -exec rm -rf {} +

#Compila
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DPACKINGSOLVER_BUILD_TEST=OFF
RUN cmake --build  ./build/src/irregular && cmake --install ./build/src/irregular --config Release --prefix install

#Exportar o path
RUN ln -s ./install/bin/packingsolver_irregular /bin/packingsolver_irregular
ENV PATH="/app/install/bin:${PATH}"

# Define o comando padrão
#CMD ["./packingsolver/bin/packingsolver"]
CMD ["tail", "-f", "/dev/null"]
