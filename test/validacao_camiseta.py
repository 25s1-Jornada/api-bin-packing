import json
import os

input_path = "/app/data/input.json"
output_path = "/app/data/output.json"

def count_input_items(data):
    return sum(item["copies"] for item in data["item_types"])

def count_output_items(data):
    return sum(1 for bin in data.get("bins", []) for _ in bin.get("items", []))

with open(input_path) as f:
    input_data = json.load(f)

with open(output_path) as f:
    output_data = json.load(f)

input_count = count_input_items(input_data)
output_count = count_output_items(output_data)

print(f"Input: {input_count} peças, Output: {output_count} peças")

assert input_count == output_count, f"Quantidade divergente: input={input_count}, output={output_count}"
print("Quantidade de peças conferida com sucesso.")
