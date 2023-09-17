class Node:
    def __init__(self, x: int, y: int, direction: str, parent) -> None:
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
    def __init__(self, start_node: Node, end_node: Node) -> None:
        self.nodes = [start_node, end_node]

    def add_node(self, node: Node) -> Node:
        self.nodes.append(node)
        return node

    def add_edge(self, node1: Node, node2: Node) -> None:
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


class Navigator:
    directions = {"N": [0, -1], "S": [0, 1], "W": [-1, 0], "E": [1, 0]}

    def __init__(self, maze_graph: Graph, maze_image) -> None:
        self.maze_graph = maze_graph
        self.maze_image = maze_image
        self.last_node = maze_graph.nodes[0]
        self.last_direction = "S"
        self.c_pos = [maze_graph.nodes[0].x, maze_graph.nodes[0].y]
        self.end_pos = [maze_graph.nodes[1].x, maze_graph.nodes[1].y]
        self.visited = set(tuple(self.c_pos))

    def is_path(self, pos: list):
        return True if self.maze_image[pos[1], pos[0]] == 255 else False

    def backtrack(self, last_cross: Node):
        self.last_node = last_cross
        self.c_pos = [last_cross.x, last_cross.y]

    def move(self, direction: str) -> None:
        return [x + y for x, y in zip(self.c_pos, self.directions[direction])]

    def scan(self):
        directions = ["S", "W", "E", "N"]
        available = []

        for d in directions:
            m = self.move(d)
            if self.is_path(m) and tuple(m) not in self.visited:
                available.append(d)
        return available

    def visit(self, directions: list) -> None:
        self.c_pos = self.move(directions[0])
        self.visited.add(tuple(self.c_pos))

    def new_node(self, scn: list) -> None:
        x, y = self.c_pos[0], self.c_pos[1]
        direction = scn[0]

        new_node = Node(x=x, y=y, direction=direction, parent=self.last_node)
        self.maze_graph.add_node(new_node)
        self.maze_graph.add_edge(self.last_node, new_node)

        self.last_node, self.last_direction = new_node, direction
        self.visit(direction)
