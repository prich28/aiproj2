from xpuzzle.algorithms.x_puzzle_search import XPuzzleSearch
import numpy as np
from xpuzzle.algorithms.h1 import h1
import time
import queue
from threading import Thread
import os
import errno

# Get initial state
with open("puzzles.txt", "r") as puzzle_file:
    puzzles = np.genfromtxt(puzzle_file, dtype='int', delimiter=" ")


def fill_2_by_4(input_list):
    return np.array([[input_list[0], input_list[1], input_list[2], input_list[3]],
                     [input_list[4], input_list[5], input_list[6], input_list[7]]], dtype=int)


# def fill_3_by_3(input_list):
#     return np.array([[input_list[0], input_list[1], input_list[2]],
#                     [input_list[3], input_list[4], input_list[5]],
#                     [input_list[6], input_list[7], input_list[8]]])


def generate_x_puzzle_game(board, method, h):
    return XPuzzleSearch(board, method, h)


def run(sol_q, algo, stop):
    start = time.time()
    solution = algo.run(stop)
    end = time.time()
    duration = end - start
    sol_q.put([solution, duration])


def print_solution_path(puzzle_num, info, method, h):
    num = str(puzzle_num)
    dir_path = "solutions/" + num + "/"
    file_path = dir_path
    if h is None:
        file_path = file_path + num + "_" + method + "_" + "solution.txt"
    else:
        file_path = file_path + num + "_" + method + "-" + h + "_" + "solution.txt"

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.mkdir(dir_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    closed_list = info[0]

    if closed_list is None:
        with open(file_path, "w") as solution_file:
            solution_file.write("no solution" + "\n")
    else:
        duration = info[1]
        backtrack_node = closed_list[-1]
        total_path_cost = backtrack_node.get_g_cost()
        output_string = ""
        while backtrack_node.get_parent_state() is not None:
            flat_board = backtrack_node.get_node().flatten()
            tile_cost = str(backtrack_node.get_tile_moved()) + " " + str(backtrack_node.get_move_cost()) + " "

            puzzle_string = " ".join(map(str, flat_board)) + "\n"

            output_string = tile_cost + puzzle_string + output_string
            backtrack_node = backtrack_node.get_parent_state()

        # Starting node
        tile_cost = str(backtrack_node.get_tile_moved()) + " " + str(backtrack_node.get_move_cost()) + " "
        output_string = tile_cost + " ".join(map(str, backtrack_node.get_node().flatten())) + "\n" + output_string

        with open(file_path, "w") as solution_file:
            solution_file.write(output_string)
            solution_file.write(str(total_path_cost) + " " + str(round(duration, 1)))


def print_search_path(puzzle_num, info, method, h):
    num = str(puzzle_num)
    dir_path = "solutions/" + num + "/"
    file_path = dir_path
    if h is None:
        file_path = file_path + num + "_" + method + "_" + "search.txt"
    else:
        file_path = file_path + num + "_" + method + "-" + h + "_" + "search.txt"

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.mkdir(dir_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    closed_list = info[0]

    if closed_list is None:
        with open(file_path, "w") as solution_file:
            solution_file.write("no solution" + "\n")
    else:
        backtrack_node = closed_list.pop()
        output_string = ""
        while backtrack_node.get_parent_state() is not None:
            flat_board = backtrack_node.get_node().flatten()
            tile_cost = str(backtrack_node.get_f_cost()) + " " + \
                        str(backtrack_node.get_g_cost()) + " " + \
                        str(backtrack_node.get_h_cost()) + " "

            puzzle_string = " ".join(map(str, flat_board)) + "\n"

            output_string = tile_cost + puzzle_string + output_string
            backtrack_node = closed_list.pop()

        # Starting node
        tile_cost = str(backtrack_node.get_f_cost()) + " " + \
                    str(backtrack_node.get_g_cost()) + " " + \
                    str(backtrack_node.get_h_cost()) + " "

        output_string = tile_cost + " ".join(map(str, backtrack_node.get_node().flatten())) + "\n" + output_string

        with open(file_path, "w") as solution_file:
            solution_file.write(output_string)


def output_to_file(puzzle_num, info, method, h):
    print_solution_path(puzzle_num, info, method, h)
    print_search_path(puzzle_num, info, method, h)


#######################################
# THE PROJECT STARTS RUNNING FROM HERE
#######################################


chosen_method = "astar"
chosen_h = "h1"

for index, puzzle in enumerate(puzzles):
    print(index)
    print(puzzle)
    puzzle_board = fill_2_by_4(puzzle)
    print(puzzle_board)
    if chosen_method == "ucs":
        game = generate_x_puzzle_game(puzzle_board, chosen_method, None)
        chosen_h = None
    elif chosen_method == "gbfs" or chosen_method == "astar":
        if chosen_h == "h1":
            game = generate_x_puzzle_game(puzzle_board, chosen_method, h1)
        elif chosen_h == "h1":
            game = generate_x_puzzle_game(puzzle_board, chosen_method, h1)
    q = queue.Queue()
    stop_threads = False
    t = Thread(target=run, args=(q, game, lambda: stop_threads,))
    t.start()
    timer = 0
    to_print = None

    while timer != 60 and q.empty():
        time.sleep(.1)
        timer += .1

    if timer >= 60:
        stop_threads = True

    t.join()
    to_print = q.get()
    print(to_print[1])
    output_to_file(index, to_print, chosen_method, chosen_h)
