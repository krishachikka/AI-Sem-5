import time

# Step 1: Define the Tower of Hanoi Problem Formulation
class TowerOfHanoi:
    def __init__(self, n):
        self.n = n
        # Initial state with all disks on Rod 1
        self.rods = {
            'Rod 1': list(range(n, 0, -1)),  # Rod 1 has disks in descending order
            'Rod 2': [],
            'Rod 3': []
        }

    # Step 2: Define the goal state
    def goal_state(self):
        # Goal state is when all disks are moved to Rod 3
        return {
            'Rod 1': [],
            'Rod 2': [],
            'Rod 3': list(range(self.n, 0, -1))  # All disks in descending order on Rod 3
        }

    # Step 3: Define actions (legal moves)
    def legal_move(self, source, destination):
        if not self.rods[source]:
            return False  # Can't move if the source rod is empty
        if not self.rods[destination]:
            return True  # Always can move to an empty rod
        # A disk can only be moved to a rod if it's smaller than the top disk on that rod
        return self.rods[source][-1] < self.rods[destination][-1]

    # Step 4: Perform a move from source to destination rod
    def move_disk(self, source, destination):
        if self.legal_move(source, destination):
            disk = self.rods[source].pop()  # Pop the top disk from the source rod
            self.rods[destination].append(disk)  # Push it to the destination rod
            print(f"Move disk {disk} from {source} to {destination}")
            self.display_state()
            time.sleep(1)  # Simulate delay for visualization effect
        else:
            print(f"Illegal move: Can't move disk from {source} to {destination}")

    # Step 5: Solve the Tower of Hanoi problem recursively
    def tower_of_hanoi(self, n, source, auxiliary, destination):
        if n == 1:
            # Base case: Only one disk to move
            self.move_disk(source, destination)
            return
        # Move the top n-1 disks from source to auxiliary using destination as auxiliary
        self.tower_of_hanoi(n - 1, source, destination, auxiliary)
        # Move the nth disk from source to destination
        self.move_disk(source, destination)
        # Move the n-1 disks from auxiliary to destination using source as auxiliary
        self.tower_of_hanoi(n - 1, auxiliary, source, destination)

    # Step 6: Display the current state of the rods
    def display_state(self):
        print("\nCurrent state of the rods:")
        for rod, disks in self.rods.items():
            print(f"{rod}: {disks}")
        print("\n")

# Problem Formulation:
n = 3  # Number of disks
problem = TowerOfHanoi(n)

# Step 1: Initial state
print("Initial state:")
problem.display_state()

# Step 2: Goal state
print("\nGoal state:")
print(problem.goal_state())

# Step 3: Start solving the Tower of Hanoi problem
print("\nSolution steps:")
problem.tower_of_hanoi(n, 'Rod 1', 'Rod 2', 'Rod 3')

# Step 4: Final state (after solution)
print("\nFinal state:")
problem.display_state()
