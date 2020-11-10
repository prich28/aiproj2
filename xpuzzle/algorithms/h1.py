import xpuzzle.algorithms.utility_functions as utility


def h1(board):
    solution_list = utility.get_solutions(board)
    sol_1 = solution_list[0].flatten()
    sol_2 = solution_list[1].flatten()

    # For every wrong tile add a cost of 1 (for each board)
    board_solution = board.flatten()

    cost_sol_1 = 0
    cost_sol_2 = 0
    for i in range(len(board_solution)):
        if board_solution[i] != sol_1[i] and board_solution[i] != 0:
            cost_sol_1 = cost_sol_1 + 1

    for i in range(len(board_solution)):
        if board_solution[i] != sol_2[i] and board_solution[i] != 0:
            cost_sol_2 = cost_sol_2 + 1

    if cost_sol_1 <= cost_sol_2:
        return cost_sol_1
    else:
        return cost_sol_2
