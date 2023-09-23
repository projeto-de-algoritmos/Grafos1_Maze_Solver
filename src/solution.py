from maze import Graph, Node, Navigator
from PIL import Image, ImageDraw
from collections import deque
from math import ceil
import cv2


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

        if not len(paths):  # Dead-end
            nav.backtrack(stack.popleft())
        elif len(paths) == 1:
            if paths[0] != nav.last_direction:  # Corner
                nav.new_node(paths)
            else:  # Corridor
                nav.visit(paths)
        elif len(paths) > 1:  # Intersection
            nav.new_node(paths)
            stack.appendleft(nav.last_node)

    end.parent = nav.last_node
    maze_graph.add_edge(nav.last_node, end)
    print("Grafo gerado.")

    return maze_graph, end


def find_path(end):
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


def resize_image(img: Image):
    width, height = img.size
    aspect_ratio = width / height
    target_width = 1000

    if width < target_width or height < target_width:
        new_width = width * ceil(target_width/width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = height
        new_width = width

    img = img.resize((new_width, new_height), resample=Image.NEAREST)

    return img


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

    image_pil = resize_image(image_pil)
    image_pil.save(f"../out/path.png")


def solve(img):
    global maze_image
    maze_image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    graph, end = create_graph()
    paint_nodes(graph)
    path = find_path(end)

    if path != None:
        paint_path(path)
        solved_image = cv2.imread("../out/path.png")
        return solved_image
    else:
        print("Deu ruim.")
        return None