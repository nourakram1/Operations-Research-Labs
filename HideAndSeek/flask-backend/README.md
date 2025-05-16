# 🎲 Hide and Seek Game Backend

Welcome to the **Hide and Seek Game Backend**!  
This project brings together the fun of classic hide-and-seek with the power of operations research and game theory, all wrapped in a modern Flask API.

---

## 🌟 Concept

Imagine a grid-based board where:
- 🕵️ **The Hider** picks a secret cell to hide in.
- 🔍 **The Seeker** tries to find the hider by choosing a cell.

But there’s a twist:  
Each cell has a **difficulty level** — `EASY`, `NEUTRAL`, or `HARD` — which changes the risk and reward for the seeker!

---

## 🧠 Mathematical Magic

This isn’t just a game—it’s a **two-player zero-sum game**:
- The board is transformed into a matrix, with each cell’s difficulty shaping the payoffs.
- Using **linear programming**, the backend computes the **optimal mixed strategies** for both players, ensuring fair and strategic play.

---

## 📚 Theoretical Foundations

> “Games are the most elevated form of investigation.”  
> — Albert Einstein

**Game Theory** is at the heart of this project. Here’s how the theory comes alive:

- **Zero-Sum Dynamics:** Every gain for the seeker is a loss for the hider, and vice versa. The strategies are calculated so that neither player can improve their outcome by changing their own strategy alone.
- **Mixed Strategies:** Instead of always picking the same cell, both players randomize their choices based on mathematically optimal probabilities. This makes the game unpredictable and fair.
- **Linear Programming:** We use advanced optimization techniques to solve for the Nash Equilibrium, ensuring both players are playing as smart as possible.
- **Payoff Matrix:** The board’s difficulties are encoded into a matrix, which is the battleground for strategic decision-making.

**Why does this matter?**  
This approach models real-world scenarios where decisions must be made under uncertainty and with incomplete information—think cybersecurity, economics, or even sports!

---

## 🚀 API Features

- 🎲 **/generate**: Create a random game board with your chosen size and get the optimal strategies for both players.
- 🧮 **/play**: Simulate a move based on any probability distribution you provide.

**What you can do:**
- Generate boards with custom dimensions and random difficulties.
- Retrieve mathematically optimal strategies for both hider and seeker.
- Simulate moves and see the outcome, all via simple API calls.

---

## 🛠️ Applications

- 📚 **Education**: Perfect for teaching game theory, probability, and optimization.
- 🧪 **Research**: Experiment with strategies and payoffs in a controlled environment.
- 🎮 **Gaming**: Use as a backend for web or mobile games that need smart, strategic gameplay.

---

## 💡 Why This Project?

This backend is a showcase of how **mathematical optimization** and **probability** can turn a simple childhood game into a rich field for learning and experimentation. Whether you’re a student, a researcher, or a developer, you’ll find something to explore!

---

## 📬 Get Involved

Questions or ideas?  
Open an issue or submit a pull request—let’s make hide and seek smarter together!