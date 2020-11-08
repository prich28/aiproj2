import numpy as np


class GameState:
    def __init__(self, board, parent):
        self.__node = board
        self.__parent_node = parent
        self.__move_cost = 0
        self.__tile_moved = 0
        self.__g_cost = 0
        self.__h_cost = 0
        self.__f_cost = 0

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
        return self.__g_cost

    def set_total_cost(self, total_cost):
        self.__g_cost = total_cost

    def get_h_cost(self):
        return self.__h_cost

    def set_h_cost(self, cost):
        self.__h_cost = cost

    def set_g_h_f_cost(self, g, h):
        self.set_total_cost(g)
        self.set_h_cost(h)
        self.compute_set_f_cost()

    def get_f_cost(self):
        return self.__f_cost

    def set_f_cost(self, cost):
        self.__f_cost = cost

    def set_f_cost_with_g_h(self, g_cost, h_cost):
        self.__f_cost = g_cost + h_cost

    def compute_set_f_cost(self):
        self.__f_cost = self.__h_cost + self.__g_cost

    def equals(self, game_state):
        return np.array_equal(self.__node, game_state.get_node())

    def parent_equals(self, game_state):
        return np.array_equal(self.__parent_node, game_state.get_node())
