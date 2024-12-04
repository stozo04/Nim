import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
         # Step 1: Get the current Q-value for the (old_state, action) pair
        # This tells us what the AI currently "thinks" about the quality of this action in this state.
        old = self.get_q_value(old_state, action)

        # Step 2: Determine the best possible future reward from the new state
        # This looks at all possible actions in the new_state and finds the highest Q-value.
        # If no Q-values exist for the new_state, it defaults to 0.
        best_future = self.best_future_reward(new_state)

        # Step 3: Update the Q-value for the (old_state, action) pair
        # This uses the Q-learning formula to adjust the Q-value based on:
        # - The immediate reward received for the action
        # - The expected rewards from future actions
        # - How confident we are in new information (controlled by alpha)
        self.update_q_value(old_state, action, old, reward, best_future)
    
    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        # Step 1: Convert the state from a list to a tuple
        # This is because tuples are immutable and can be used as dictionary keys.
        # Example: [1, 2, 3] -> (1, 2, 3)
        state_tuple = tuple(state)

        # Step 2: Retrieve the Q-value for the (state, action) pair
        # Use the `get` method to fetch the value from the dictionary.
        # If the key doesn't exist in `self.q`, it will return 0 as a default.
        return self.q.get((state_tuple, action), 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        # Step 1: Calculate the new value estimate
        # This is the sum of the immediate reward and the estimated future rewards.
        # Example: If reward is 1 and future_rewards is 0.5, new_value_estimate = 1.5.
        new_value_estimate = reward + future_rewards

        # Step 2: Apply the Q-learning formula
        # The new Q-value is the old Q-value plus an adjustment term:
        # The adjustment is `alpha * (new_value_estimate - old_q)`, which shifts the old value
        # towards the new estimate, based on the learning rate (alpha).
        self.q[(tuple(state), action)] = old_q + self.alpha * (new_value_estimate - old_q)

    # Note: `tuple(state)` converts the state list to a tuple because tuples are hashable
    # and can be used as keys in a dictionary.

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        # Step 1: Convert the state to a tuple, since states need to be hashable for dictionary keys
        state_tuple = tuple(state)

        # Step 2: Get all available actions for the current state
        actions = Nim.available_actions(state)  # Returns a set of valid actions, e.g., {(0, 1), (1, 2)}
        
        # Step 3: Handle edge case where no actions are available
        if not actions:
            # No actions mean no future reward
            return 0

        # Step 4: Calculate the maximum Q-value for all possible actions
        # Use `get()` to safely retrieve Q-values from the dictionary; default to 0 if not found
        max_reward = max(self.q.get((state_tuple, action), 0) for action in actions)
        
        # Step 5: Return the best Q-value found
        return max_reward

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        
        # Step 1: Get all possible actions in the current state
        actions = list(Nim.available_actions(state))  # List of all valid actions
        if not actions:
            # If no actions are available, raise an error (this should not happen in normal gameplay)
            raise Exception("No available actions.")

        # Step 2: Decide whether to explore or exploit
        if epsilon and random.random() < self.epsilon:
            # Explore: Randomly choose an action
            # The `random.random()` function generates a number between 0 and 1.
            # If it's less than `self.epsilon`, we randomly select an action.
            return random.choice(actions)
        else:
            # Exploit: Choose the best action based on Q-values
            # Convert the state into a tuple since it's used as a dictionary key
            state_tuple = tuple(state)

            # Find the action with the highest Q-value.
            # If an action has no Q-value (not yet learned), assume it's 0.
            best_action = max(
                actions,  # The list of all possible actions
                key=lambda action: self.q.get((state_tuple, action), 0)  # Use Q-value as the "score"
            )
            return best_action


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return
