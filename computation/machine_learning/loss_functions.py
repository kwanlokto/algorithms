import numpy as np


def zero_one_loss(exp_val, true_val):
    return 0 if exp_val == true_val else 1


def hinge_loss(exp_val, true_val):
    # Good for SVM
    return max(0, 1 - exp_val * true_val)


def squared_error(exp_val, true_val):
    return 0.5 * (exp_val - true_val) ** 2


def cross_entropy_loss(exp_val, true_val):
    """
    Best loss function that allows gradient descent to be efficient
    and correct

    Args:
        exp_val (float): target associated with the training input
        true_val (float): value retrieved from model
    Returns:
        float: total cross-entropy loss for the current model and data
    """
    return np.log(exp_val) if true_val == 1 else np.log(1 - exp_val)


def logistic_cross_entropy_loss(exp_val, true_val):
    """
    Combination of the logistic function (sigma) and cross-entropy loss

    sigma of a large negative number is approx 0 and computer may round
    this expected value to 0. The log(0) is negative infinity

    Args:
        exp_val (float): target associated with the training input
        true_val (float): value retrieved from model
    Returns:
        float: total logistic cross-entropy loss for the current model
               and data
    """
    return true_val * np.logaddexp(0, -exp_val) + (
        1 - true_val
    ) * np.logaddexp(0, exp_val)
