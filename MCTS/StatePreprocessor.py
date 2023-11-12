import numpy as np
import torch
class StatePreprocessor:
    def __init__(self, game_state):
        self.game_state = game_state

    def extract_player_info(self, player):
        # extract relevant player information
        player_info = [
            player.money,
            len(player.properties),
            len(player.stations),
            len(player.utilities),
            player.jail_cards,
            player.houses,
            player.hotels
        ]
        return np.array(player_info)

    def extract_board_info(self):
        board_info = [
            len(self.game_state.properties),
            len(self.game_state.stations),
            len(self.game_state.utilities),
            len(self.game_state.tax),
            len(self.game_state.chance.cards),
            len(self.game_state.community_chest.cards),
            self.game_state.go.position,
            self.game_state.jail.position,
            self.game_state.free_parking.position,
            self.game_state.go_to_jail.position
        ]
        return np.array(board_info)

    def preprocess_state(self):
        player_infos = [self.extract_player_info(player) for player in self.game_state.players]
        board_info = self.extract_board_info()

        # concatenate player and board information into a single feature vector
        feature_vector = np.concatenate([info.flatten() for info in player_infos] + [board_info])

        return feature_vector