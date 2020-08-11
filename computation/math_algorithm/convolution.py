import numpy as np


def convolution(input_data, kernel):
    """
    Suppose we have two signals x and kernel, which are 2D arrays,
    with elements denoted as x[t][u] and so on. You can think of x as
    an input signal (such as a waveform or an image) and filter as
    a set of weights, which we’ll refer to as a filter or kernel.

    """
    # Format the inputs and kernel
    flipped_kernel = _flip(kernel)

    padded_x = add_padding_to_x(input_data, len(kernel) - 1)
    return filter_2D(padded_x, flipped_kernel)


def add_padding_to_x(x, padding_size):
    x_size = len(x)
    padded_x = np.zeros(
        (x_size + padding_size * 2, x_size + padding_size * 2)
    )

    # Last row/col number in padded_x that holds a non zero value
    edge_idx = x_size + padding_size
    padded_x[padding_size:edge_idx, padding_size:edge_idx] = x
    return np.array(padded_x)


def _flip(x):
    """
    Rotate the 2D matrix x by 180 degrees

    Args:
        x (ndarray): 2D square matrix
    Return:
        ndarray: rotated matrix
    """
    flipped_x = []
    for row_idx in range(len(x) - 1, -1, -1):
        flipped_x.append(x[row_idx][::-1])  # reverse the order

    return np.array(flipped_x)


def filter_2D(x, kernel):
    """
    Apply the filter operation: x * kernel where x and kernel
    are 2D square matrices and kernel.shape < x.shape

    Args:
        x (ndarray): w x w square matrix
        kernel (ndarray): f x f square kernel
    """
    kernel_size = len(kernel)
    edge_idx = len(x) - (kernel_size - 1)

    # Run the filtering
    conv = []
    for row_idx in range(0, edge_idx):
        conv_row = []
        for col_idx in range(0, edge_idx):
            conv_row.append(
                np.sum(
                    x[
                        row_idx: row_idx + kernel_size,
                        col_idx: col_idx + kernel_size,
                    ]
                    * kernel
                )
            )
        conv.append(conv_row)
    return np.array(conv)


def filter_3D(x, kernel):
    """
    Apply the filter operation: x * kernel where x and kernel
    are 3D square matrices and kernel.shape < x.shape

    Args:
        x (ndarray): w x w x l square matrix
        kernel (ndarray): f x f x l square kernel
    """
    if x.shape[-1] != kernel.shape[-1]:
        raise Exception(
            "Error: Number of channels in both "
            + "image and filter must match."
        )

    return np.sum(
        [
            filter_2D(x[:, :, filter_num], kernel[:, :, filter_num])
            for filter_num in range(0, kernel.shape[-1])
        ]
    )


def run_filters(x, kernels):
    """
    Checking if there are mutliple channels for the single filter.
    If so, then each channel will convolve the image.
    The result of all convolutions are summed to return a single feature map.

    Args:
        x (ndarray): w x w (x l) square matrix
        kernel (ndarray): m x f x f (x l) square kernel
    """
    # Check that the input is correct format
    if kernels.shape[1] != kernels.shape[2]:
        raise Exception(
            "Error: The kernel must have a matching number "
            + "of rows and columns"
        )

    feature_maps = np.zeros(
        (
            x.shape[0] - kernels.shape[1] + 1,
            x.shape[1] - kernels.shape[1] + 1,
            kernels.shape[0],
        )
    )
    # Convolving the image by the filter(s).
    for kernel_num in range(kernels.shape[0]):
        curr_kernel = kernels[
            kernel_num, :
        ]  # getting a filter from the bank.
        if len(curr_kernel.shape) == 3:
            conv_map = filter_3D(x, curr_kernel)
        elif len(curr_kernel.shape) == 2:
            # only one channel in the filter.
            conv_map = filter_2D(x, curr_kernel)
        else:
            raise Exception("Error: Kernel tensor can only be 2D/3D")
        feature_maps[:, :, kernel_num] = conv_map
    return feature_maps  # Returning all feature maps.
