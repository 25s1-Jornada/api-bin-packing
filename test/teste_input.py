import requests
import time
import os

base_url = "http://localhost:8000"
data_dir = "/app/data"  # se estiver rodando dentro do container

# 1. Cria a mesa
res = requests.post(f"{base_url}/table/new", json={"width": 800, "height": 600})
assert res.status_code == 200
table_id = int(res.json().replace('"', '').split(":")[1][:-1])
print(f"Mesa criada com ID {table_id}")

# 2. Envia camisetas
payload = {
    "type": "basic",
    "p": 2,
    "m": 2,
    "g": 1
}
res = requests.post(f"{base_url}/table/{table_id}/addMany", json=payload)
assert res.status_code == 200
print(f"Camisetas enviadas à mesa")

# 3. Aguarda output.json aparecer
print("Aguardando geração do output.json...")
for _ in range(20):  # até 10s
    if os.path.exists(f"{data_dir}/{table_id}/output.json"):
        print("Arquivo de saída encontrado.")
        break
    time.sleep(0.5)
else:
    raise TimeoutError("Timeout: output.json não encontrado")

# 4. Executa validações
os.system(f"python test/validacao_camiseta.py")
os.system(f"python test/validacao_tempo.py")
os.system(f"python test/validacao_espaco.py")
