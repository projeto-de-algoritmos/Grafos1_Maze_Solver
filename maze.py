from PIL import Image, ImageDraw
from collections import deque
import cv2


class Node:
    def __init__(self, x, y, direction) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.neighbors = []


class Graph:
    def __init__(self) -> None:
        self.nodes = []

    def add_node(self, node: Node) -> Node:
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Both nodes must be in the graph.")

        node1.neighbors.append(node2)
        node2.neighbors.append(node1)

    def __str__(self):
        result = ""
        for node in self.nodes:
            neighbors = ", ".join(
                f"({neighbor.x},{neighbor.y})" for neighbor in node.neighbors
            )
            result += f"({node.x},{node.y},{node.direction}) -> [{neighbors}]\n"
        return result


def move(pos: list, direction: str) -> None:
    x, y = pos
    if direction == "N":
        y -= 1
    if direction == "S":
        y += 1
    if direction == "W":
        x -= 1
    if direction == "E":
        x += 1

    return [x, y]


def paint_nodes(graph):
    image_pil = Image.fromarray(cv2.cvtColor(maze_image, cv2.COLOR_GRAY2RGB))
    draw = ImageDraw.Draw(image_pil)
    pixel_coordinates = [(n.x, n.y) for n in graph.nodes]
    pixel_color = (0, 255, 0)

    for coord in pixel_coordinates:
        draw.point(coord, fill=pixel_color)

    image_pil.save(f"out/nodes.png")


def paint_path(visited):
    image_pil = Image.fromarray(cv2.cvtColor(maze_image, cv2.COLOR_GRAY2RGB))
    draw = ImageDraw.Draw(image_pil)
    pixel_coordinates = [n for n in visited]
    pixel_color = (255, 0, 0)

    for coord in pixel_coordinates:
        draw.point(coord, fill=pixel_color)

    image_pil.save(f"out/path.png")


def is_path(pos: list):
    return True if maze_image[pos[1], pos[0]] == 255 else False


def scan(pos: list, visited: str):
    directions = ["S", "W", "E", "N"]
    available = []

    for d in directions:
        m = move(pos, d)
        if is_path(m) and tuple(m) not in visited:
            available.append(d)
    return available


maze_image = cv2.imread("in/41x41.png", cv2.IMREAD_GRAYSCALE)


def create_graph():
    maze_graph = Graph()
    q = deque()
    visited = set()
    height, width = maze_image.shape

    for x in range(width):
        if maze_image[0, x] == 255:
            start = Node(x=x, y=0, direction=" ")

        if maze_image[height - 1, x] == 255:
            end = Node(x=x, y=height - 1, direction=" ")

    maze_graph.add_node(start)
    maze_graph.add_node(end)

    print(f"start = ({start.x},{start.y}), end = ({end.x},{end.y})\n")

    c_pos = [start.x, start.y]
    end_pos = [end.x, end.y]
    visited.add(tuple(c_pos))
    last_direction = "S"
    last_node = start

    while c_pos != end_pos:
        scn = scan(c_pos, visited)
        if not len(scn):  # dead-end
            last_cross = q.popleft()
            c_pos = last_cross
        if len(scn) == 1:  # Only one way to go
            if scn[0] != last_direction:  # If the path changes directions (corner)
                new_node = Node(x=c_pos[0], y=c_pos[1], direction=scn[0])
                maze_graph.add_node(new_node)
                maze_graph.add_edge(last_node, new_node)
                last_node = new_node
                last_direction = scn[0]
                c_pos = move([last_node.x, last_node.y], last_direction)
                visited.add(tuple(c_pos))
            else:
                c_pos = move(c_pos, scn[0])
                visited.add(tuple(c_pos))
        if len(scn) > 1:  # Intersection
            new_node = Node(x=c_pos[0], y=c_pos[1], direction=scn[0])
            maze_graph.add_node(new_node)
            maze_graph.add_edge(last_node, new_node)
            last_node = new_node
            visited.add(tuple(c_pos))
            q.append([last_node.x, last_node.y])
            last_direction = scn[0]
            c_pos = move([last_node.x, last_node.y], last_direction)
            if tuple(c_pos) not in visited:
                visited.add(tuple(c_pos))
    print("Grafo gerado.")

    return maze_graph, visited


def main():
    graph, visited = create_graph()
    paint_path(visited)
    paint_nodes(graph)


if __name__ == "__main__":
    main()
