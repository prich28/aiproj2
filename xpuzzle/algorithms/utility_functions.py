import numpy as np


def get_solutions(board):
    # The max array positions for rows and columns (used to identify type of position on the board
    rows = board.shape[0]
    columns = board.shape[1]
    solution_range = rows * columns
    solution1 = np.arange(1, solution_range + 1, 1, dtype=int).reshape(rows, columns)
    solution1[board.shape[0] - 1][board.shape[1] - 1] = 0

    solution2 = np.arange(1, solution_range + 1, 1, dtype=int).reshape(columns, rows)
    solution2 = np.transpose(solution2)
    solution2[board.shape[0] - 1][board.shape[1] - 1] = 0

    return[solution1, solution2]

