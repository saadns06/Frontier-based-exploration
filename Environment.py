import numpy as np

class FrontierEnvironment:
    def __init__(self, width, height, fire_zones=None):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height))
        self.fire_zones = fire_zones if fire_zones else []

        for zone in self.fire_zones:
            x, y = zone
            self.grid[x, y] = -1  # Fire zones marked as -1

        self.agent_position = (0, 0)
        self.grid[0, 0] = 1  # Starting position marked as explored

    def move_agent(self, new_position):
        x, y = new_position
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.grid[x, y] != -1:  # Avoid fire zones
                self.agent_position = new_position
                if self.grid[x, y] == 0:
                    self.grid[x, y] = 1  # Mark as explored
                elif self.grid[x, y] == 1:
                    self.grid[x, y] = 2  # Mark as fully explored
                return True
            else:
                print(f"Move failed: Position {new_position} is a fire zone.")
        else:
            print(f"Move failed: Position {new_position} is out of bounds.")
        return False

    def get_frontiers(self):

        frontiers = set()
        visited = set()

        # Check around all currently explored cells
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] >= 1:  # Explored or fully explored cell
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            # Add to frontiers if unexplored and not a fire zone
                            if self.grid[nx, ny] == 0 and (nx, ny) not in visited:
                                frontiers.add((nx, ny))
                            visited.add((nx, ny))

        return list(frontiers)

    def is_covered(self):

        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] == 0:  # Unexplored cell
                    return False
        return True

    def display_grid(self):
        """
        Display the grid with better visualization:
        - '0' for unexplored
        - '1' for explored
        - '2' for fully explored
        - '-1' for fire zones
        """
        display = self.grid.copy()
        print("Grid State:")
        print(display)
