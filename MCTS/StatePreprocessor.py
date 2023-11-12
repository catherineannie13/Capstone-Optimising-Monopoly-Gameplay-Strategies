import numpy as np
import torch
class StatePreprocessor:
    def __init__(self, game_state):
        self.game_state = game_state

    def extract_player_info(self):
        player_info = [...]
        return np.array(player_info)

    def extract_property_info(self):
        property_info = [...]
        return np.array(property_info)

    def preprocess_state(self):
        player_info = self.extract_player_info()
        property_info = self.extract_property_info()
        feature_vector = np.concatenate([player_info, property_info])
        return torch.tensor(feature_vector).float().unsqueeze(0)