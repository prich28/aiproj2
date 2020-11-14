import numpy as np
import xpuzzle.algorithms.utility_functions as utility


def h2(board):
    solution_list = utility.get_solutions(board)
    sol_1 = solution_list[0]
    sol_2 = solution_list[1]

    goal_1_total = pieces_cost(board, sol_1)

    goal_2_total = pieces_cost(board, sol_2)

    if goal_1_total < goal_2_total:
        return goal_1_total
    else:
        return goal_2_total


def pieces_cost(board, sol):
    max_row_len = board.shape[0]
    max_col_len = board.shape[1]

    solution_total = 0
    # What should be in each position
    for r_index in range(max_row_len):
        for c_index in range(max_col_len):
            expected_number = sol[r_index][c_index]
            if not expected_number == 0:
                if board[r_index][c_index] != expected_number:
                    # But where is it?
                    current_location = np.asarray(np.where(board == expected_number)).T[0]
                    current_loc_row_len = current_location[0] + 1
                    current_loc_column_len = current_location[1] + 1
                    # cost to get it there abs(row diff) + abs(column diff)
                    solution_total += abs((r_index + 1) - current_loc_row_len) + abs((c_index + 1) - current_loc_column_len)

    return solution_total
