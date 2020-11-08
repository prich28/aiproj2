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
    def __init__(self, initial_board, algorithm):
        self.initial_node_state = GameState(initial_board, None)
        self.open_list = []

        # Sorting method based on Search Algorithm
        self.method = algorithm

        # search path
        self.closed_list = [self.initial_node_state]

        # cost
        self.total_cost = 0

    def sort_open_list(self, e):
        if self.method == "ucs":
            return e.get_total_cost()
        elif self.method == "gbfs":
            return e.get_h_cost()
        elif self.method == "a":
            return e.get_f_cost()

    def run(self):
        current_node_state = self.closed_list[- 1]
        while not rules.is_goal(current_node_state.get_node()):
            self.get_moves(current_node_state)
            self.make_next_move()
            current_node_state = self.closed_list[- 1]

        return {
            "totalCost": self.total_cost,
            "solutionPath": self.get_solution_path()
        }

    def get_moves(self, node_state):
        # get possible node moves
        next_moves = rules.get_moves(node_state.get_node()).values()

        # For each possible next move
        for next_move_state in next_moves:
            if next_move_state is not None:
                # Get the node states and set the total cost
                total_node_cost = next_move_state.get_move_cost() + self.total_cost
                next_move_state.set_total_cost(total_node_cost)

                if not is_node_on_list(next_move_state, self.closed_list):
                    if is_node_on_list(next_move_state, self.open_list):
                        open_node_state = self.open_list[get_state_index(next_move_state, self.open_list)]
                        if open_node_state.get_total_cost() > next_move_state.get_total_cost():
                            self.open_list.remove(open_node_state)
                            self.open_list.append(next_move_state)
                    else:
                        self.open_list.append(next_move_state)

        self.open_list.sort(key=self.sort_open_list)

    def make_next_move(self):
        # check in open list for least cost move
        next_move_state = self.open_list[0]

        self.closed_list.append(next_move_state)
        self.open_list.remove(next_move_state)
        self.total_cost = self.total_cost + next_move_state.get_move_cost()

    def get_solution_path(self):
        return self.closed_list
