import unittest
from unittest.mock import patch
import numpy as np

from computation.machine_learning.models.conv_network import maxpool


class TestConvolution(unittest.TestCase):
    def test_convolution(self):
        input_data = np.array(
            [
                [[0, 2], [1, 1], [3, 0]],
                [[0, 0], [-1, 0], [1, 0]],
                [[2, 0], [2, 10], [-1, 0]],
            ]
        )
        result = maxpool(input_data, 2, 1)

        assert type(result) == np.ndarray
        self.assertListEqual(
            result.tolist(), [[[1, 2], [3, 1]], [[2, 10], [2, 10]]],
        )
