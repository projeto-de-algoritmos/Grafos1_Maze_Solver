from maze import Graph, Node, Navigator
from PIL import Image, ImageDraw
from collections import deque
import cv2
import sys


if len(sys.argv) == 2:
    img_name = sys.argv[1]
    maze_image = cv2.imread(f"../in/{img_name}.png", cv2.IMREAD_GRAYSCALE)
else:
    maze_image = cv2.imread(f"../in/41.png", cv2.IMREAD_GRAYSCALE)


def create_graph():
    height, width = maze_image.shape

    for x in range(width):
        if maze_image[0, x] == 255:
            start = Node(x=x, y=0, direction="S", parent=None)

        if maze_image[height - 1, x] == 255:
            end = Node(x=x, y=height - 1, direction=" ", parent=None)

    print(f"start = ({start.x},{start.y}), end = ({end.x},{end.y})\n")

    maze_graph = Graph(start, end)
    nav = Navigator(maze_graph, maze_image)
    stack = deque()

    while nav.c_pos != nav.end_pos:
        paths = nav.scan()
        
        if not len(paths):                          # Dead-end
            nav.backtrack(stack.popleft())
        elif len(paths) == 1:                     
            if paths[0] != nav.last_direction:      # Corner
                nav.new_node(paths)
            else:                                   # Corridor
                nav.visit(paths)
        elif len(paths) > 1:                        # Intersection
            nav.new_node(paths)
            stack.appendleft(nav.last_node)

    end.parent = nav.last_node
    maze_graph.add_edge(nav.last_node, end)
    print("Grafo gerado.")

    return maze_graph, start, end


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

def test(end):
    c_node = end
    path = []
    while c_node:
        path.insert(0, c_node)
        c_node = c_node.parent
    print("retornando path")
    return path


def paint_nodes(graph):
    image_pil = Image.fromarray(cv2.cvtColor(maze_image, cv2.COLOR_GRAY2RGB))
    draw = ImageDraw.Draw(image_pil)
    pixel_coordinates = [(n.x, n.y) for n in graph.nodes]
    pixel_color = (0, 0, 255)

    for coord in pixel_coordinates:
        draw.point(coord, fill=pixel_color)

    image_pil.save(f"../out/nodes.png")


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

    image_pil.save(f"../out/path.png")


def main():
    graph, start, end = create_graph()
    paint_nodes(graph)
    path = bfs(start, end)
    #path = test(end)

    if path != None:
        paint_path(path)
    else:
        print("Deu ruim.")


if __name__ == "__main__":
    main()
