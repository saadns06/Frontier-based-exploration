from Environment import FrontierEnvironment
from Agent import FrontierAgent
from RewardSystem import RewardSystem

def main():
    fire_zones = [(2, 2), (3, 3), (1, 4)]
    env = FrontierEnvironment(5, 5, fire_zones)
    agent = FrontierAgent(env)
    rewards = RewardSystem(env)

    print("Starting frontier-based exploration:")

    step_limit = 100
    visited_positions = set()
    steps_taken = 0
    total_reward = 0
    max_distance = 0

    while not env.is_covered() and steps_taken < step_limit:
        frontier = agent.choose_closest_frontier()

        if frontier:
            agent.move_directly_to_frontier(frontier)
            reward = rewards.calculate_reward(agent)
            total_reward += reward

            current_position = agent.environment.agent_position
            visited_positions.add(current_position)

            print(f"Agent moved to {current_position}, reward: {reward}, total reward: {total_reward}")

            # Check if the agent is stuck by revisiting the same position frequently
            if len(visited_positions) < steps_taken / 2:
                print("Agent is getting stuck, stopping exploration.")
                break

            # Calculate the distance from the starting position (0, 0)
            x, y = current_position
            distance = abs(x - 0) + abs(y - 0)
            max_distance = max(max_distance, distance)
        else:
            print("No frontiers available!")
            break

        steps_taken += 1
        env.display_grid()

    if steps_taken >= step_limit:
        print("Step limit reached, stopping exploration.")

    print("Exploration complete!")
    print(f"Total steps taken: {steps_taken}")
    print(f"Total reward collected: {total_reward}")
    print(f"Maximum distance traveled from start: {max_distance}")

if __name__ == "__main__":
    main()
