from PIL import Image, ImageDraw
from collections import deque
import cv2


class Node:
    def __init__(self, x, y, direction, parent) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.neighbors = []
        self.parent = parent

    def __str__(self):
        parent = f"{self.parent.x},{self.parent.y}" if self.parent != None else None
        return (
            f"(Node {self.x},{self.y}), parent: ({parent}) direction: {self.direction}"
        )


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


directions = {"N": [0, -1], "S": [0, 1], "W": [-1, 0], "E": [1, 0]}


def move(pos: list, direction: list) -> None:
    return [x + y for x, y in zip(pos, direction)]


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


maze_image = cv2.imread("in/501x501.png", cv2.IMREAD_GRAYSCALE)


def create_graph():
    maze_graph = Graph()
    q = deque()
    visited = set()
    height, width = maze_image.shape

    for x in range(width):
        if maze_image[0, x] == 255:
            start = Node(x=x, y=0, direction=" ", parent=None)

        if maze_image[height - 1, x] == 255:
            end = Node(x=x, y=height - 1, direction=" ", parent=None)

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
            last_node = last_cross
            c_pos = [last_cross.x, last_cross.y]
        elif len(scn) == 1:  # Only one way to go
            if scn[0] != last_direction:  # If the path changes directions (corner)
                new_node = Node(
                    x=c_pos[0], y=c_pos[1], direction=scn[0], parent=last_node
                )
                maze_graph.add_node(new_node)
                maze_graph.add_edge(last_node, new_node)
                last_node = new_node
                last_direction = scn[0]
                c_pos = move([last_node.x, last_node.y], last_direction)
                visited.add(tuple(c_pos))
            else:
                c_pos = move(c_pos, scn[0])
                visited.add(tuple(c_pos))
        elif len(scn) > 1:  # Intersection
            new_node = Node(x=c_pos[0], y=c_pos[1], direction=scn[0], parent=last_node)
            maze_graph.add_node(new_node)
            maze_graph.add_edge(last_node, new_node)
            last_node = new_node
            visited.add(tuple(c_pos))
            q.append(last_node)
            last_direction = scn[0]
            c_pos = move([last_node.x, last_node.y], last_direction)
            if tuple(c_pos) not in visited:
                visited.add(tuple(c_pos))

    end.parent = last_node
    maze_graph.add_edge(last_node, end)
    print("Grafo gerado.")

    return maze_graph, visited, start, end


def bfs(start: Node, end: Node):
    visited = set()
    q = deque([start])

    while q:
        c_node = q.popleft()
        if c_node == end:
            path = []
            while c_node:
                path.insert(0, c_node)
                c_node = c_node.parent
            print("retornando path")
            return path

        visited.add(c_node)

        for neighbor in c_node.neighbors:
            if neighbor not in visited:
                q.append(neighbor)
                visited.add(neighbor)

    return visited


def paint_nodes(graph):
    image_pil = Image.fromarray(cv2.cvtColor(maze_image, cv2.COLOR_GRAY2RGB))
    draw = ImageDraw.Draw(image_pil)
    pixel_coordinates = [(n.x, n.y) for n in graph.nodes]
    pixel_color = (0, 255, 0)

    for coord in pixel_coordinates:
        draw.point(coord, fill=pixel_color)

    image_pil.save(f"out/nodes.png")


def paint_path(path: list):
    image_pil = Image.fromarray(cv2.cvtColor(maze_image, cv2.COLOR_GRAY2RGB))
    draw = ImageDraw.Draw(image_pil)
    edge_color = (255, 0, 0)

    for node in path:
        if not node.parent == None:
            x1 = node.x
            y1 = node.y
            x2 = node.parent.x
            y2 = node.parent.y
            draw.line([(x1, y1), (x2, y2)], fill=edge_color, width=1)
        else:
            draw.point((node.x, node.y), fill=edge_color)

    image_pil.save(f"out/path.png")


def main():
    graph, visited, start, end = create_graph()
    paint_nodes(graph)
    path = bfs(start, end)

    if path != None:
        paint_path(path)
    else:
        print("Deu ruim.")


if __name__ == "__main__":
    main()
