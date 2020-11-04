def get_moves(board):
    empty_slot = board.index(0)
    return moves[empty_slot](board)


def move(board, moving_tile, empty_tile):
    board[empty_tile] = board[moving_tile]
    board[moving_tile] = 0
    return board


def zero_moves(board):
    choices = {
        "left": {
            "cost": 1,
            "move": move(board, 1, 0)
        },
        "up": {
            "cost": 1,
            "move": move(board, 4, 0)
        },
        "around": {
            "cost": 2,
            "move": move(board, 3, 0)
        },
        "kitty": {
            "cost": 3,
            "move": move(board, 5, 0)
        },
        "diagonal": {
            "cost": 3,
            "move": move(board, 7, 0)
        }
    }
    return choices


def one_moves(board):
    choices = {
        "right": {
            "cost": 1,
            "move": move(board, 0, 1)
        },
        "left": {
            "cost": 1,
            "move": move(board, 2, 1)
        },
        "up": {
            "cost": 1,
            "move": move(board, 5, 1)
        }
    }
    return choices


def two_moves(board):
    choices = {
        "right": {
            "cost": 1,
            "move": move(board, 1, 2)
        },
        "left": {
            "cost": 1,
            "move": move(board, 3, 2)
        },
        "up": {
            "cost": 1,
            "move": move(board, 6, 2)
        }
    }
    return choices


def three_moves(board):
    choices = {
        "right": {
            "cost": 1,
            "move": move(board, 2, 3)
        },
        "up": {
            "cost": 1,
            "move": move(board, 7, 3)
        },
        "around": {
            "cost": 2,
            "move": move(board, 0, 3)
        },
        "kitty": {
            "cost": 3,
            "move": move(board, 6, 3)
        },
        "diagonal": {
            "cost": 3,
            "move": move(board, 4, 3)
        }
    }
    return choices


def four_moves(board):
    choices = {
        "down": {
            "cost": 1,
            "move": move(board, 0, 4)
        },
        "left": {
            "cost": 1,
            "move": move(board, 5, 4)
        },
        "around": {
            "cost": 2,
            "move": move(board, 7, 4)
        },
        "kitty": {
            "cost": 3,
            "move": move(board, 1, 4)
        },
        "diagonal": {
            "cost": 3,
            "move": move(board, 3, 4)
        }
    }
    return choices


def five_moves(board):
    choices = {
        "down": {
            "cost": 1,
            "move": move(board, 1, 5)
        },
        "right": {
            "cost": 1,
            "move": move(board, 4, 5)
        },
        "left": {
            "cost": 1,
            "move": move(board, 6, 5)
        }
    }
    return choices


def six_moves(board):
    choices = {
        "down": {
            "cost": 1,
            "move": move(board, 2, 6)
        },
        "right": {
            "cost": 1,
            "move": move(board, 5, 6)
        },
        "left": {
            "cost": 1,
            "move": move(board, 7, 6)
        }
    }
    return choices


def seven_moves(board):
    choices = {
        "down": {
            "cost": 1,
            "move": move(board, 3, 7)
        },
        "right": {
            "cost": 1,
            "move": move(board, 6, 7)
        },
        "around": {
            "cost": 2,
            "move": move(board, 4, 7)
        },
        "kitty": {
            "cost": 3,
            "move": move(board, 2, 7)
        },
        "diagonal": {
            "cost": 3,
            "move": move(board, 0, 7)
        }
    }
    return choices


moves = {
    0: zero_moves,
    1: one_moves,
    2: two_moves,
    3: three_moves,
    4: four_moves,
    5: five_moves,
    6: six_moves,
    7: seven_moves
}