import unittest
import numpy as np
from computation.math_algorithm.convolution import convolution


class TestConvolution(unittest.TestCase):
    def test_convolution(self):
        input_data = [[1, 3, 1], [0, -1, 1], [2, 2, -1]]
        kernel = [[1, 2], [0, -1]]
        conv = convolution(input_data, kernel)

        assert type(conv) == np.ndarray
        self.assertListEqual(
            conv.tolist(),
            [
                [1, 5, 7, 2],
                [0, -2, -4, 1],
                [2, 6, 4, -3],
                [0, -2, -2, 1],
            ],
        )
