# Week 4 — RL Environment Design & Training

This week you will learn how to build your own reinforcement learning environment and train an agent to solve it.

## Resources

- [Official Gymnasium Documentation](https://gymnasium.farama.org/introduction/create_custom_env/)
- [Video Tutorial](https://www.youtube.com/watch?v=bD6V3rcr_54)
- [Example Environment Implementation](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)

## Task 1 — CartPole (Warmup)

Run this file to see a pre-built environment in action:

```
python3 cartpole.py
```

Read the code. It creates a CartPole environment from Gymnasium, trains a PPO agent on it, and then lets the trained agent balance the pole. Learn more about cartpole from [here](https://gymnasium.farama.org/environments/classic_control/cart_pole/)


## Task 2 — Maze

You need to train an agent to navigate from the start to the goal in a maze. The maze has walls (1)and paths (0). The agent can move up, right, down, or left.

Example Maze layout:
```
1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 0 1
1 0 1 0 1 0 1 1 0 1
1 0 1 0 0 0 0 0 0 1
1 0 1 1 1 1 1 1 0 1
1 0 0 0 0 0 0 1 0 1
1 1 1 0 1 1 0 1 0 1
1 0 0 0 1 0 0 1 0 1
1 0 1 0 0 0 1 0 0 1
1 1 1 1 1 1 1 1 1 1
```
Start is at (1,1) and end at (8,8)
You need to complete the MazeEnv class in `maze_train.py`.

### Function Specifics

`__init__`
It stores the action space, observation space, maze layout, the start position, and the goal position.
- `self.action_space = spaces.Discrete(4)` means the agent has 4 choices: up, right, down, and left.
- `self.observation_space = Box(0, 3, (1, 10, 10), np.int8)` means the observation is a 10 by 10 grid where each cell has a value between 0 and 3. The (1, 10, 10) shape means there is one channel (like a black-and-white image) with 10 rows and 10 columns. You may want to use float32 and a normalized cell value for better results.

`_get_obs(self)`
This function turns the current maze and agent position into a numpy array.
The returned array should have shape `(1, 10, 10)` and use these values:
- `0` for empty path cells
- `1` for wall cells
- `2` for the goal cell
- `3` for the agent's current position
- Normalize them to [0,1]. 
  
`reset(self, seed=None)`
This function is called every time a new episode starts. It puts the agent back at the start position.
Read the documentation once for more detailed information.

`step(self, action)`
This function updates the agent's position based on the chosen action. It should check whether the move is valid, apply rewards, and determine if the goal has been reached. A positive reward is given for reaching the goal, while small penalties encourage the agent to avoid invalid moves and find efficient paths. The function then returns the outcome of the action.

`_render_rgb(self)`
This function creates a colour representation of the maze using a NumPy array. This array is used to render the maze using the blit function. Make sure to check its use case in maze.py

### Do this after you are done:

Install dependencies:
```
pip install -r requirements.txt
```

First, train the agent:
```
python3 maze_train.py
```

Then watch it solve the maze:
```
python3 maze.py
```

## Mid-Term Summary — What I Learned (RL Resources)

This week was a buffer week with no graded code deliverable, used to go through the Gymnasium docs, the linked video tutorial, and the custom-environment tutorial. Implementing `MazeEnv` (and reading `cartpole.py`) alongside those resources clarified the following:

- **The `gym.Env` contract**: every environment needs an `action_space` and `observation_space` (so the agent/policy knows the shape of inputs and outputs), plus `reset()` and `step()`. `reset()` starts a new episode and returns the first observation; `step(action)` advances the simulation one tick and returns `(observation, reward, terminated, truncated, info)`.
- **`terminated` vs `truncated`**: `terminated=True` means the episode ended because of the environment's own rules (agent reached the goal, or "died"). `truncated=True` means the episode was cut off for an external reason (a step limit), even though the task itself wasn't finished. Keeping a `max_steps` counter and using `truncated` is what stops an episode from running forever if the agent never finds the goal.
- **Observation design matters for learning speed**: feeding raw integer cell values (0-3) into a neural network trains far less smoothly than normalizing them to `[0, 1]` float32 — large unscaled inputs produce large/unstable gradients. This is why `_get_obs()` divides the maze array by 3 before returning it.
- **Reward shaping changes agent behavior directly**: a small per-step penalty pushes the agent toward shorter paths; a separate, larger penalty for hitting walls discourages invalid moves without making the agent overly cautious; a penalty for revisiting a cell discourages looping in place. Removing the revisit penalty (as the skeleton comments suggested experimenting with) tends to make the agent wander more before committing to a path.
- **PPO (Proximal Policy Optimization)**: a policy-gradient RL algorithm that updates the policy in small, "clipped" steps so a single batch of experience can't push the policy too far from where it just was — this is what `clip_range` controls in the training logs. `ent_coef` adds an exploration bonus (entropy of the action distribution); with the default `ent_coef=0`, an agent can get stuck repeating the same action if it finds no reward signal early on, since it has no incentive to try alternatives.
- **CartPole as a sanity check**: `cartpole.py` is useful because the environment is built-in and known-good, so training on it first confirms the RL pipeline (gymnasium + stable-baselines3 + PPO) works *before* debugging a custom environment, isolating whether bugs are in the algorithm setup or in my own `MazeEnv` code.
- **Practical result**: training `MazeEnv` for 50,000 timesteps converged to `ep_rew_mean ≈ 0.85` with `ep_len_mean ≈ 14` steps — close to the maze's shortest possible path, confirming the reward shaping and observation encoding above were effective.

  
We were also given Sutton & Barto's *Reinforcement Learning: An Introduction* (2020 edition) as a resource — I have only skimmed Chapter 1 (Introduction) so far and have not properly studied it yet. From that chapter, the framing that stuck with me is RL as learning from interaction rather than from labeled examples (unlike supervised learning) or from finding structure in unlabeled data (unlike unsupervised learning) — the agent senses state, takes actions, and learns through trial-and-error search and delayed reward. I want to go through the rest of the book properly after the mid-term deadline, since it should give the formal theory (Markov decision processes, value functions, etc.) behind the PPO/Gymnasium concepts I only understood practically this week.

**Note on AI assistance**: I used an AI assistant to help me understand some of these RL concepts and with syntax while implementing `MazeEnv` (e.g. Gymnasium API conventions, Stable-Baselines3 usage) — the explanations above and the code are written based on that understanding, not copied blindly.

