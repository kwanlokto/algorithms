import unittest
from unittest.mock import patch
import numpy as np

from computation.math_algorithm.convolution import (
    filter_2D,
    _flip,
    add_padding_to_x,
    convolution,
    run_filters,
)


class TestConvolution(unittest.TestCase):
    def test_convolution(self):
        input_data = [[1, 3, 1], [0, -1, 1], [2, 2, -1]]
        kernel = [[1, 2], [0, -1]]
        conv = convolution(input_data, kernel)

        assert type(conv) == np.ndarray
        self.assertListEqual(
            conv.tolist(),
            [[1, 5, 7, 2], [0, -2, -4, 1], [2, 6, 4, -3], [0, -2, -2, 1]],
        )

    def test_flip(self):
        kernel = np.array([[1, 2], [0, -1]])
        result = _flip(kernel)

        assert type(result) == np.ndarray
        self.assertListEqual(
            result.tolist(), [[-1, 0], [2, 1]],
        )

    def test_add_padding_to_x(self):
        x = [[1, 3, 1], [0, -1, 1], [2, 2, -1]]
        result = add_padding_to_x(x, 2)

        assert type(result) == np.ndarray
        self.assertListEqual(
            result.tolist(),
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 3, 1, 0, 0],
                [0, 0, 0, -1, 1, 0, 0],
                [0, 0, 2, 2, -1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
        )

    def test_filter_2D(self):
        input_data = np.array([[1, 3, 1], [0, -1, 1], [2, 2, -1]])
        kernel = np.array([[-1, 0], [2, 1]])
        result = filter_2D(input_data, kernel)

        assert type(result) == np.ndarray
        self.assertListEqual(
            result.tolist(), [[-2, -4], [6, 4]],
        )

    def test_filter_3D(self):
        input_data = np.array(
            [
                [[1, 1], [3, 1], [1, 1]],
                [[0, 1], [-1, 1], [1, 1]],
                [[2, 1], [2, 1], [-1, 1]],
            ]
        )
        kernel = np.array([[[-1, 1], [0, 1]], [[2, 1], [1, 1]]])
        result = filter_2D(input_data, kernel)

        assert type(result) == np.ndarray
        self.assertListEqual(
            result.tolist(), [[2, 0], [10, 8]],
        )

    @patch("computation.math_algorithm.convolution.filter_3D")
    def test_run_filters(self, mock_filter_3D):
        mock_filter_3D.side_effect = [
            [[0, 1], [2, 3]],
            [[4, 5], [6, 7]],
        ]
        x = np.ones((3, 3, 2))
        kernels = np.ones((2, 2, 2, 2))
        result = run_filters(x, kernels)

        assert type(result) == np.ndarray

        self.assertListEqual(
            result.tolist(),
            [[[0.0, 4.0], [1.0, 5.0]], [[2.0, 6.0], [3.0, 7.0]]],
        )
