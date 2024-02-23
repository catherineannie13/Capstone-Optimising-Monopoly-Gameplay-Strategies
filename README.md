# Optimising Monopoly Gameplay Strategies: A Simulation Modeling Study Using MCTS

## Abstract
This study presents an exploration into optimising gameplay strategies for Monopoly using Monte Carlo Tree Search (MCTS). By integrating a near-comprehensive simulation model of Monopoly with MCTS and an exploration of various gameplay strategies, this research aims to uncover evidence-based approaches for achieving victory in the game. Through the simulation of thousands of Monopoly games, the study analyses strategies related to property acquisition, development, and management, providing concrete recommendations for players seeking to enhance their gameplay. The findings reveal nuanced strategies that diverge from conventional wisdom, including the strategic purchase of certain property groups, the timing of building development, and the judicious use of mortgaging and jail time to maximise financial advantage. This research contributes to the broader understanding of game strategy optimisation, offering valuable insights into the complexities of Monopoly and presenting a robust framework for future studies in game strategy analysis.

## Table of Contents
├── Demos\
│   └── GameDemo.ipynb\
├── Exploration\
│   ├── BasicMonopolySimulation.ipynb\
│   ├── BoardSpaceProbabilities.ipynb\
│   ├── ExpectedRent.ipynb\
│   └── PaybackPeriods.ipynb\
├── Main\
│   ├── GridSearch_BaseStrategy.json\
│   ├── GridSearch_RandomStrategy.json\
│   ├── Hyperparameter_Search.ipynb\
│   ├── Main.ipynb\
│   ├── MCTS_BaseStrategy_100_game_outcomes.json\
│   ├── MCTS_BaseStrategy_100_node_actions_1.json\
│   ├── MCTS_BaseStrategy_100_node_actions_2.json\
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_game_outcomes.json\
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_node_actions_1.json\
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_node_actions_2.json\
│   ├── MCTS_BaseStrategy_MaxRounds100_1000_node_actions_3.json\
│   ├── MCTS_BaseStrategy_MaxRounds20_1000_game_outcomes.json\
│   ├── MCTS_BaseStrategy_MaxRounds20_1000_node_actions.json\
│   ├── MCTS_BaseStrategy_MaxRounds20_5000_game_outcomes.json\
│   ├── MCTS_BaseStrategy_MaxRounds20_5000_node_actions_1.json\
│   ├── MCTS_BaseStrategy_MaxRounds20_5000_node_actions_2.json\
│   ├── MCTS_RandomStrategy_100_game_outcomes.json\
│   └── Parsed Results\
│       ├── build.json\
│       ├── build_hotel.json\
│       ├── build_house.json\
│       ├── jail.json\
│       ├── mortgage.json\
│       ├── purchase.json\
│       ├── sell.json\
│       ├── sell_hotel.json\
│       ├── sell_house.json\
│       └── unmortgage.json\
├── MCTS\
│   ├── Examples\
│   │   ├── MCTSExample.ipynb\
│   │   └── MCTSTicTacToeExample.ipynb\
│   ├── MCTS.py\
│   ├── MCTS_NN.py\
│   ├── MonopolyBoardMCTS.py\
│   ├── NN.py\
│   ├── Node.py\
│   └── State.py\
├── README.md\
├── Simulation Classes\
│   ├── Chance.py\
│   ├── CommunityChest.py\
│   ├── FreeParking.py\
│   ├── Go.py\
│   ├── GoToJail.py\
│   ├── Jail.py\
│   ├── MonopolyBoard.py\
│   ├── Player.py\
│   ├── RandomStrategy.py\
│   ├── Station.py\
│   ├── Strategy.py\
│   ├── Street.py\
│   ├── Tax.py\
│   └── Utility.py\
├── Testing\
│   ├── TestingMCTS.ipynb\
│   ├── TestingSimulation.ipynb\
│   └── TestingState.ipynb\
└── Requirements.txt

## Prerequisites
Prerequesites can be found in the requirements.txt file. Use 'pip install requirements.txt' to install these dependencies.