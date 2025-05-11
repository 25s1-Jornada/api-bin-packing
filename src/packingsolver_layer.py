import docker
from docker.errors import DockerException

client = docker.from_env()

def run_packingsolver(input_path: str, output_path: str):
    try:
        # Nome do container que já está rodando
        container = client.containers.get("api-bin-packing-packingsolver-1")  # <- Nome do container em execução
        
        # Executa o comando dentro do container rodando
        # To rodando detach pq por algum motivo o packingsolver não finaliza a execução
        exec_result = container.exec_run(
            cmd="packingsolver_irregular -i /data/input.json -c /data/output.json -e",
            detach=True
        )
        
    except DockerException as e:
        print("Erro:", e)


if __name__ == "__main__":
    run_packingsolver("", "")
