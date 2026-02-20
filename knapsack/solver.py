#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])


def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')
    n, capacity = (int(token) for token in lines[0].split())  # 0..(n-1)

    if capacity > 100000 and n > 30:
        return solve_it_greedy(input_data)

    values = [0] * (n+1)
    weights = [0] * (n+1)

    for i in range(1, n+1):
        line = lines[i]
        parts = line.split()
        values[i] = int(parts[0])
        weights[i] = int(parts[1])

    # Build table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight = weights[i]
        value = values[i]
        for c in range(1, capacity + 1):
            # Not taken item i
            dp[i][c] = dp[i-1][c]
            # Take item i
            if weight <= c:
                dp[i][c] = max(dp[i][c], dp[i-1][c-weight] + value)

    max_value = dp[n][capacity]

    # Reconstruct chosen items
    taken = [0] * (n + 1)  # 0 .. n
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:  # item i wak taken
            taken[i] = 1
            w -= weights[i]

    # prepare the solution in the specified output format
    output_data = str(max_value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken[1:]))
    return output_data


def solve_it_greedy(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0] * len(items)

    # sort by density
    items.sort(key=lambda x: x.value / x.weight, reverse=True)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

