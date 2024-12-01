class RewardSystem:
    def __init__(self, environment):
        self.environment = environment
        self.revisit_count = {}  # Track revisit counts for dynamic penalty

    def calculate_reward(self, agent):
        exploration_reward = self.exploration_reward(agent)
        revisit_penalty = self.dynamic_revisit_penalty(agent)
        distance_bonus = self.distance_bonus(agent)
        danger_zone_penalty = self.danger_zone_penalty(agent)

        # Calculate the total reward
        total_reward = exploration_reward + revisit_penalty + distance_bonus + danger_zone_penalty

        # Enhanced debug output
        x, y = agent.environment.agent_position
        cell_value = self.environment.grid[x, y]
        print(f"Agent at position ({x}, {y}), cell value: {cell_value}, "
              f"exploration reward: {exploration_reward}, "
              f"revisit penalty: {revisit_penalty}, "
              f"distance bonus: {distance_bonus}, "
              f"danger zone penalty: {danger_zone_penalty}, "
              f"total reward: {total_reward}")

        return total_reward

    def exploration_reward(self, agent):
        x, y = agent.environment.agent_position

        if self.environment.grid[x, y] == 0:
            self.environment.grid[x, y] = 1
            return 15

        elif self.environment.grid[x, y] == 1:
            self.environment.grid[x, y] = 2
            return 8

        return 0

    def dynamic_revisit_penalty(self, agent):
        x, y = agent.environment.agent_position
        position = (x, y)

        # Track the number of revisits
        if position not in self.revisit_count:
            self.revisit_count[position] = 0
        self.revisit_count[position] += 1

        # Dynamic penalty based on the number of times the cell is revisited
        penalty = -2 * self.revisit_count[position]
        return penalty

    def distance_bonus(self, agent):
        """
        Calculate a small bonus based on the distance from the starting position (0, 0).
        This encourages the agent to explore farther away.
        """
        x, y = agent.environment.agent_position
        distance = abs(x - 0) + abs(y - 0)  # Manhattan distance
        bonus = 0.5 * distance  # Small bonus based on the distance
        return bonus

    def danger_zone_penalty(self, agent):
        """
        Apply a high penalty if the agent enters a fire zone (-1).
        """
        x, y = agent.environment.agent_position

        # Check if the current position is a fire zone
        if self.environment.grid[x, y] == -1:
            print("Agent entered a fire zone! High penalty applied.")
            return -100  # High penalty for entering a dangerous area
        return 0



