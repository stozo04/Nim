
# Nim Game AI with Q-Learning

This project implements an **AI player for the game of Nim** using **Q-learning**, a type of reinforcement learning. The AI learns optimal strategies by playing against itself, making it increasingly better over time.

---

## Table of Contents
- [Introduction](#introduction)
- [Game Rules](#game-rules)
- [How the AI Works](#how-the-ai-works)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [How to Train the AI](#how-to-train-the-ai)
- [How to Play Against the AI](#how-to-play-against-the-ai)
- [File Structure](#file-structure)
- [Customization Options](#customization-options)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

This project creates an AI to play the game of **Nim**, a classic game of strategy. By using **Q-learning**, the AI learns to make better decisions by updating its understanding of the game's states and possible actions based on rewards and penalties.

The goal? Create an AI that can give even the most strategic human player a tough challenge!

---

## Game Rules

1. **Setup**:
   - The game starts with a number of piles, each containing a specific number of objects.

2. **Gameplay**:
   - Players take turns.
   - On a turn, a player removes any number of objects from a single pile (at least one object).

3. **Winning Condition**:
   - The player forced to remove the last object **loses** the game.

---

## How the AI Works

The AI uses **Q-learning**, a type of reinforcement learning:
- **State**: The current configuration of the piles (e.g., `[1, 3, 5]`).
- **Action**: Removing a specific number of objects from a specific pile (e.g., `(1, 2)`).
- **Q-values**: The AI maintains a dictionary of `(state, action)` pairs and their corresponding "goodness" (reward).
- **Training**: By playing games against itself, the AI learns:
  - Good actions to take in different states (rewarded with +1 for a win).
  - Bad actions to avoid (penalized with -1 for a loss).

### Key Components:
1. **Exploration vs. Exploitation**:
   - The AI explores random moves sometimes (exploration) to discover new strategies.
   - It also selects the best-known move most of the time (exploitation).

2. **Learning Rate (`alpha`)**:
   - Controls how quickly the AI updates its knowledge.

3. **Discount Factor (`epsilon`)**:
   - Encourages the AI to occasionally explore new strategies.

---

## Key Features

- **Trainable AI**: The AI improves over time by playing more games.
- **Human vs. AI**: Play against the trained AI and test your skills!
- **Customizable**: Adjust the number of piles, objects, and training parameters for a personalized experience.
- **Epsilon-Greedy Strategy**: Balances exploration and exploitation during gameplay.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/nim-ai.git
   cd nim-ai
   ```

2. Install Python (if not already installed):
   - Download from [python.org](https://www.python.org/).

3. No external libraries are required—this project runs on standard Python modules.

---

## Usage

### How to Train the AI

1. Open the `play.py` file.
2. Edit the number of training games (default: 10,000):
   ```python
   ai = train(10000)
   ```
3. Run the training script:
   ```bash
   python play.py
   ```

The AI will play games against itself and improve over time. You'll see messages like:
```
Playing training game 1
Playing training game 2
...
Done training
```

---

### How to Play Against the AI

1. Run the `play.py` script:
   ```bash
   python play.py
   ```

2. Follow the prompts to play:
   ```
   Piles:
   Pile 0: 1
   Pile 1: 3
   Pile 2: 5
   Your Turn
   Choose Pile: 1
   Choose Count: 2
   ```

3. The game alternates between you and the AI until a winner is determined.

---

## File Structure

- **`nim.py`**:
  - Contains the game logic and AI implementation.
  - Key classes and methods:
    - `Nim`: Handles game state and rules.
    - `NimAI`: Implements Q-learning for decision-making.

- **`play.py`**:
  - Used to train the AI and allow human players to play against it.

---

## Customization Options

### Adjusting the Game Setup
You can modify the initial pile configuration in the `Nim` class:
```python
game = Nim(initial=[3, 4, 5])  # Three piles with 3, 4, and 5 objects
```

### Changing AI Learning Parameters
Modify the AI's learning behavior in the `NimAI` class:
- **Learning rate (`alpha`)**:
  ```python
  player = NimAI(alpha=0.7)  # Faster updates
  ```
- **Exploration rate (`epsilon`)**:
  ```python
  player = NimAI(epsilon=0.2)  # More random exploration
  ```

---

## Contributing

Contributions are welcome! If you’d like to improve this project:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes and submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to suggest any improvements or let me know if you have questions. Enjoy playing (or coding) Nim! 😊
