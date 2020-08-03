import numpy as np
from computation.machine_learning.activation_functions import (
    sigmoid,
    sigmoid_derivative,
)


class NeuralNetwork:
    def __init__(self, x, y, learn_rate=1):
        """
        Create a neural network with one hidden layer
        Each matrix has the following dimensions:
            Input Matrix: n x m
            Weight 1 Matrix: m x 4
            Weight 2 Matrix: 4 x l
            Output Matrix: n x l

        Note: Size indicates the number of neural units at each layer

        Args:
            x (ndarray): n x m array where n is the number of training
                         examples and m is the size of a single input
            y (ndarray): n x l array where n is the number of training
                         examples and l is the size of expected output
            learn_rate (float): learning rate of the neural network
        """
        self.input_layer_size = x.shape[1]
        self.output_layer_size = y.shape[1]
        self.hidden_layer_size = 4

        self.input = x
        self.y = y
        self.weights1 = np.random.rand(
            self.input_layer_size, self.hidden_layer_size
        )
        self.weights2 = np.random.rand(
            self.hidden_layer_size, self.output_layer_size
        )
        self.output = np.zeros(self.y.shape)
        self.learn_rate = learn_rate

    def feedforward(self):
        """
        Run forward propogation to calculate the expected result
        """
        self.hidden_layer = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.hidden_layer, self.weights2))

    def backprop(self):

        # Find derivates for backpropogation
        d_output = -(
            (self.y - self.output)  # n x 1
            * sigmoid_derivative(self.output)  # n x 1
        )
        d_hidden = np.dot(
            d_output, self.weights2.T
        ) * sigmoid_derivative(  # n x 4
            self.hidden_layer
        )  # n x 4

        # application of the chain rule to find derivative of the loss
        # function with respect to weights2 and weights1
        d_weights2 = np.dot(self.hidden_layer.T, d_output)
        d_weights1 = np.dot(self.input.T, d_hidden)

        # update the weights with the derivative (slope) of the loss function
        self.weights1 -= self.learn_rate * d_weights1
        self.weights2 -= self.learn_rate * d_weights2
