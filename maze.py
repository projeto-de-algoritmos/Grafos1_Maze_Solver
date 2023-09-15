import cv2


class Node:
    def __init__(self, x, y, parent) -> None:
        self.x = x
        self.y = y
        self.parent = parent
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
            result += f"({node.x},{node.y}) -> [{neighbors}]\n"
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

    return [x,y]

def find_dir(parent) -> str:
        if parent == "N":
            return "S"
        if parent == "S":
            return "N"
        if parent == "E":
            return "W"
        if parent == "W":
            return "E"


def is_path(pos: list):
    return True if maze_image[pos[1], pos[0]] == 255 else False


def scan(pos: list, back: str):
    directions = ["N", "S", "W", "E"]
    directions.remove(back)
    available = []

    for d in directions:
        if is_path(move(pos, d)):
            available.append(d)

    return available


maze_image = cv2.imread("maze.png", cv2.IMREAD_GRAYSCALE)

def create_node(maze_graph, c_pos, last_node, last_direction, scn, corner):
    c_pos = move([last_node.x, last_node.y], scn[0])
    new_node = Node(x=c_pos[0], y=c_pos[1], parent=find_dir(last_direction)  if corner else last_direction)
    maze_graph.add_node(new_node)
    maze_graph.add_edge(last_node, new_node)
    last_node = new_node
    c_pos = [last_node.x, last_node.y]

def create_graph():
    maze_graph = Graph()
    height, width = maze_image.shape

    for x in range(width):
        if maze_image[0, x] == 255:
            start = Node(x=x, y=0, parent="N")

        if maze_image[height - 1, x] == 255:
            end = Node(x=x, y=height - 1, parent="N")

    maze_graph.add_node(start)
    maze_graph.add_node(end)

    print(f"start = ({start.x},{start.y}), end = ({end.x},{end.y})\n")

    c_pos = [start.x, start.y]
    last_direction = "N"
    last_node = start

    i = 0
    while i < 4:
        scn = scan(c_pos, last_direction)
        if len(scn) == 1:
            if scn != find_dir(last_direction): # If the path changes directions (corner)
                create_node(maze_graph, c_pos, last_node, last_direction, scn, corner=True)
            else:
                c_pos = move(c_pos, scn)
        i += 1


# add new node
    # c_pos = move([last_node.x, last_node.y], scn[0])
    # new_node = Node(x=c_pos[0], y=c_pos[1], parent=last_direction)
    # maze_graph.add_node(new_node)
    # maze_graph.add_edge(last_node, new_node)
    # last_node = new_node
    # c_pos = [last_node.x, last_node.y]

    # elif len(scn) > 2:
    #     new_node = Node(x=c_pos[0], y=c_pos[1], parent=direc.find(last_direction))
    #     maze_graph.add_node(new_node)
    #     maze_graph.add_edge(last_node, new_node)
    #     last_node = new_node

    print(maze_graph)


create_graph()
