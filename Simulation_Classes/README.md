# Simulation Classes Package: Monopoly Simulation

This package, `simulation_classes`, provides a comprehensive suite of classes to simulate the classic board game Monopoly. It is designed to model the game's dynamics, including properties, players, and game logic, offering a robust foundation for creating and analyzing Monopoly strategies. Below is an overview of the key components and functionalities provided by this package.

## Features

- **Monopoly Board Simulation**: A central `MonopolyBoard` class that encapsulates the game board, properties, and players, facilitating the simulation of full game rounds.
- **Game Entities**: Includes classes for various game entities such as `Chance`, `CommunityChest`, `FreeParking`, `Go`, `GoToJail`, `Jail`, `Player`, `Station`, `Strategy`, `RandomStrategy`, `Street`, `Tax`, and `Utility`.
- **Gameplay Mechanics**: Implements methods for simulating the game's mechanics, such as moving around the board, buying properties, paying rent, drawing Chance and Community Chest cards, and handling special board spaces like Jail and Free Parking.
- **Strategic Framework**: The package includes a `Strategy` class that can be extended to define custom gameplay strategies. A `RandomStrategy` class is provided as an example.

## Installation

### **Option 1**
Clone this repository to your local machine:

```bash
bashCopy code
git clone https://github.com/catherineannie13/Capstone-Optimising-Monopoly-Gameplay-Strategies.git
cd monopoly-mcts-ai

```

Ensure you have Python 3.8 or later installed. It's recommended to use a virtual environment:

```bash
bashCopy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

Install the required dependencies:

```bash
bashCopy code
pip install -r requirements.txt

```

### **Option 2**
Run pip install -i https://pypi.org/simple/ simulation-classes-catherineannie13==0.0.1

## Usage

Here is a simple example to get started with simulating a Monopoly game:

```python
from simulation_classes.monopoly_board import MonopolyBoard
from simulation_classes.player import Player

# Initialize the game board
board = MonopolyBoard()

# Create players
player1 = Player("Player 1")
player2 = Player("Player 2")

# Add players to the board
board.add_player(player1)
board.add_player(player2)

# Start the game simulation
board.play_game()

```

## Documentation

For a detailed description of all classes and methods, refer to the inline documentation provided within each module. The `MonopolyBoard` class documentation offers insights into the initialization parameters, attributes, and available methods for simulating the game and interactions between game entities.

## Contributing

Contributions to the `simulation_classes` package are welcome. Please refer to the project's repository for contribution guidelines and submit pull requests with any enhancements, bug fixes, or documentation improvements.

## License

`simulation_classes` is released under the MIT License. See the LICENSE file in the project repository for more information.