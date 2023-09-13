import cv2
import networkx as nwx
import matplotlib.pyplot as plt

maze_image = cv2.imread('20x20.png', cv2.IMREAD_GRAYSCALE)
_, binary_image = cv2.threshold(maze_image, 128, 255, cv2.THRESH_BINARY_INV)

maze_graph = nwx.Graph()
height, width = binary_image.shape

for y in range(height):
    for x in range(width):
        if binary_image[y, x] == 255:  # Paths are white pixels (255)
            maze_graph.add_node((x, y))
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and binary_image[ny, nx] == 0:
                    maze_graph.add_edge((x, y), (nx, ny))

pos = {node: (node[0], height - node[1]) for node in maze_graph.nodes()}

nwx.draw(maze_graph, pos, with_labels=False, node_size=2)
plt.show()