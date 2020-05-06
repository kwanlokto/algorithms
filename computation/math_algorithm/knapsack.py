def regular_knapsack(bag_size, items):
    """
    Maximize total value when only taking 'bag_size' items from 'items'

    OPT(i) = max()
    Args:
        bag_size (int): number of items which we can carry
        items (list): the value of each associated item
    Returns:
        list: indices of items which will maximize value
    """
    bag_size += 1
    values = [
        [[] for _ in range(bag_size)] for _ in range(len(items))
    ]  # The best value after taking i items

    for item_num in range(len(items)):
        for items_taken in range(1, bag_size):
            total = sum_by_idx(items, values[item_num - 1][items_taken])

            new_total = (  # assume weight 1
                sum_by_idx(
                    items, values[item_num - 1][items_taken - 1]
                )
                + items[item_num]
            )

            # OPT[i][j] = max(OPT[i-1][j-1] + val[i], OPT[i-1][j])
            if total < new_total:
                values[item_num][items_taken] = values[item_num - 1][
                    items_taken - 1
                ] + [item_num]
            else:
                values[item_num][items_taken] = values[item_num - 1][
                    items_taken
                ]
    return values[-1][-1]  # only bc weight is 1


def sum_by_idx(array, indices):
    total = 0
    for idx in indices:
        total += array[idx]
    return total
