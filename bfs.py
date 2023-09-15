import networkx as nx

def bfs(maze_graph):
    visited = set()
    queue = []
    tree_edges = []

    for start_node in maze_graph.nodes():
        if start_node not in visited:
            queue.append(start_node)
            visited.add(start_node)

            while queue:
                current_node = queue.pop(0)
                for neighbor in maze_graph.neighbors(current_node):
                    if neighbor not in visited:
                        tree_edges.append((current_node, neighbor))
                        visited.add(neighbor)
                        queue.append(neighbor)
    
    return tree_edges

# Assuming you have created maze_graph as shown in previous code

# Call the BFS function
tree_edges = bfs(maze_graph)

# Print the tree edges found by BFS
for edge in tree_edges:
    print(f"Edge: {edge[0]} - {edge[1]}")
