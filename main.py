from xpuzzle.algorithms.x_puzzle_search import XPuzzleSearch
import numpy as np


# Get initial state


# play game until solution or 60 seconds

def fill_2_by_4(input_list):
    return np.array([[input_list[0], input_list[1], input_list[2], input_list[3]],
                     [input_list[4], input_list[5], input_list[6], input_list[7]]], dtype=int)


board = fill_2_by_4([0, 1, 2, 3, 4, 5, 6, 7])

ucs = XPuzzleSearch(board, "ucs")
solution = ucs.run()
