import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
import pygame


MAZE = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
], dtype=np.int8)

START_POS = (1, 1)
GOAL_POS = (8, 8)

# action -> (drow, dcol), matching the README order: up, right, down, left
ACTIONS = {
    0: (-1, 0),  # up
    1: (0, 1),   # right
    2: (1, 0),   # down
    3: (0, -1),  # left
}


class MazeEnv(gym.Env):

    def __init__(self, max_steps=200):
        self.action_space = spaces.Discrete(4)
        """
        - Using np.int8 for observations can cause training instability. Neural networks expect float inputs. Try np.float32 and normalize values to [0, 1] instead of raw 0-3.
        - Add a max_steps parameter to prevent episodes from running forever.
        """
        # self.observation_space = spaces.Box(0, 3, (1, 10, 10), dtype=np.int8)
        self.observation_space = spaces.Box(0, 1, (1, 10, 10), dtype=np.float32)
        # TODO
        # self._max_steps = max_steps
        # self._steps = 0
        # self._maze = None
        # self.start_pos = None
        # self.goal_pos = None
        # self.agent_pos = self.start_pos
        self._max_steps = max_steps
        self._steps = 0
        self._maze = MAZE
        self.start_pos = START_POS
        self.goal_pos = GOAL_POS
        self.agent_pos = self.start_pos
        self._visited = set()

    def _get_obs(self):
        """
        Note: Normalize values to [0, 1] so the neural network sees well-scaled inputs. Raw int values 0-3 can produce large gradients and slow or unstable learning.
        """
        grid = self._maze.astype(np.float32).copy()
        gr, gc = self.goal_pos
        grid[gr, gc] = 2
        ar, ac = self.agent_pos
        grid[ar, ac] = 3
        grid = grid / 3.0  # normalize 0-3 -> 0-1
        return grid[np.newaxis, :, :].astype(np.float32)  # shape (1, 10, 10)

    def reset(self, seed=None, options=None):
        # Track step count here so you can truncate long episodes in step().
        super().reset(seed=seed)
        self.agent_pos = self.start_pos
        self._steps = 0
        self._visited = {self.start_pos}
        return self._get_obs(), {}

    def step(self, action):
        """
        Note: Add a truncation condition (e.g., max 200 steps) — the episode should end if the agent hasn't reached the goal in time.
        Experiment with different reward values!!
         - wall penalty (-0.5), step penalty (-0.01), revisit penalty (-0.3)
         - What happens if you increase the goal reward? (+1 is quite small)
         - Try removing the revisit penalty and see what the agent does
        """
        self._steps += 1
        drow, dcol = ACTIONS[action]
        row, col = self.agent_pos
        nrow, ncol = row + drow, col + dcol

        terminated = False
        reward = -0.01  # step penalty

        if nrow < 0 or nrow >= self._maze.shape[0] or ncol < 0 or ncol >= self._maze.shape[1] or self._maze[nrow, ncol] == 1:
            reward += -0.5  # wall penalty, stay in place
        else:
            self.agent_pos = (nrow, ncol)
            if self.agent_pos in self._visited:
                reward += -0.3  # revisit penalty
            self._visited.add(self.agent_pos)

            if self.agent_pos == self.goal_pos:
                reward += 1.0  # goal reward
                terminated = True

        truncated = self._steps >= self._max_steps
        return self._get_obs(), reward, terminated, truncated, {}

    def _render_rgb(self):
        # Note: Return shape (height, width, 3) with uint8 values 0-255.
        rows, cols = self._maze.shape
        rgb = np.zeros((rows, cols, 3), dtype=np.uint8)
        rgb[self._maze == 1] = (40, 40, 40)     # walls
        rgb[self._maze == 0] = (255, 255, 255)  # paths
        gr, gc = self.goal_pos
        rgb[gr, gc] = (0, 200, 0)               # goal
        ar, ac = self.agent_pos
        rgb[ar, ac] = (200, 0, 0)               # agent
        return rgb


def main():
    env = MazeEnv()
    """
    - PPO's default ent_coef=0 means NO exploration pressure. If your agent gets stuck at the start, try ent_coef=0.01 to encourage trying things.
    - Try different learning rates (lr=0.0003 is the default):
      - too high -> unstable training
      - too low  -> slow progress
    - Increase total_timesteps if the agent hasn't converged.
    """
    model = PPO("MlpPolicy", env, verbose=1, n_steps=1024, batch_size=64, ent_coef=0.01)
    model.learn(total_timesteps=50_000)
    model.save("maze_ppo")


if __name__ == "__main__":
    main()
