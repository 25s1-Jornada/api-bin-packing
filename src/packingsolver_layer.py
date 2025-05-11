import docker
from docker.errors import DockerException

client = docker.from_env()

def run_packingsolver(input_path: str, output_path: str):
    try:
        # Nome do container que já está rodando
        container = client.containers.get("api-bin-packing-packingsolver-1")  # <- Nome do container em execução
        
        # Executa o comando dentro do container rodando
        exec_result = container.exec_run(
            cmd="./app/src/irregular/packingsolver_irregular -i /app/data/input.json -c /app/data/output.json",
            workdir="/app"  # <- Define a pasta onde o comando vai rodar
        )

        print(exec_result.output.decode('utf-8'))
    except DockerException as e:
        print("Erro:", e)


if __name__ == "__main__":
    run_packingsolver("", "")
