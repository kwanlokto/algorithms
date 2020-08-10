import unittest

import numpy as np

from computation.machine_learning.models.multilayer_perceptron import MLP


class TestConvolution(unittest.TestCase):
    def setUp(self):
        x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([[0], [1], [1], [0]])
        self.mlp = MLP(x, y)

        # Zero out the weights so testing is consistent
        self.mlp.weights1 *= 0
        self.mlp.weights2 *= 0

    def test_predict(self):
        input_data = np.array([[1, 0]])

        hidden, result = self.mlp.predict(input_data)

        assert type(hidden) == np.ndarray
        assert type(result) == np.ndarray
        self.assertListEqual(
            result.tolist(), [[0.5]],
        )
        self.assertListEqual(hidden.tolist(), [[0.5, 0.5, 0.5, 0.5]])

    def test_feedforward(self):
        self.mlp.weights1 += 1
        self.mlp.weights2 += 0.5

        self.mlp.feedforward()

        # Testing forward feed
        assert type(self.mlp.hidden_layer) == np.ndarray
        assert type(self.mlp.output) == np.ndarray
        self.assertListEqual(
            self.mlp.output.tolist(),
            [
                [0.7310585786300049],
                [0.8118562749129378],
                [0.8118562749129378],
                [0.8534092045709026],
            ],
        )
        self.assertListEqual(
            self.mlp.hidden_layer.tolist(),
            [
                [0.5, 0.5, 0.5, 0.5],
                [
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                ],
                [
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                ],
                [
                    0.8807970779778823,
                    0.8807970779778823,
                    0.8807970779778823,
                    0.8807970779778823,
                ],
            ],
        )

    def test_backpropogation(self):
        # setup
        self.mlp.hidden_layer = np.array(
            [
                [0.5, 0.5, 0.5, 0.5],
                [
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                ],
                [
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                    0.7310585786300049,
                ],
                [
                    0.8807970779778823,
                    0.8807970779778823,
                    0.8807970779778823,
                    0.8807970779778823,
                ],
            ]
        )
        self.mlp.output = np.array(
            [
                [0.7310585786300049],
                [0.8118562749129378],
                [0.8118562749129378],
                [0.8534092045709026],
            ]
        )
        self.mlp.backprop()

        self.assertListEqual(
            self.mlp.weights1.tolist(),
            [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
        )

        self.assertListEqual(
            self.mlp.weights2.tolist(),
            [
                [-0.12388555892117109],
                [-0.12388555892117109],
                [-0.12388555892117109],
                [-0.12388555892117109],
            ],
        )
