# --- Day 2: Rock Paper Scissors ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/2](https://adventofcode.com/2022/day/2)

The problem is a simulation of a Rock-Paper-Scissors game, where the player is given an encrypted strategy guide and they need to calculate the total score they will get if they follow the strategy guide. The score for each round is determined by the choice of shape the player selects (1 for Rock, 2 for Paper, and 3 for Scissors), and the outcome of the round (0 if the player loses, 3 if the round is a draw, and 6 if the player wins).

In Part One, the player is instructed to choose a shape in response to their opponent's shape, and the score is calculated based on whether the player wins, loses, or draws.

In Part Two, the player is instructed to choose a shape in such a way that the round ends as indicated by the second column of the strategy guide. The letter (X, Y or Z) represents the needed outcome of the round, X is a loss, Y is a draw and Z is a win. the player will need to figure out the corresponding shape based on the letter they are given in the strategy guide, and calculate the total score in the same way as in Part One.