import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# BFS to find shortest path by hops (not weight)
def bfs_shortest_path(G, start, target):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    level_map = {start: 0}  # Track the level of each node

    while queue:
        current = queue.popleft()
        current_level = level_map[current]
        
        # If we reached the target, reconstruct the path
        if current == target:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], level_map  # Return path in reverse order (start to target)
        
        # Explore neighbors
        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                level_map[neighbor] = current_level + 1  # Assign level to neighbor
                queue.append(neighbor)

    return [], level_map  # Return empty path and level map if no path found

# Map node numbers to IPs
ip_addresses = {
    1: "192.168.1.1",  # A
    2: "192.168.1.2",  # B
    3: "192.168.1.3",  # C
    4: "192.168.1.4",  # D
    5: "192.168.1.5",  # E
    6: "192.168.1.6",  # F
    7: "192.168.1.7",  # G
    8: "192.168.1.8",  # H
}

# Letter-to-number and number-to-letter mappings
letter_to_node = {chr(64 + n): n for n in ip_addresses.keys()}  # A->1, B->2, ...
node_to_letter = {v: k for k, v in letter_to_node.items()}

# Create binary tree as an undirected graph
G = nx.Graph()
for node, ip in ip_addresses.items():
    G.add_node(node, ip=ip)

# Define binary tree edges based on your structure
G.add_edges_from([
    (1, 2),  # A - B
    (1, 3),  # A - C
    (2, 4),  # B - D
    (2, 5),  # B - E
    (3, 6),  # C - F
    (3, 7),  # C - G
    (4, 8),  # D - H
])

# Get user input for start and end nodes
start_letter = input("Enter start node (A-H): ").strip().upper()
target_letter = input("Enter target node (A-H): ").strip().upper()

# Convert to numeric node IDs
start = letter_to_node.get(start_letter)
target = letter_to_node.get(target_letter)

if start is None or target is None:
    print("Invalid input. Please enter letters A-H.")
    exit()

# Run BFS to find the shortest path
path, level_map = bfs_shortest_path(G, start, target)
if path:
    path_letters = [node_to_letter[n] for n in path]
    print(f"Shortest path from {start_letter} to {target_letter} (by hops): {path_letters}")
else:
    print("No path found.")

# Draw the graph
# Manually set node positions for the new binary tree layout
pos = {
    1: (0, 3),    # A
    2: (-1, 2),   # B
    3: (1, 2),    # C
    4: (-1.5, 1), # D
    5: (-0.5, 1), # E
    6: (0.5, 1),  # F
    7: (1.5, 1),  # G
    8: (-1.5, 0), # H
}

# Draw the graph
fig, ax = plt.subplots(figsize=(10, 8))
nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=2000, ax=ax)

# Show node labels: A, B, C... and IPs
alphabet_labels = {node: node_to_letter[node] for node in G.nodes()}
ip_labels = nx.get_node_attributes(G, "ip")
ip_label_pos = {node: (x + 0.1, y) for node, (x, y) in pos.items()}

# Draw alphabet and IP labels
nx.draw_networkx_labels(G, pos, labels=alphabet_labels, font_color="black", font_size=12)
nx.draw_networkx_labels(G, ip_label_pos, labels=ip_labels, font_color="red", font_size=8)

# Highlight the path
if path:
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='yellow', ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='orange', width=2, ax=ax)

# Draw dotted edges for nodes at the same level
for level in set(level_map.values()):
    level_nodes = [node for node, lvl in level_map.items() if lvl == level]
    if len(level_nodes) > 1:  # Only draw dotted lines if more than one node at the level
        level_edges = [(level_nodes[i], level_nodes[i+1]) for i in range(len(level_nodes)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=level_edges, edge_color='darkgray', style='dotted', width=2, ax=ax)

        # Add label for the explored level
        level_pos = (sum(pos[node][0] for node in level_nodes) / len(level_nodes), 
                     sum(pos[node][1] for node in level_nodes) / len(level_nodes))
        plt.text(level_pos[0], level_pos[1], f"Explored Level {level}", fontsize=10, color='black', ha='center')

# Set the title and axis properties
plt.title(f"Shortest Path from {start_letter} to {target_letter} (Binary Tree BFS)", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
