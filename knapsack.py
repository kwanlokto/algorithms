import numpy as np
import random

def regular_knapsack(bag_size, items):
    """
    Maximize total value when only taking 'bag_size' items from 'items'

    Args:
        bag_size (int): number of items which we can carry
        items (list): the value of each associated item
    Returns:
        list: indices of items which will maximize value
    """
    bag_size += 1 
    values = [[] for _ in range(bag_size)]  # The best value after taking i items where i is index in the array
    
    for item_num in range(0, len(items)):
        for items_taken in range(bag_size - 1, 0, -1):  # Reverse order so we don't double add
            total = sum_by_idx(items, values[items_taken])
            new_total = sum_by_idx(items, values[items_taken - 1]) + items[item_num]
            if total < new_total:
                values[items_taken] = values[items_taken - 1] + [item_num]
                
    return values[-1]


def sum_by_idx(array, indices):
    total = 0
    for idx in indices:
        total += array[idx]
    return total

array = [90, 20, 30, 40, 50, 60, 70, 80, 90]
print(regular_knapsack(2, array))