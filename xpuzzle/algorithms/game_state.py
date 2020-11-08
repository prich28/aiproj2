import numpy as np


class GameState:
    def __init__(self, board, parent):
        self.__node = board
        self.__parent_node = parent
        self.__move_cost = 0
        self.__tile_moved = 0
        self.__total_cost = 0

    def get_node(self):
        return self.__node

    def set_node(self, board):
        self.__node = board

    def get_parent_node(self):
        return self.__parent_node

    def set_parent_node(self, parent):
        self.__parent_node = parent

    def get_move_cost(self):
        return self.__move_cost

    def set_move_cost(self, move_cost):
        self.__move_cost = move_cost

    def get_tile_moved(self):
        return self.__tile_moved

    def set_tile_moved(self, tile_moved):
        self.__tile_moved = tile_moved

    def get_total_cost(self):
        return self.__total_cost

    def set_total_cost(self, total_cost):
        self.__total_cost = total_cost

    def equals(self, game_state):
        return np.array_equal(self.__node, game_state.get_node())

    def parent_equals(self, game_state):
        return np.array_equal(self.__parent_node, game_state.get_node())
