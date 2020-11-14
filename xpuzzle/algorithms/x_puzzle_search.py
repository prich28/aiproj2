import xpuzzle.game_rules as rules
from xpuzzle.algorithms.game_state import GameState


def is_node_on_list(node, list_to_check):
    is_on_list = False
    for list_node in list_to_check:
        if node.equals(list_node):
            is_on_list = True
    return is_on_list


def get_state_index(node, list_to_check) -> int:
    for index, item in enumerate(list_to_check):
        if node.equals(item):
            return index


class XPuzzleSearch:
    def __init__(self, initial_board, algorithm, heuristic):
        self.initial_node_state = GameState(initial_board, None, None)
        self.open_list = []

        # Sorting method based on Search Algorithm
        self.method = algorithm

        # Heuristic function
        self.heuristic = heuristic

        # search path
        self.closed_list = [self.initial_node_state]

    def sort_open_list(self, e):
        if self.method == "ucs":
            return e.get_g_cost()
        elif self.method == "gbfs":
            return e.get_h_cost()
        elif self.method == "astar":
            return e.get_f_cost()

    def run(self, stop):
        current_node_state = self.closed_list[-1]
        while not rules.is_goal(current_node_state.get_node()):
            if not stop():
                self.get_moves(current_node_state)
                self.make_next_move()
                current_node_state = self.closed_list[- 1]
            else:
                return None

        return self.get_solution_path()

    def get_moves(self, node_state):
        # get possible node moves
        next_moves = rules.get_moves(node_state.get_node()).values()

        # For each possible next move
        for next_move_state in next_moves:
            if next_move_state is not None:
                next_move_state.set_parent_state(node_state)
                # Get the node states and set the total actual* cost
                total_node_cost = next_move_state.get_move_cost() + node_state.get_g_cost()
                next_move_state.set_g_cost(total_node_cost)

                # Calculate heuristic if necessary
                if self.method == "gbfs" or self.method == "astar":
                    h_value = self.heuristic(next_move_state.get_node())
                    next_move_state.set_h_cost(h_value)

                # If using the a algorithm calculate f(n) cost
                if self.method == "astar":
                    next_move_state.compute_set_f_cost()

                if not is_node_on_list(next_move_state, self.closed_list):
                    if is_node_on_list(next_move_state, self.open_list):
                        open_node_state = self.open_list[get_state_index(next_move_state, self.open_list)]
                        if open_node_state.get_g_cost() > next_move_state.get_g_cost():
                            self.open_list.remove(open_node_state)
                            self.open_list.append(next_move_state)
                    else:
                        self.open_list.append(next_move_state)
                else:
                    # on closed list (for astar)
                    if self.method == "astar":
                        closed_node_state = self.closed_list[get_state_index(next_move_state, self.closed_list)]
                        if closed_node_state.get_f_cost() > next_move_state.get_f_cost():
                            self.closed_list.remove(closed_node_state)
                            self.open_list.append(next_move_state)

        self.open_list.sort(key=self.sort_open_list)

    def make_next_move(self):
        # check in open list for least cost move
        next_move_state = self.open_list[0]

        self.closed_list.append(next_move_state)
        self.open_list.remove(next_move_state)

    def get_solution_path(self):
        return self.closed_list
