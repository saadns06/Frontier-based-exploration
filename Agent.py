import math

class FrontierAgent:
    def __init__(self, environment):
        self.environment = environment
        self.path = []

    def move_directly_to_frontier(self, frontier):
        if self.environment.move_agent(frontier):
            self.path.append(frontier)
            return True
        return False

    def choose_closest_frontier(self, use_manhattan=True):
        """
        Select the closest frontier. Optionally use Manhattan distance for efficiency.
        """
        frontiers = self.environment.get_frontiers()
        print(f"Detected frontiers (excluding fire zones): {frontiers}")

        if not frontiers:
            return None

        agent_x, agent_y = self.environment.agent_position
        closest_frontier = None
        min_distance = float('inf')

        for frontier in frontiers:
            fx, fy = frontier

            # Calculate distance (Manhattan or Euclidean based on the flag)
            if use_manhattan:
                distance = abs(fx - agent_x) + abs(fy - agent_y)
            else:
                distance = math.sqrt((fx - agent_x) ** 2 + (fy - agent_y) ** 2)

            # Prioritize unexplored cells (0) over partially explored (1)
            if self.environment.grid[fx, fy] == 0:
                distance -= 1  # Give a small priority bonus

            if distance < min_distance:
                min_distance = distance
                closest_frontier = frontier

        print(f"Chosen frontier: {closest_frontier}, distance: {min_distance}")
        return closest_frontier
