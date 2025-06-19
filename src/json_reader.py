import json

def get_total_item_area(path):
    with open(path, "r") as f:
        data = json.load(f)

    total_area = 0
    for item in data["item_types"]:
        shape = item["shapes"][0]
        vertices = shape["vertices"]
        area = polygon_area(vertices)
        total_area += area * item["copies"]
    return total_area

def get_table_area(path):
    with open(path, "r") as f:
        data = json.load(f)

    bin_data = data["bin_types"][0]
    return bin_data["width"] * bin_data["height"]

def get_item_count(path):
    with open(path, "r") as f:
        data = json.load(f)

    return sum(item["copies"] for item in data["item_types"])

def polygon_area(vertices):
    # Shoelace formula
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i]["x"] * vertices[j]["y"]
        area -= vertices[j]["x"] * vertices[i]["y"]
    return abs(area) / 2
