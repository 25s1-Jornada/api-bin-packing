import time
import docker

input_path = "/app/data/input.json"
output_path = "/app/data/output.json"

client = docker.from_env()
container_name = "api-bin-packing-packingsolver-1"

start = time.time()

container = client.containers.get(container_name)
exec_result = container.exec_run(
    cmd=f"packingsolver_irregular -i {input_path} -c {output_path} --time-limit 120 -e"
)

end = time.time()
elapsed = end - start
print(f"⏱️ Tempo de execução: {elapsed:.2f} segundos")

assert elapsed <= 10.0, "Tempo de execução excedeu o limite de 10s"
print("Tempo de execução dentro do esperado.")
