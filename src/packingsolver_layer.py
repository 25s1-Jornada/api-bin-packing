from ast import Tuple
import uuid
import docker
from docker.errors import DockerException
import json
import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
from typing import Dict, List, Union, Optional
import os

from models import GartmentTable, ShirtPoligon

client = docker.from_env()
                                                 #[int, ShirtPoligon]       
def execute_action(clientId, vertices_list: List[Tuple], table: GartmentTable):
    # Cria o JSON de entrada
    dirname = f"/data/{clientId}"
    input_json_path = create_input_json(clientId, vertices_list, table, dirname=dirname)
    
    # Executa o packingsolver
    output_json_path = f"{dirname}/output.json"
    resume = run_packingsolver(input_json_path, output_json_path)
    
    # Lê o JSON de saída
    with open(output_json_path, 'r') as f:
        data = json.load(f)
    
    # Extrai os vértices
    simplified_items = extract_vertices(data)
    
    # Plota a solução
    plot_solution(data, save_as=f"/data/{clientId}/output.png")
    
    return simplified_items

def run_packingsolver(input_path: str, output_path: str):
    try:
        # Nome do container que já está rodando
        container = client.containers.get("api-bin-packing-packingsolver-1")  # <- Nome do container em execução
        
        # Executa o comando dentro do container rodando
        # To rodando detach pq por algum motivo o packingsolver não finaliza a execução
        exec_result = container.exec_run(
            cmd=f"packingsolver_irregular -i {input_path} -c {output_path} --time-limit 120 -e",
            #detach=True
        )
        
        print(exec_result.output.decode('utf-8'))
        
    except DockerException as e:
        print("Erro:", e)
                                                 #[int, ShirtPoligon]       
def create_input_json(clientId, vertices_list: List[Tuple], table: GartmentTable, dirname: str = "/data/") -> str:
    generated_json = generate_json(vertices_list, table.width, table.height)
    
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    with open(f"{dirname}/input.json", "w") as f:
        json.dump(generated_json, f)
    print("Input JSON created:", generated_json)
    
    return f"{dirname}/input.json"
    
                                  #[int, ShirtPoligon]       
def generate_json(vertices_list: List[Tuple],
                  width: float,
                  height: float,
#                  copies_per_item: Optional[int] = 1,
                  item_copies: Optional[int] = 3) -> Dict:

    non_sleeve_items = []
    sleeve_items = []

    
    shirt_id = uuid.uuid4()
        ## aqui eu preciso achar um jeito de melhorar esses tipos para verificar as quantidades
    for vertices in vertices_list:
        
        copies = vertices[0]
        
        for vert in vertices[1]:
            item = {
                "copies": copies,
                "allow_mirroring": True,
                "shapes": [
                    {
                        "id": str(shirt_id) + str(vert.type),
                        "type": "polygon",
                        "copies": 1,
                        "vertices": vert.vertices,
                        "holes": []
                    }
                ]
            }
            if vert.type.lower() == "manga":
                sleeve_items.append(item)
            else:
                non_sleeve_items.append(item)
                
    item_types = non_sleeve_items + sleeve_items

    result = {
        "objective": "open-dimension-x",
        "parameters": {
            "item_bin_minimum_spacing": 0.2,
            "item_item_minimum_spacing": 0.4
        },
        "bin_types": [
            {
                "type": "rectangle",
                "width": width,
                "height": height
            }
        ],
        "allow_mirroring": True,
        "item_types": item_types
    }

    return result  


def extract_vertices(data):
    simplified_items = []

    for bin in data.get("bins", []):
        for item in bin.get("items", []):
            shape = item["item_shapes"][0]["shape"]
            vertices = []

            # Para evitar repetição e garantir ordem, coletamos só o ponto inicial de cada segmento
            for segment in shape:
                point = (segment["xs"], segment["ys"])
                if point not in vertices:
                    vertices.append(point)
            # O último vértice pode ser o final do último segmento, se necessário
            last_segment = shape[-1]
            last_point = (last_segment["xe"], last_segment["ye"])
            if last_point not in vertices:
                vertices.append(last_point)

            simplified_items.append({
                "id": item["id"],
                "vertices": vertices
            })

    return simplified_items

def _shape_path(path_x, path_y, shape, is_hole=False):
    for element in (shape if not is_hole else reversed(shape)):
        t = element["type"]
        xs, ys, xe, ye = element["xs"], element["ys"], element["xe"], element["ye"]
        if t == "CircularArc":
            xc, yc = element["xc"], element["yc"]
            anticlockwise = 1 if element["anticlockwise"] else 0
            rc = math.hypot(xc - xs, yc - ys)

        if is_hole:
            xs, ys, xe, ye = xe, ye, xs, ys

        if not path_x or path_x[-1] is None:
            path_x.append(xs)
            path_y.append(ys)

        if t == "LineSegment":
            path_x.append(xe)
            path_y.append(ye)
        elif t == "CircularArc":
            start_angle = math.atan2(ys - yc, xs - xc)
            end_angle = math.atan2(ye - yc, xe - xc)

            if anticlockwise and end_angle <= start_angle:
                end_angle += 2 * math.pi
            if not anticlockwise and end_angle >= start_angle:
                end_angle -= 2 * math.pi

            t = np.linspace(start_angle, end_angle, 128)
            x = xc + rc * np.cos(t)
            y = yc + rc * np.sin(t)
            path_x.extend(x[1:])
            path_y.extend(y[1:])

    path_x.append(None)
    path_y.append(None)


def _extract_shapes(data):
    bins_x, bins_y = [], []
    defects_x, defects_y = [], []
    items_x, items_y = [], []

    for bin_data in data.get("bins", []):
        bin_x, bin_y = [], []
        defect_x, defect_y = [], []
        item_x, item_y = [], []

        _shape_path(bin_x, bin_y, bin_data["shape"])

        for defect in bin_data.get("defects", []):
            _shape_path(defect_x, defect_y, defect["shape"])
            for hole in defect.get("holes", []):
                _shape_path(defect_x, defect_y, hole, is_hole=True)

        for solution_item in bin_data.get("items", []):
            for item_shape in solution_item.get("item_shapes", []):
                _shape_path(item_x, item_y, item_shape["shape"])
                for hole in item_shape.get("holes", []):
                    _shape_path(item_x, item_y, hole, is_hole=True)

        bins_x.append(bin_x)
        bins_y.append(bin_y)
        defects_x.append(defect_x)
        defects_y.append(defect_y)
        items_x.append(item_x)
        items_y.append(item_y)

    return bins_x, bins_y, defects_x, defects_y, items_x, items_y


def plot_solution(
    data: Union[str, dict],
    show: bool = True,
    save_as: Optional[str] = None
) -> go.Figure:
    """
    Plots the solution from a JSON file path or dict.

    Args:
        data (str or dict): Path to JSON file or loaded JSON dictionary.
        show (bool): Whether to display the figure immediately (default: True).
        save_as (str): Optional path to save the figure as PNG (e.g., "output.png").

    Returns:
        plotly.graph_objects.Figure: The plotly figure.
    """
    if isinstance(data, str):
        with open(data, 'r') as f:
            data = json.load(f)

    bins_x, bins_y, defects_x, defects_y, items_x, items_y = _extract_shapes(data)
    num_bins = len(bins_x)

    fig = sp.make_subplots(
        rows=num_bins,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.005
    )

    for i in range(num_bins):
        fig.add_trace(go.Scatter(
            x=bins_x[i],
            y=bins_y[i],
            name="Bin",
            legendgroup="bins",
            showlegend=(i == 0),
            mode="lines",
            line=dict(color="black")
        ), row=i+1, col=1)

        fig.add_trace(go.Scatter(
            x=defects_x[i],
            y=defects_y[i],
            name="Defects",
            legendgroup="defects",
            showlegend=(i == 0),
            mode="lines",
            fill="toself",
            fillcolor="crimson",
            line=dict(color="black")
        ), row=i+1, col=1)

        fig.add_trace(go.Scatter(
            x=items_x[i],
            y=items_y[i],
            name="Items",
            legendgroup="items",
            showlegend=(i == 0),
            mode="lines",
            fill="toself",
            fillcolor="cornflowerblue",
            line=dict(color="black")
        ), row=i+1, col=1)

    fig.update_layout(
        autosize=True,
        height=max(500, num_bins * 800),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    if save_as:
        fig.write_image(save_as)
        print(f"[✓] Figura salva como: {save_as}")

    if show:
        fig.show()

    return fig


# if __name__ == "__main__":
#     notify = inotify.adapters.Inotify()
#     notify.add_watch("/data/")
    
#     run_packingsolver("/data/input.json", "/data/output.json")

    
#     for event in notify.event_gen(yield_nones=False):
#         (_, type_names, path, filename) = event
        
#         print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
#               path, filename, type_names))

#         if filename == "output.json" and type_names[0] == 'IN_CLOSE_WRITE':
#             print("ploting solution")
#             plot_solution("/data/output.json", save_as="/data/output.png")