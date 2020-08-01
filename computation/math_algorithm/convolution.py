import numpy as np


def convolution(input_data, kernel):
    """
    Suppose we have two signals x and kernel, which are 2D arrays,
    with elements denoted as x[t][u] and so on. You can think of x as
    an input signal (such as a waveform or an image) and filter as
    a set of weights, which we’ll refer to as a filter or kernel.

    """
    # Format the inputs and kernel
    flipped_kernel = __flip(kernel)

    return __filter(input_data, flipped_kernel)


def __flip(x):
    """
    Rotate the 2D matrix x by 180 degrees
    """
    flipped_x = []
    for row_idx in range(len(x) - 1, -1, -1):
        flipped_x.append(x[row_idx][::-1])  # reverse the order

    return np.array(flipped_x)


def __filter(x, kernel):
    kernel_size = len(kernel)
    x_size = len(x)

    padding_size = kernel_size * 2 - 2  # padding of 0s in the matrix
    padded_x = np.zeros((x_size + padding_size, x_size + padding_size))

    # Last row/col number in padded_x that holds a non zero value
    edge_idx = x_size + padding_size - (kernel_size - 1)
    padded_x[kernel_size - 1: edge_idx, kernel_size - 1: edge_idx] = x

    # Run the filtering
    conv = []
    for row_idx in range(0, edge_idx):
        conv_row = []
        for col_idx in range(0, edge_idx):
            conv_row.append(
                np.sum(
                    padded_x[
                        row_idx: row_idx + kernel_size,
                        col_idx: col_idx + kernel_size,
                    ]
                    * kernel
                )
            )
        conv.append(conv_row)
    return np.array(conv)
