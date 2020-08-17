import numpy as np

from computation.machine_learning.activation_functions import (
    softmax,
    sigmoid_derivative,
)
from computation.math_algorithm.convolution import (
    add_padding_to_x,
    run_filters,
)


class ConvNetwork:
    def __init__(self, x, y, learn_rate=1):
        """
        Create a neural network with one conv layer followed by a pooling layer
        input -> conv -> pool -> output

        Each matrix has the following dimensions:
            Input Matrix: n x w x w x l
            Filter/Kernel: m x 3 x 3 x l  # must be odd
            Output Matrix: n x z

        Note: Size indicates the number of neural units at each layer

        Args:
            x (ndarray): n x w x w x l array where n is the number of training
                         examples and (w x w x l) is the size of a single input
            y (ndarray): n x z array where n is the number of training
                         examples and z is the number of categories
                         (probability of each category)
            learn_rate (float): learning rate of the neural network
        """
        self.input_layer_size = x.shape[1:]
        self.kernel_size = [2, 3, 3, self.input_layer_size[-1]]
        self.pool_size, self.stride = 2, 2
        self.pool_layer_width = int(
            (self.input_layer_size[0] - self.pool_size) / self.stride
        ) + 1
        self.output_layer_size = y.shape[1]

        self.input = x
        self.y = y
        self.kernel = np.random.rand(*self.kernel_size)
        self.activation = np.random.rand()

        self.output = np.zeros(self.y.shape)
        self.learn_rate = learn_rate
        self.weights = np.random.rand(
            self.pool_layer_width
            * self.pool_layer_width
            * self.kernel_size[0],
            self.output_layer_size
        )

    def feedforward(self):
        """
        Run forward propogation to calculate the probability of each test
        case representing each of the z categories
        """
        for idx in range(self.input.shape[0]):
            x = self.input[idx]
            self.output[idx] = self.predict(x)

    def backprop(self):
        """
        """
        for idx in range(self.input.shape[0]):
            # Find derivates for backpropogation
            d_output = -(
                (self.y[idx] - self.output[idx])  # n x 1
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

            # update the weights with the derivative (slope) of the loss
            # function
            self.weights1 -= self.learn_rate * d_weights1
            self.weights2 -= self.learn_rate * d_weights2

    def predict(self, x):
        padding = int((self.kernel.shape[1] - 1) / 2)
        padded_input = np.zeros((
            x.shape[0] + 2 * padding,
            x.shape[1] + 2 * padding,
            x.shape[2]
        ))

        # Add just enough 0 padding to the input such that the convolution
        # layer will be the same size as the input
        for feature_idx in range(x.shape[-1]):
            padded_input[:, :, feature_idx] = add_padding_to_x(
                x[:, :, feature_idx],
                padding
            )
        self.conv_layer = run_filters(padded_input, self.kernel)
        self.conv_layer[self.conv_layer <= 0] = 0  # RELU activation

        # shrink the information down to pick up on features and reduce
        # chance of overfitting
        pooled_layer = maxpool(
            self.conv_layer, self.pool_size, self.stride
        )

        reshaped_pool = pooled_layer.reshape(
            (
                1,
                self.pool_layer_width
                * self.pool_layer_width
                * self.kernel_size[0]
            )
        )

        return softmax(np.dot(reshaped_pool, self.weights))


def maxpool(x, size, stride):
    """
    Pooling operators consist of a fixed-shape window that is slid over
    all regions in the input according to its stride, computing a single
    output for each location traversed by the fixed-shape window
    (sometimes known as the pooling window).

    Pooling operators are deterministic, typically calculating either
    the maximum or the average value of the elements in the pooling window.

    Pooling serves the dual purposes of mitigating the sensitivity of
    convolutional layers to location and of spatially downsampling
    representations.

    Args:
        x (ndarray): tensor of a single input (w x w x l)
        size (int): size of the fixed-shaped window
        stride (int): determines how many units the fixed-shaped window
                        can slide over
    """
    (w, w, l) = x.shape
    pool = []
    for row_idx in range(0, w - size + 1, stride):
        pool_row = []
        for col_idx in range(0, w - size + 1, stride):
            # Get the max value within the window whose top-left corner
            # is located at (row_idx, col_idx, 0)
            pool_row.append(
                [
                    np.max(
                        x[
                            row_idx: row_idx + size,
                            col_idx: col_idx + size,
                            channel,
                        ]
                    )
                    for channel in range(0, l)
                ]
            )
        pool.append(pool_row)
    pool = np.array(pool)
    output_size = (w - size) / stride + 1
    if pool.shape != (output_size, output_size, l):
        raise Exception(
            "SOMETHING is wrong with max pool calculation. "
            + "This is a problem with this function"
        )
    return pool
