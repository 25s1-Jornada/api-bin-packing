import docker
from docker.errors import DockerException
import json
import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
from typing import Union, Optional
import os
import inotify.adapters

client = docker.from_env()

def run_packingsolver(input_path: str, output_path: str):
    try:
        # Nome do container que já está rodando
        container = client.containers.get("api-bin-packing-packingsolver-1")  # <- Nome do container em execução
        
        # Executa o comando dentro do container rodando
        # To rodando detach pq por algum motivo o packingsolver não finaliza a execução
        exec_result = container.exec_run(
            cmd=f"packingsolver_irregular -i {input_path} -c {output_path} --time-limit 10",
            #detach=True
        )
        
        print(exec_result.output.decode('utf-8'))
        
    except DockerException as e:
        print("Erro:", e)

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


if __name__ == "__main__":
    notify = inotify.adapters.Inotify()
    notify.add_watch("/data/")
    
    run_packingsolver("/data/input.json", "/data/output.json")

    
    for event in notify.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        
        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              path, filename, type_names))

        if filename == "output.json" and type_names[0] == 'IN_CLOSE_WRITE':
            print("ploting solution")
            plot_solution("/data/output.json", save_as="/data/output.png")

