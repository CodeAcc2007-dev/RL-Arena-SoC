---
tags: [reinforcement-learning, mdp, monte-carlo, rl-arena]
chapter: 1
topic: Grid Maze Example & Monte Carlo Methods
source: https://youtu.be/VnpRp7ZglfA
timestamp: 16:37 - 36:22
---

# Grid Maze Example & Monte Carlo Methods

## 1. The Grid Maze Setup
A simple gridworld is used to make the MDP framework concrete:

- A small maze with just **one wall**.
- The agent starts at a fixed **start cell** and must reach a **target cell**.
- Allowed moves: **up, down, left, right** — the agent cannot move through walls.
- **Episode length cap:** 20 steps.
- **Termination condition:** the episode ends when either
	- the agent reaches the target, **or**
	- it has taken 20 steps without reaching the target.

> [!note] Why this example?
> It's small enough to reason about by hand, but rich enough to illustrate states, actions, rewards, transitions, and episodes all at once.

---

## 2. Mapping the Maze onto an MDP
To formalize the maze as an MDP, we need to define state, action, and reward:

| MDP element | Grid maze instance |
|---|---|
| **State** $S$ | The agent's current cell (position) in the grid |
| **Action** $A$ | One of {up, down, left, right} |
| **Reward** $R$ | Feedback signal — e.g. penalizing each step to encourage shorter paths, and/or a bonus on reaching the target |
| **Terminal condition** | Reaching the target cell, or hitting the 20-step cap |

- Walls act as constraints on the transition function: an action that would move the agent into a wall simply leaves it in the same cell (or is disallowed).
- Because the episode can end without reaching the goal (step cap), this is an **episodic task with a fixed maximum horizon**.

---

## 3. Trajectories and Episodes
- Once state/action/reward are defined, the agent can act in the maze and generate a **trajectory** (an episode):
$$
S_0, A_0, R_1, S_1, A_1, R_2, \dots, S_T
$$
- Each full run from start to termination (goal or step-cap) is one **episode**.
- Running the agent repeatedly through the maze produces many **sampled episodes** — this sampled experience is the raw material Monte Carlo methods use to learn.

---

## 4. From Trajectories to Monte Carlo Methods
The key idea introduced here: instead of requiring a full model of the environment (transition probabilities, reward function), we can **learn value estimates directly from sampled experience**.

- For each episode, compute the **return** $G_t$ for each visited state (discounted sum of rewards from that point onward).
- **Monte Carlo (MC) methods** estimate the value of a state by **averaging the observed returns** across many episodes where that state was visited.

$$
V(s) \approx \text{average of } G_t \text{ over all visits to } s \text{ across sampled episodes}
$$

- This is fundamentally different from Dynamic Programming: MC doesn't need $P(s'\mid s,a)$ or $R(s,a,s')$ up front — it just needs **experience** (sampled trajectories).

---

## 5. Tracking Value Estimates in a Table
- A simple way to implement this: keep a **table** with one entry per state (or state-action pair).
- For each state visited during an episode:
	1. Compute the return $G_t$ from that point to the end of the episode.
	2. Add it to a running list/average for that state's entry in the table.
- Over many episodes, the table entries converge toward the true value function $V^\pi(s)$ for the policy being followed.

> [!tip] Intuition
> Think of the table as a scoreboard: every time the agent passes through a cell, it records "here's how things turned out from here" and averages that over time.

---

## 6. Why This Matters
- This grid maze + table-averaging approach is the **simplest possible version of Monte Carlo estimation** — no bootstrapping, no function approximation, just counting and averaging.
- It sets up the contrast for later chapters:
	- **Monte Carlo** → learns from complete episodes, averages actual returns.
	- **Temporal-Difference (TD) learning** (later chapters) → updates estimates from partial episodes using bootstrapping.

---

## 7. Key Takeaways
- [ ] The maze example maps state → cell, action → direction, reward → step/goal feedback.
- [ ] Episodes terminate at the goal or after a fixed step cap (20 steps here).
- [ ] Sampling many episodes gives trajectories to learn from.
- [ ] Monte Carlo methods estimate $V(s)$ by **averaging observed returns** across visits, using a simple table.
- [ ] No environment model needed — MC learns purely from experience.

---

## References
- [[Chapter 1 - Markov Decision Process]]
- Sutton & Barto — *Reinforcement Learning: An Introduction* (Ch. 5, Monte Carlo Methods)

%% Source: https://youtu.be/VnpRp7ZglfA, timestamp 16:37-36:22. Notes built from the provided transcript excerpt (17:49-18:24) plus standard MC-methods framing; verify against the full video for exact wording/details. %%
