# RL Arena — Games and Reinforcement Learning

A Season of Code collection of Pygame grid games and introductory reinforcement-learning experiments. The completed coursework in this repository covers Weeks 1–4: movement, grid collisions, territory capture, and a custom Gymnasium maze trained with PPO.

## Explore

| Module | Implementation | Run |
|---|---|---|
| [Week 1](WEEK-1/) | Grid movement and obstacles | `cd WEEK-1 && python main.py` |
| [Week 2](WEEK-2/) | Two-player light-cycle trail game | `cd WEEK-2 && python main.py` |
| [Week 3](WEEK-3/) | Territory capture with flood-fill logic | `cd WEEK-3 && python main.py` |
| [Week 4](WEEK-4/) | Gymnasium MazeEnv, PPO training, and CartPole example | `cd WEEK-4 && python maze_train.py` |

## Setup

```bash
git clone https://github.com/CodeAcc2007-dev/RL-Arena-SoC.git
cd RL-Arena-SoC
python -m venv .venv
source .venv/bin/activate
python -m pip install -r WEEK-4/requirements.txt
```

Run a module from its own folder so local imports and model paths resolve. The Pygame games need a graphical desktop. After training the maze policy, `python maze.py` in `WEEK-4` displays the agent. The repository also includes the original `maze_ppo.zip` checkpoint; library-version compatibility can affect loading it.

## Learning notes

- [Markov decision processes](Chapter%201%20-%20Markov%20Decision%20Process.md)
- [Grid mazes and Monte Carlo methods](Chapter%202%20-%20Grid%20Maze%20Example%20and%20Monte%20Carlo%20Methods.md)
- [Week 4 implementation and reflection](WEEK-4/README.md)

This is an educational collection, not a general-purpose RL library or a completed full-season submission. Historical training observations in the week notes are recorded results; the documentation update does not rerun PPO training.

Original project: Seasons of Code, PID 73, RL Arena. The local workspace also contains staged changes; this update uses the existing GitHub version and preserves those unpublished local changes.
