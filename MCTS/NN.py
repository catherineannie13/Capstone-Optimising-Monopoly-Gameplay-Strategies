import torch.nn as nn

class NN(nn.Module):
    """
    This class represents a neural network model for a specific task.

    Parameters
    ----------
    input_size : int
        The size of the input layer.
    output_size : int
        The size of the output layer.
    """

    def __init__(self, input_size, output_size):
        super(NN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, output_size)

    def forward(self, x):
        """
        Performs forward pass through the neural network.

        Parameters
        ----------
        x : tensor
            The input tensor.

        Returns
        -------
        tensor
            The output tensor.
        """
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x