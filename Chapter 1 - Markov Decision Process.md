---
tags: [reinforcement-learning, mdp, rl-arena]
chapter: 1
topic: Markov Decision Process
---

# Chapter 1 — Markov Decision Process (MDP)

## 1. Why MDPs?
- MDPs are the **mathematical framework** for sequential decision-making under uncertainty.
- Almost all of Reinforcement Learning (RL) is built on top of the MDP formalism.
- An **agent** interacts with an **environment** over discrete time steps, taking actions and receiving rewards.

---

## 2. The Agent-Environment Loop
- At each time step $t$:
	1. Agent observes state $S_t$
	2. Agent takes action $A_t$
	3. Environment returns reward $R_{t+1}$ and next state $S_{t+1}$
- This repeats, generating a trajectory:
$$
S_0, A_0, R_1, S_1, A_1, R_2, S_2, A_2, R_3, \dots
$$

> [!note] Mental model
> Agent ↔ Environment loop = perceive → act → get feedback → repeat

---

## 3. Formal Definition of an MDP
An MDP is defined as a tuple:
$$
\langle S, A, P, R, \gamma \rangle
$$

| Symbol | Meaning |
|---|---|
| $S$ | Set of all possible **states** |
| $A$ | Set of all possible **actions** |
| $P$ | **Transition probability** function |
| $R$ | **Reward** function |
| $\gamma$ | **Discount factor** ($0 \le \gamma \le 1$) |

### Transition Function
$$
P(s' \mid s, a) = \Pr(S_{t+1} = s' \mid S_t = s, A_t = a)
$$
- Probability of ending up in state $s'$ given you were in state $s$ and took action $a$.

### Reward Function
$$
R(s, a, s') = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a, S_{t+1} = s']
$$
- Expected immediate reward from that transition.

---

## 4. The Markov Property
> "The future is independent of the past given the present."

$$
\Pr(S_{t+1} \mid S_t, A_t, S_{t-1}, A_{t-1}, \dots, S_0, A_0) = \Pr(S_{t+1} \mid S_t, A_t)
$$

- The **current state must capture all relevant information** from history.
- This is what makes the problem tractable — no need to remember the entire history, just the current state.

---

## 5. Policies
A **policy** $\pi$ defines the agent's behavior.

- **Deterministic policy:** $a = \pi(s)$
- **Stochastic policy:** $\pi(a \mid s) = \Pr(A_t = a \mid S_t = s)$

The goal of RL/planning is to find an **optimal policy** $\pi^*$ that maximizes long-term reward.

---

## 6. Returns and Discounting
The **return** $G_t$ is the total accumulated reward from time $t$ onward:

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$$

### Why discount ($\gamma$)?
- Makes infinite sums **converge** (mathematically well-defined).
- Encodes preference for **sooner rewards** over later ones.
- $\gamma \to 0$: agent is "myopic" (only cares about immediate reward).
- $\gamma \to 1$: agent is "far-sighted" (cares about long-term reward).

> [!warning]
> Setting $\gamma = 1$ in an infinite-horizon task can cause the return to diverge unless rewards are guaranteed to reach zero (e.g., episodic tasks).

---

## 7. Value Functions

### State-Value Function
Expected return starting from state $s$, following policy $\pi$:
$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]
$$

### Action-Value Function (Q-function)
Expected return starting from state $s$, taking action $a$, then following $\pi$:
$$
Q^\pi(s, a) = \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a]
$$

These functions let us **compare states/actions** and drive policy improvement.

---

## 8. Bellman Equation (Preview)
Value functions can be written **recursively**:

$$
V^\pi(s) = \sum_{a} \pi(a \mid s) \sum_{s'} P(s' \mid s,a) \Big[ R(s,a,s') + \gamma V^\pi(s') \Big]
$$

- This recursive structure (today's value = immediate reward + discounted value of next state) is the foundation for **Dynamic Programming**, **Value Iteration**, and **Q-Learning** — covered in later chapters.

---

## 9. Types of MDP Problems
- **Finite MDP:** finite $S$ and $A$ (most intro examples: gridworlds, etc.)
- **Episodic tasks:** interaction breaks into episodes with a terminal state (e.g., a game round).
- **Continuing tasks:** interaction goes on indefinitely (no natural terminal state) — discounting becomes essential here.

---

## 10. Key Takeaways
- [ ] MDP = $\langle S, A, P, R, \gamma \rangle$
- [ ] Markov property → next state depends only on current state + action
- [ ] Policy $\pi$ → mapping from states to actions
- [ ] Return $G_t$ → discounted sum of future rewards
- [ ] $V^\pi(s)$ and $Q^\pi(s,a)$ → measure "goodness" of states/actions under a policy
- [ ] Bellman equation → recursive decomposition of value, sets up next chapter (Dynamic Programming)

---

## References / Further Reading
- Sutton & Barto — *Reinforcement Learning: An Introduction* (Ch. 3)
- [[RL Arena]] project notes

%% Source video: https://www.youtube.com/watch?v=VnpRp7ZglfA  — transcript unavailable at time of writing, notes based on standard MDP curriculum. Update this file if the actual lecture covers content differently. %%
