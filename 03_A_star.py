import networkx as nx
import matplotlib.pyplot as plt
import heapq

def a_star(graph, start, goal, heuristic):
    open_set = []  # Priority queue
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic[start]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            total_cost = 0
            while current in came_from:
                path.append(current)
                total_cost += graph[came_from[current]][current]
                current = came_from[current]

            path.append(start)
            path.reverse()
            print("Minimum Distance:", total_cost)
            return path

        for neighbor, cost in graph[current].items():
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

# Define the graph as an adjacency list with costs
graph = {
    'S': {'B': 4, 'C': 3},
    'B': {'F': 5, 'E': 12},
    'C': {'E': 10, 'D': 7},
    'D': {'E': 2},
    'E': {'G': 5},
    'F': {'G': 6},
    'G': {}
}

# Heuristic values
heuristic = {
    'S': 14, 'B': 12, 'C': 11, 'D': 6,
    'E': 4, 'F': 11, 'G': 0
}

# Get start and goal nodes from user input
start = input("Enter the start node: ").strip()
goal = input("Enter the goal node: ").strip()

# Ensure that the start and goal nodes exist in the graph
if start not in graph or goal not in graph:
    print("Invalid start or goal node. Please enter nodes that exist in the graph.")
else:
    # Run A*
    path = a_star(graph, start, goal, heuristic)
    print("A* Path:", path)

    # Visualization
    def draw_graph(graph, path):
        G = nx.DiGraph()

        # Add edges with weights
        for node in graph:
            for neighbor, weight in graph[node].items():
                G.add_edge(node, neighbor, weight=weight)

        # Custom positions for nodes
        pos = {
            'S': (0, 2),
            'B': (1, 3),
            'C': (1, 1),
            'D': (2, 0),
            'E': (2, 2),
            'F': (3, 3),
            'G': (4, 2)
        }

        plt.figure(figsize=(10, 7))

        # Node colors: highlight path
        node_colors = ['pink' if node in path else '#A0CBE2' for node in G.nodes()]

        # Edge colors: highlight path edges
        edge_colors = ['pink' if (u, v) in zip(path, path[1:]) else '#A9A9A9' for u, v in G.edges()]

        # Draw nodes and edges
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3000, alpha=0.9)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2.5, alpha=0.8)

        # Node labels
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

        # Edge weight labels
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_weight='bold')

        plt.axis('off')
        plt.show()

    # Visualize the graph
    if path:
        draw_graph(graph, path)
    else:
        print("No path found to visualize.")
