import heapq
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Define the given initial and goal states
INITIAL_STATE = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

MOVES = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:  # Skip the blank tile
                goal_x, goal_y = [(row, col) for row in range(3) for col in range(3) if GOAL_STATE[row][col] == value][0]
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

def generate_new_state(state, move):
    x, y = find_blank(state)
    dx, dy = MOVES[move]
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < 3 and 0 <= new_y < 3:
        new_state = [row[:] for row in state]
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
        return new_state
    return None

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def is_solvable(state):
    flat_list = [num for row in state for num in row if num != 0]
    inversions = sum(1 for i in range(len(flat_list)) for j in range(i + 1, len(flat_list)) if flat_list[i] > flat_list[j])
    return inversions % 2 == 0

def print_state(state):
    for row in state:
        print(" ".join(map(str, row)))
    print()

def a_star_search(initial_state):
    if not is_solvable(initial_state):
        print("Given initial state is unsolvable!")
        return None, None
    
    print("Initial State:")
    print_state(initial_state)
    print(f"Initial heuristic (Manhattan distance): {manhattan_distance(initial_state)}")
    print("Starting A* search...\n")
    
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(initial_state), 0, initial_state, []))
    visited = set([state_to_tuple(initial_state)])  # Add initial state to visited
    parent_map = {}
    g_values = {state_to_tuple(initial_state): 0}
    f_values = {state_to_tuple(initial_state): manhattan_distance(initial_state)}
    
    steps = 0
    max_steps = 10000  # Prevent infinite loops
    
    while open_list and steps < max_steps:
        f_value, g_value, current_state, path = heapq.heappop(open_list)
        current_tuple = state_to_tuple(current_state)
        
        steps += 1
        
        if steps % 1000 == 0:
            print(f"Step {steps}, current f-value: {f_value}")
        
        # Check if we've reached the goal
        if current_state == GOAL_STATE:
            print(f"\nGoal reached in {g_value} moves!")
            solution_path = path + [current_state]
            return solution_path, parent_map
        
        # Generate all possible moves
        blank_x, blank_y = find_blank(current_state)
        
        for move_name, (dx, dy) in MOVES.items():
            new_x, new_y = blank_x + dx, blank_y + dy
            
            # Check if the move is valid
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = [row[:] for row in current_state]
                new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
                new_tuple = state_to_tuple(new_state)
                
                # Calculate the cost to reach this state
                new_g_value = g_value + 1
                
                # If we haven't visited this state or found a better path
                if new_tuple not in visited or new_g_value < g_values.get(new_tuple, float('inf')):
                    visited.add(new_tuple)
                    g_values[new_tuple] = new_g_value
                    h_value = manhattan_distance(new_state)
                    new_f_value = new_g_value + h_value
                    f_values[new_tuple] = new_f_value
                    
                    parent_map[new_tuple] = current_tuple
                    heapq.heappush(open_list, (new_f_value, new_g_value, new_state, path + [current_state]))
    
    print("\nFailed to find a solution within the step limit.")
    return None, None

def visualize_tree_with_path_highlighting(initial_state, solution_path, parent_map, max_depth=3):
    G = nx.DiGraph()
    pos = {}
    f_values = {}
    g_values = {}
    h_values = {}
    node_boxes = {}  # To store node box coordinates for background coloring
    
    # Convert solution_path to tuples for easier comparisons
    solution_path_tuples = [state_to_tuple(state) for state in solution_path]
    
    # Initialize with initial state
    initial_tuple = state_to_tuple(initial_state)
    G.add_node(initial_tuple)
    pos[initial_tuple] = (0, 5)  # Start at y=5 to leave room for the title
    h_values[initial_tuple] = manhattan_distance(initial_state)
    g_values[initial_tuple] = 0
    f_values[initial_tuple] = h_values[initial_tuple]
    
    # Build tree using BFS
    queue = [(initial_tuple, 0, 0)]  # (state, depth, x_position)
    y_offset = 5  # Starting y position to avoid title overlap
    
    while queue:
        state_tuple, depth, x_pos = queue.pop(0)
        if depth >= max_depth:
            continue
        
        # Get child states by reconstructing from parent_map
        children = []
        for child, parent in parent_map.items():
            if parent == state_tuple:
                children.append(child)
        
        # Skip if no children
        if not children:
            continue
        
        # Calculate positions for children
        num_children = len(children)
        step_size = max(1, 2 ** (max_depth - depth - 1))
        
        for i, child in enumerate(children):
            # Calculate position
            child_x = x_pos - ((num_children - 1) / 2) * step_size + i * step_size
            child_y = y_offset - (depth + 1) * 2  # Multiply by 2 to increase vertical spacing
            
            # Add to graph
            G.add_node(child)
            G.add_edge(state_tuple, child)
            pos[child] = (child_x, child_y)
            
            # Compute values
            child_list = [list(row) for row in child]
            g_values[child] = depth + 1
            h_values[child] = manhattan_distance(child_list)
            f_values[child] = g_values[child] + h_values[child]
            
            # Add to queue
            queue.append((child, depth + 1, child_x))
    
    # Create the figure with more vertical space
    plt.figure(figsize=(12, 10))
    
    # Draw the graph first without nodes to set up the figure layout
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, arrows=True)
    
    # Define edge colors based on path
    path_edges = []
    normal_edges = []
    
    for edge in G.edges():
        if edge[0] in solution_path_tuples and edge[1] in solution_path_tuples:
            if solution_path_tuples.index(edge[0]) == solution_path_tuples.index(edge[1]) - 1:
                path_edges.append(edge)
            else:
                normal_edges.append(edge)
        else:
            normal_edges.append(edge)
    
    # First draw colored rectangles behind the nodes
    for node in G.nodes():
        x, y = pos[node]
        rect_width = 1.2
        rect_height = 1.2
        
        if node == state_to_tuple(INITIAL_STATE):
            rect_color = 'lightgreen'
        elif node == state_to_tuple(GOAL_STATE):
            rect_color = 'pink'
        elif node in solution_path_tuples:
            rect_color = 'lightyellow'
        else:
            rect_color = 'lightgray'
        
        # Create the background rectangle
        rect = plt.Rectangle((x - rect_width/2, y - rect_height/2), rect_width, rect_height, 
                             facecolor=rect_color, edgecolor='black', zorder=0)
        plt.gca().add_patch(rect)
        node_boxes[node] = rect
    

    # Draw regular edges
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color='gray', width=1, arrows=True)

    # Draw path edges with a different color and width
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5, 
                        arrows=True, arrowstyle='-|>', arrowsize=20)

    # # Draw regular edges
    # nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color='gray', width=1, arrows=True, zorder=1)
    
    # # Draw path edges with a different color and width
    # nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5, 
    #                       arrows=True, arrowstyle='-|>', arrowsize=20, zorder=2)
    
    # Add state representation and f-values to nodes
    for node, (x, y) in pos.items():
        # Create a text representation of the 3x3 grid
        state_matrix = [[0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                state_matrix[i][j] = node[i][j]
        
        # Format the matrix string
        matrix_str = "\n".join([" ".join(map(str, row)).replace("0", " ") for row in state_matrix])
        
        # Add the state matrix as text
        plt.text(x, y, matrix_str, fontsize=8, ha='center', va='center', 
                color='black', zorder=10)
        
        # Add f, g, h values on top of the node
        f_text = f"f={f_values[node]}"
        g_text = f"g={g_values[node]}"
        h_text = f"h={h_values[node]}"
        plt.text(x, y+0.4, f_text, fontsize=8, ha='center', va='center', color='red', zorder=10)
        plt.text(x-0.4, y+0.4, g_text, fontsize=8, ha='left', va='center', color='blue', zorder=10)
        plt.text(x+0.4, y+0.4, h_text, fontsize=8, ha='right', va='center', color='green', zorder=10)
    
    # Add a legend with colored rectangles
    from matplotlib.patches import Patch
    
    
    # Add title with enough space above the graph
    plt.title("8-Puzzle A* Search Tree", fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)  # Adjust top margin to make room for title
    plt.show()

# Run the algorithm
try:
    solution_path, parent_map = a_star_search(INITIAL_STATE)
    
    if solution_path:
        print("Solution found!")
        print(f"Number of steps: {len(solution_path) - 1}")
        
        print("\nSolution Path:")
        for i, state in enumerate(solution_path):
            print(f"Step {i}:")
            print_state(state)
        
        # Show only the final tree visualization with improved path highlighting
        visualize_tree_with_path_highlighting(INITIAL_STATE, solution_path, parent_map, max_depth=3)
    else:
        print("No solution found.")
except Exception as e:
    print(f"An error occurred: {e}")