from xpuzzle.algorithms.game_state import GameState
import numpy as np

goal1 = [[1, 2, 3, 4], [5, 6, 7, 0]]

goal2 = [[1, 3, 5, 7], [2, 4, 6, 0]]


def is_goal(board):
    print(board)
    return np.array_equal(goal1, board) or np.array_equal(goal2, board)


def get_move_state(board, moving_position, empty_position, move_cost):
    new_board = move(board, moving_position, empty_position)
    node = GameState(new_board, board)
    node.set_move_cost(move_cost)
    # Old empty position is contains the tile that was just moved
    node.set_tile_moved(new_board[empty_position[0]][empty_position[1]])
    return node


def move(board, moving_position, empty_position):
    altered_board = np.copy(board)
    altered_board[empty_position[0]][empty_position[1]] = altered_board[moving_position[0]][moving_position[1]]
    altered_board[moving_position[0]][moving_position[1]] = 0
    return altered_board


def get_moves(board):
    # Empty spot is an array of 2 values indicating the position of the empty space in 2d array
    empty_slot = np.asarray(np.where(board == 0)).T[0]

    # The max array positions for rows and columns (used to identify type of position on the board
    max_row_pos = board.shape[0] - 1
    max_column_pos = board.shape[1] - 1

    # Is empty spot a corner?
    if((empty_slot[0] == max_row_pos) or (empty_slot[0] == 0)) and\
            ((empty_slot[1] == max_column_pos) or (empty_slot[1] == 0)):
        # If true, get all possible moves
        return get_corner_moves(board, empty_slot, max_row_pos, max_column_pos)

    # Is empty spot a side
    # (logic: if it was not a corner, at least one of the values of the tuple must be an edge)
    elif(empty_slot[0] == max_row_pos) or (empty_slot[0] == 0) or\
            (empty_slot[1] == max_column_pos) or (empty_slot[1] == 0):
        # If true get all possible moves
        return get_edge_moves(board, empty_slot, max_row_pos, max_column_pos)

    # Is empty spot in the middle
    # (logic: if you are here it did not qualify as corner or edge
    else:
        # If true get all possible moves
        get_interior_moves(board, empty_slot)


def get_corner_moves(board, empty_slot, max_row_pos, max_column_pos):
    # Top left
    if np.array_equal(empty_slot, [0, 0]):
        return get_top_left_corner_moves(board, empty_slot, max_row_pos, max_column_pos)

    # Top right
    elif np.array_equal(empty_slot, [0, max_column_pos]):
        return get_top_right_corner_moves(board, empty_slot, max_row_pos)

    # Bottom left
    elif np.array_equal(empty_slot, [max_row_pos, 0]):
        return get_bottom_left_corner_moves(board, empty_slot, max_column_pos)

    # Bottom right
    elif np.array_equal(empty_slot, [max_row_pos, max_column_pos]):
        return get_bottom_right_corner_moves(board, empty_slot)


def get_edge_moves(board, empty_slot, max_row_pos, max_column_pos):
    # NO WRAPPING on edge pieces
    # Top Edge
    if empty_slot[0] == 0:
        return get_top_edge_moves(board, empty_slot)

    # Bottom Edge
    elif empty_slot[0] == max_row_pos:
        return get_bottom_edge_moves(board, empty_slot)

    # Left Edge
    elif empty_slot[1] == 0:
        return get_left_edge_moves(board, empty_slot)

    # Right Edge
    elif empty_slot[1] == max_column_pos:
        return get_right_edge_moves(board, empty_slot)


def get_interior_moves(board, empty_slot):
    return {
        "up": get_up(board, empty_slot),
        "down": get_down(board, empty_slot),
        "left": get_left(board, empty_slot),
        "right": get_right(board, empty_slot)
    }


def get_top_left_corner_moves(board, empty_slot, max_row_pos, max_column_pos):
    # up
    up = get_up(board, empty_slot)

    # left
    left = get_left(board, empty_slot)

    # around vertical
    around_v = None
    if not empty_slot[0] + 1 == max_row_pos:
        moving_position = [max_row_pos, empty_slot[1]]
        around_v = get_move_state(board, moving_position, empty_slot, 2)

    # around horizontal
    around_h = None
    if not empty_slot[1] + 1 == max_column_pos:
        moving_position = [empty_slot[0], max_column_pos]
        around_h = get_move_state(board, moving_position, empty_slot, 2)

    # kitty
    moving_position = [empty_slot[0] + 1, empty_slot[1] + 1]
    kitty = get_move_state(board, moving_position, empty_slot, 3)

    # diagonal
    moving_position = [max_row_pos, max_column_pos]
    diagonal = get_move_state(board, moving_position, empty_slot, 3)

    return {
        "up": up,
        "left": left,
        "kitty": kitty,
        "around_v": around_v,
        "around_h": around_h,
        "diagonal": diagonal
    }


def get_top_right_corner_moves(board, empty_slot, max_row_pos):
    # up
    up = get_up(board, empty_slot)

    # right
    right = get_right(board, empty_slot)

    # around vertical
    around_v = None
    if not empty_slot[0] + 1 == max_row_pos:
        moving_position = [max_row_pos, empty_slot[1]]
        around_v = get_move_state(board, moving_position, empty_slot, 2)

    # around horizontal
    around_h = None
    if not empty_slot[1] - 1 == 0:
        moving_position = [empty_slot[0], 0]
        around_h = get_move_state(board, moving_position, empty_slot, 2)

    # kitty
    moving_position = [empty_slot[0] + 1, empty_slot[1] - 1]
    kitty = get_move_state(board, moving_position, empty_slot, 3)

    # diagonal
    moving_position = [max_row_pos, 0]
    diagonal = get_move_state(board, moving_position, empty_slot, 3)

    return {
        "up": up,
        "right": right,
        "kitty": kitty,
        "around_v": around_v,
        "around_h": around_h,
        "diagonal": diagonal
    }


def get_bottom_left_corner_moves(board, empty_slot, max_column_pos):
    # down
    down = get_down(board, empty_slot)

    # left
    left = get_left(board, empty_slot)

    # around vertical
    around_v = None
    if not empty_slot[0] - 1 == 0:
        moving_position = [0, empty_slot[1]]
        around_v = get_move_state(board, moving_position, empty_slot, 2)

    # around horizontal
    around_h = None
    if not empty_slot[1] + 1 == max_column_pos:
        moving_position = [empty_slot[0], max_column_pos]
        around_h = get_move_state(board, moving_position, empty_slot, 2)

    # kitty
    moving_position = [empty_slot[0] - 1, empty_slot[1] + 1]
    kitty = get_move_state(board, moving_position, empty_slot, 3)

    # diagonal
    moving_position = [0, max_column_pos]
    diagonal = get_move_state(board, moving_position, empty_slot, 3)

    return {
        "down": down,
        "left": left,
        "kitty": kitty,
        "around_v": around_v,
        "around_h": around_h,
        "diagonal": diagonal
    }


def get_bottom_right_corner_moves(board, empty_slot):
    # down
    down = get_down(board, empty_slot)

    # right
    right = get_right(board, empty_slot)

    # around vertical
    around_v = None
    if not empty_slot[0] - 1 == 0:
        moving_position = [0, empty_slot[1]]
        around_v = get_move_state(board, moving_position, empty_slot, 2)

    # around horizontal
    around_h = None
    if not empty_slot[1] - 1 == 0:
        moving_position = [empty_slot[0], 0]
        around_h = get_move_state(board, moving_position, empty_slot, 2)

    # kitty
    moving_position = [empty_slot[0] - 1, empty_slot[1] - 1]
    kitty = get_move_state(board, moving_position, empty_slot, 3)

    # diagonal
    moving_position = [0, 0]
    diagonal = get_move_state(board, moving_position, empty_slot, 3)

    return {
        "down": down,
        "right": right,
        "kitty": kitty,
        "around_v": around_v,
        "around_h": around_h,
        "diagonal": diagonal
    }


def get_top_edge_moves(board, empty_slot):
    # up
    up = get_up(board, empty_slot)
    # left
    left = get_left(board, empty_slot)
    # right
    right = get_right(board, empty_slot)

    return {
        "up": up,
        "left": left,
        "right": right
    }


def get_bottom_edge_moves(board, empty_slot):
    # down
    down = get_down(board, empty_slot)
    # left
    left = get_left(board, empty_slot)
    # right
    right = get_right(board, empty_slot)

    return {
        "down": down,
        "left": left,
        "right": right
    }


def get_left_edge_moves(board, empty_slot):
    # up
    up = get_up(board, empty_slot)
    # down
    down = get_down(board, empty_slot)
    # right
    right = get_right(board, empty_slot)

    return {
        "up": up,
        "down": down,
        "right": right
    }


def get_right_edge_moves(board, empty_slot):
    # up
    up = get_up(board, empty_slot)
    # down
    down = get_down(board, empty_slot)
    # left
    left = get_left(board, empty_slot)

    return {
        "up": up,
        "down": down,
        "left": left
    }


def get_up(board, empty_slot):
    moving_position = [empty_slot[0] + 1, empty_slot[1]]
    return get_move_state(board, moving_position, empty_slot, 1)


def get_right(board, empty_slot):
    moving_position = [empty_slot[0], empty_slot[1] - 1]
    return get_move_state(board, moving_position, empty_slot, 1)


def get_left(board, empty_slot):
    moving_position = [empty_slot[0], empty_slot[1] + 1]
    return get_move_state(board, moving_position, empty_slot, 1)


def get_down(board, empty_slot):
    moving_position = [empty_slot[0] - 1, empty_slot[1]]
    return get_move_state(board, moving_position, empty_slot, 1)
