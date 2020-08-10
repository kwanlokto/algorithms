import numpy as np


def sigmoid(z):
    """
    Non linear function to squash predictions between 0 and 1
    Positive large val -> 1
    Negative large val -> 0

    Args:
        z (float): prediction (arbitrary real value) that will be squashed
    Returns
        float: prediction between 0 and 1
    """
    return 1 / (1 + np.exp(-z))


def sigmoid_derivative(z):
    return z * (1 - z)


def softmax(z):
    """
    Multivariate generalization of the logistic function.
    Importantly, the outpust of hte softmax function are nonnegative and
    sum to 1, so they can be interpreted as a probability distribution
    over |z| clases
    Args:
        z (ndarray): vector predictions (logits) to squash between
                     0 and 1
    Returns:
        ndarray: vector predictions between 0 and 1
    """
    prediction = np.e ** z
    return prediction / np.sum(prediction)  # Normalize the prediction
