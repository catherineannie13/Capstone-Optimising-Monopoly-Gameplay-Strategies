# Optimising Monopoly Gameplay Strategies: A Simulation Modeling Study Using MCTS

## Abstract
This study presents an exploration into optimising gameplay strategies for Monopoly using Monte Carlo Tree Search (MCTS). By integrating a near-comprehensive simulation model of Monopoly with MCTS and an exploration of various gameplay strategies, this research aims to uncover evidence-based approaches for achieving victory in the game. Through the simulation of thousands of Monopoly games, the study analyses strategies related to property acquisition, development, and management, providing concrete recommendations for players seeking to enhance their gameplay. The findings reveal nuanced strategies that diverge from conventional wisdom, including the strategic purchase of certain property groups, the timing of building development, and the judicious use of mortgaging and jail time to maximise financial advantage. This research contributes to the broader understanding of game strategy optimisation, offering valuable insights into the complexities of Monopoly and presenting a robust framework for future studies in game strategy analysis.

## Table of Contents
├── .gitignore
├── Demos
│   └── GameDemo.ipynb
├── Exploration
│   ├── BasicMonopolySimulation.ipynb
│   ├── BoardSpaceProbabilities.ipynb
│   ├── ExpectedRent.ipynb
│   └── PaybackPeriods.ipynb
├── Main
│   ├── GridSearch_BaseStrategy.json
│   ├── GridSearch_RandomStrategy.json
│   ├── Hyperparameter_Search.ipynb
│   ├── Main.ipynb
│   ├── MCTS_BaseStrategy_100_game_outcomes.json
│   ├── MCTS_BaseStrategy_100_node_actions_1.json
│   ├── MCTS_BaseStrategy_100_node_actions_2.json
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_game_outcomes.json
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_node_actions_1.json
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_node_actions_2.json
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_node_actions_3.json
│   ├── MCTS_BaseStrategy_MaxRounds20_1000_game_outcomes.json
│   ├── MCTS_BaseStrategy_MaxRounds20_1000_node_actions.json
│   ├── MCTS_BaseStrategy_MaxRounds20_5000_game_outcomes.json
│   ├── MCTS_BaseStrategy_MaxRounds20_5000_node_actions_1.json
│   ├── MCTS_BaseStrategy_MaxRounds20_5000_node_actions_2.json
│   ├── MCTS_RandomStrategy_100_game_outcomes.json
│   └── Parsed Results
│       ├── build.json
│       ├── build_hotel.json
│       ├── build_house.json
│       ├── jail.json
│       ├── mortgage.json
│       ├── purchase.json
│       ├── sell.json
│       ├── sell_hotel.json
│       ├── sell_house.json
│       └── unmortgage.json
├── MCTS
│   ├── dist
│   │   ├── mcts_catherineannie13-0.0.1-py3-none-any.whl
│   │   └── mcts_catherineannie13-0.0.1.tar.gz
│   ├── LICENSE
│   ├── pyproject.toml
│   ├── README.md
│   └── src
│       └── mcts
│           ├── MCTS.py
│           ├── MCTS_NN.py
│           ├── MonopolyBoardMCTS.py
│           ├── NN.py
│           ├── Node.py
│           ├── State.py
│           └── __init__.py
├── README.md
├── requirements.txt
├── Simulation_Classes
│   ├── dist
│   │   ├── simulation_classes_catherineannie13-0.0.1-py3-none-any.whl
│   │   └── simulation_classes_catherineannie13-0.0.1.tar.gz
│   ├── LICENSE
│   ├── pyproject.toml
│   ├── README.md
│   └── src
│       └── simulation_classes
│           ├── Chance.py
│           ├── CommunityChest.py
│           ├── FreeParking.py
│           ├── Go.py
│           ├── GoToJail.py
│           ├── Jail.py
│           ├── MonopolyBoard.py
│           ├── Player.py
│           ├── RandomStrategy.py
│           ├── Station.py
│           ├── Strategy.py
│           ├── Street.py
│           ├── Tax.py
│           ├── Utility.py
│           └── __init__.py
└── Testing
    ├── TestingMCTS.ipynb
    ├── TestingSimulation.ipynb
    └── TestingState.ipynb

## Usage
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

If you are only interested in using simulation classes or MCTS classes, these can be installed using:
```bash
pip install simulation-classes-catherineannie13==0.0.1
pip install mcts-catherineannie13==0.0.1
```

You can visit the respective package documentations as follows:
- https://pypi.org/project/simulation-classes-catherineannie13/0.0.1/
- https://pypi.org/project/mcts-catherineannie13/0.0.1/


## Prerequisites
Prerequesites can be found in the requirements.txt file. Use 'pip install requirements.txt' to install these dependencies.