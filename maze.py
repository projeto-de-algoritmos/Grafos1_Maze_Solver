import cv2
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    x : int
    y : int
    parent : str
    neighbors: list

    def __init__(self, x, y, parent) -> None:
        self.x = x
        self.y = y
        self.parent = parent
    

def read_image():
    maze_image = cv2.imread('maze.png', cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(maze_image, 128, 255, cv2.THRESH_BINARY)
    return binary_image

def create_graph():
    binary_image = read_image()
    maze_graph = list()
    height, width = binary_image.shape

    for x in range(width):
        if binary_image[0, x] == 255:
            start = Node(x=x, y=0, parent='N')

        if binary_image[height-1, x] == 255:
            end = Node(x=x, y=height-1, parent='N')

    maze_graph.append(start)    
    maze_graph.append(end)

    print(f'start = {start.x}, end = {end.x}')

    c_pos = start
    # c_pos = start

    # north = (-1,0)
    # east = (0,-1)
    # west = (0,1)
    # south = (1,0)

    # c_pos = tuple(map(lambda a: sum(a), zip(c_pos, south)))
    # y, x = c_pos
    # print(height-y, x)
    # if binary_image[y, x] == 255:
    #     maze_graph.add_node('second', pos=(x, height-y))
    #     print("entrei")


create_graph()
# while c_pos != end:
    

# for y in range(height):
#     for x in range(width):
#         if binary_image[y, x] == 255:  # Paths are white pixels (255)
#             maze_graph.add_node((x, y))
#             for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < width and 0 <= ny < height and binary_image[ny, nx] == 0:
#                     maze_graph.add_edge((x, y), (nx, ny))

#pos = {node: node for node in maze_graph.nodes()}
#pos = {node:(x, y) for (node, (x,y)) in nx.get_node_attributes(maze_graph, 'pos').items()}
# pos = nx.get_node_attributes(maze_graph, 'pos')
# #pos = {node: (y, x) for node, (x, y) in pos.items()}

# nx.draw(maze_graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10)
# # nx.draw(maze_graph, pos, with_labels=False, node_size=10)
# plt.show()