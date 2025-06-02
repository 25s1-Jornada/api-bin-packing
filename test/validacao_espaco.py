import json

output_path = "/app/data/output.json"

with open(output_path) as f:
    data = json.load(f)

mesa = data["bins"][0]["shape"]
mesa_width = max(p["xe"] for p in mesa)
mesa_height = max(p["ye"] for p in mesa)
mesa_area = mesa_width * mesa_height

total_area = 0
for bin in data.get("bins", []):
    for item in bin.get("items", []):
        for shape in item["item_shapes"]:
            for segment in shape["shape"]:
                width = abs(segment["xe"] - segment["xs"])
                height = abs(segment["ye"] - segment["ys"])
                total_area += width * height

uso_percentual = total_area / mesa_area

print(f"📏 Área mesa: {mesa_area:.2f}, ocupada: {total_area:.2f} → {uso_percentual:.2%}")

assert uso_percentual >= 0.95, f"Espaço ocupado abaixo de 95%: {uso_percentual:.2%}"
print("Utilização da mesa acima de 95%.")
