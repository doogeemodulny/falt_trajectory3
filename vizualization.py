import matplotlib.pyplot as plt
import logging

from matrix_handler import MatrixHandler
from config import POINT_COLOR, AIR_BASE_COLOR, FORBIDDEN_LINE_COLOR, FORBIDDEN_ZONE_COLOR, INPUT_FILE

log = logging.getLogger('trajectory')


def draw_all(path, data):
    """Drowing the path"""

    _, ax = plt.subplots(figsize=(6, 6))
    draw_path(ax=ax, path=path)
    draw_environment(ax=ax, data=data, path=path)
    plt.show()
    log.info("нарисовали траекторию")


def draw_environment(ax, data, path):
    """Drawing points of the root, forbidden lines, zones, etc."""
    x = [data["data_points"][i]["x"] for i in path]  # x-координаты точек пути
    y = [data["data_points"][i]["y"] for i in path]  # y-координаты точек пути
    point_id = [str(data["data_points"][i]["id"]) for i in path]  # id точек пути
    for px, py, text in zip(x[1:-1], y[1:-1], point_id[1:-1]):  # рисуем и подписываем все точки
        logging.debug(f"{px, py, text}")
        ax.plot(px, py, POINT_COLOR)
        ax.annotate(text, (px, py))

    ax.plot(x[0], y[0], AIR_BASE_COLOR)  # помечаем АБ зеленой точкой

    forbidden_lines = [(x["id1"], x["id2"]) for x in data["forbidden_lines"]]
    for p1, p2 in forbidden_lines:  # каждый запрещенный ВК помечаем красным
        p1_coords = [(i["x"], i["y"]) for i in data["data_points"] if i["id"] == p1]
        p2_coords = [(i["x"], i["y"]) for i in data["data_points"] if i["id"] == p2]
        if len(p1_coords) > 0 and len(p2_coords) > 0:
            x, y = zip(p1_coords[0], p2_coords[0])
            ax.plot(x, y, FORBIDDEN_LINE_COLOR)

    forbidden_zones = [(z["x"], z["y"], z["r"]) for z in data["data_forbidden_zone"]]
    for zone in forbidden_zones:
        ax.add_patch(plt.Circle((zone[0], zone[1]), radius=zone[2], color=FORBIDDEN_ZONE_COLOR))


def draw_path(ax, path):
    """Drawing the trajectory"""
    handler = MatrixHandler()
    for i in range(1, len(path)):
        road_matrix = handler.get_roads_matrix(INPUT_FILE)[1:, 1:]
        road = road_matrix[path[i - 1], path[i]]
        road.draw(ax)
