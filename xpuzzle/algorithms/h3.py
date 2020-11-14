import numpy as np
import xpuzzle.algorithms.utility_functions as utility


def h3(board):
    solution_list = utility.get_solutions(board)
    sol_1 = solution_list[0]
    sol_2 = solution_list[1]

    max_row_len = board.shape[0]
    max_col_len = board.shape[1]

    max_row_pos = max_row_len - 1
    max_column_pos = max_col_len - 1

    # Goal 1
    # TR
    # What should be in the top right for goal 1
    good_tr = sol_1[0][max_column_pos]
    # But where is it?
    current_tr = np.asarray(np.where(board == good_tr)).T[0]
    current_tr_row_len = current_tr[0] + 1
    current_tr_column_len = current_tr[1] + 1

    # And what is the minimal cost to get it there for goal 1?
    tr_cost_1 = current_tr_row_len - 1 + max_col_len - current_tr_column_len

    # BL
    good_bl = sol_1[max_row_pos][0]
    # But where is it?
    current_bl = np.asarray(np.where(board == good_bl)).T[0]
    current_bl_row_len = current_bl[0] + 1
    current_bl_column_len = current_bl[1] + 1

    # And what is the minimal cost to get it there for goal 1?
    bl_cost_1 = max_row_len - current_bl_row_len + current_bl_column_len - 1

    cost_1 = tr_cost_1 + bl_cost_1

    # Goal 2
    # TR
    # What should be in the top right for goal 2
    good_tr = sol_2[0][max_column_pos]
    # But where is it?
    current_tr = np.asarray(np.where(board == good_tr)).T[0]
    current_tr_row_len = current_tr[0] + 1
    current_tr_column_len = current_tr[1] + 1

    # And what is the minimal cost to get it there for goal 2?
    tr_cost_2 = current_tr_row_len - 1 + max_col_len - current_tr_column_len

    # BL
    good_bl = sol_2[max_row_pos][0]
    # But where is it?
    current_bl = np.asarray(np.where(board == good_bl)).T[0]
    current_bl_row_len = current_bl[0] + 1
    current_bl_column_len = current_bl[1] + 1

    # And what is the minimal cost to get it there for goal 2?
    bl_cost_2 = max_row_len - current_bl_row_len + current_bl_column_len - 1

    cost_2 = tr_cost_2 + bl_cost_2

    if cost_1 > cost_2:
        return cost_2
    else:
        return cost_1
