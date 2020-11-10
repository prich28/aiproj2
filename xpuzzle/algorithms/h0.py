import numpy as np


def h0(board):
    # Empty spot is an array of 2 values indicating the position of the empty space in 2d array
    empty_slot = np.asarray(np.where(board == 0)).T[0]

    # The max array positions for rows and columns (used to identify type of position on the board
    max_row_pos = board.shape[0] - 1
    max_column_pos = board.shape[1] - 1
    if empty_slot[0] == max_row_pos and empty_slot[1] == max_column_pos:
        return 0
    else:
        return 1
