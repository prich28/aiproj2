from xpuzzle.algorithms.x_puzzle_search import XPuzzleSearch
import numpy as np
from xpuzzle.algorithms.h1 import h1
from xpuzzle.algorithms.h2 import h2
from xpuzzle.algorithms.h0 import h0
import time
import queue
from threading import Thread
import os
import errno
import sys


def generate_puzzle_board(input_list, width):
    try:
        return np.reshape(input_list, (-1, width))
    except:
        sys.exit("Your puzzle dimensions don't seem to be correct!")


def generate_x_puzzle_game(board, method, h):
    return XPuzzleSearch(board, method, h)


def run(sol_q, algo, stop):
    start = time.time()
    solution = algo.run(stop)
    end = time.time()
    duration = end - start
    sol_q.put([solution, duration])


def print_solution_path(puzzle_num, info, method, h):
    len_sol = 0
    num = str(puzzle_num)
    dir_path = "solutions/"
    puzzle_dir_path = dir_path + num + "/"

    if h is None:
        file_path = puzzle_dir_path + num + "_" + method + "_" + "solution.txt"
    else:
        file_path = puzzle_dir_path + num + "_" + method + "-" + h + "_" + "solution.txt"

    if not os.path.exists(os.path.dirname(dir_path)):
        try:
            os.mkdir(dir_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if not os.path.exists(os.path.dirname(puzzle_dir_path)):
        try:
            os.mkdir(puzzle_dir_path)
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
            len_sol += 1
            backtrack_node = backtrack_node.get_parent_state()

        # Starting node
        tile_cost = str(backtrack_node.get_tile_moved()) + " " + str(backtrack_node.get_move_cost()) + " "
        output_string = tile_cost + " ".join(map(str, backtrack_node.get_node().flatten())) + "\n" + output_string
        len_sol += 1

        with open(file_path, "w") as solution_file:
            solution_file.write(output_string)
            solution_file.write(str(total_path_cost) + " " + str(round(duration, 1)))

    return len_sol


def print_search_path(puzzle_num, info, method, h):
    len_search = 0
    num = str(puzzle_num)
    dir_path = "solutions/"
    puzzle_dir_path = dir_path + num + "/"

    if h is None:
        file_path = puzzle_dir_path + num + "_" + method + "_" + "search.txt"
    else:
        file_path = puzzle_dir_path + num + "_" + method + "-" + h + "_" + "search.txt"

    if not os.path.exists(os.path.dirname(dir_path)):
        try:
            os.mkdir(dir_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if not os.path.exists(os.path.dirname(puzzle_dir_path)):
        try:
            os.mkdir(puzzle_dir_path)
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
            len_search += 1
            backtrack_node = closed_list.pop()

        # Starting node
        tile_cost = str(backtrack_node.get_f_cost()) + " " + \
                    str(backtrack_node.get_g_cost()) + " " + \
                    str(backtrack_node.get_h_cost()) + " "

        output_string = tile_cost + " ".join(map(str, backtrack_node.get_node().flatten())) + "\n" + output_string
        len_search += 1
        with open(file_path, "w") as solution_file:
            solution_file.write(output_string)

    return len_search


def print_stats_file(method, h, len_sol, len_search, no_sol, t_cost, exec_time, num_puzzles, ind_sol_paths, ind_search_paths, ind_costs, ind_exec_times):
    dir_path = "stats/"
    if method == "ucs":
        global_stats_file_path = dir_path + method + ".txt"
        all_sol_paths_file_path = dir_path + method + "_sol_paths.txt"
        all_search_paths_file_path = dir_path + method + "_search_paths.txt"
        all_costs_file_path = dir_path + method + "_all_costs.txt"
        all_exec_times_file_path = dir_path + method + "_all_exec_times.txt"
    else:
        global_stats_file_path = dir_path + method + "-" + h + ".txt"
        all_sol_paths_file_path = dir_path + method + "-" + h + "_sol_paths.txt"
        all_search_paths_file_path = dir_path + method + "-" + h + "_search_paths.txt"
        all_costs_file_path = dir_path + method + "-" + h + "_all_costs.txt"
        all_exec_times_file_path = dir_path + method + "-" + h + "_all_exec_times.txt"

    if not os.path.exists(os.path.dirname(dir_path)):
        try:
            os.mkdir(dir_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if (num_puzzles - no_sol) == 0:
        avg_len_sol_path = 0
        avg_len_search_path = 0
        avg_total_cost = 0
    else:
        avg_len_sol_path = len_sol / (num_puzzles - no_sol)
        avg_len_search_path = len_search / (num_puzzles - no_sol)
        avg_total_cost = t_cost / (num_puzzles - no_sol)

    avg_no_sol = no_sol / num_puzzles * 100
    avg_exec_time = exec_time / num_puzzles

    with open(global_stats_file_path, "w") as stats_file:
        stats_file.write("Average solution length: " + str(round(avg_len_sol_path, 2)) + "\n")
        stats_file.write("Average search length: " + str(round(avg_len_search_path, 2)) + "\n")
        stats_file.write("Number of 'no solutions': " + str(no_sol) + "\n")
        stats_file.write("Proportion of 'no solutions': " + str(round(avg_no_sol, 2)) + "%\n")
        stats_file.write("Average total cost: " + str(round(avg_total_cost, 2)) + "\n")
        stats_file.write("Average execution time: " + str(round(avg_exec_time, 2)) + "\n")

    with open(all_sol_paths_file_path, "w") as ind_sol_file:
        ind_sol_file.write(method + " ")
        if h is not None:
            ind_sol_file.write(h)
        ind_sol_file.write("\n")
        ind_sol_file.write(",".join(map(str, ind_sol_paths)))

    with open(all_search_paths_file_path, "w") as ind_search_file:
        ind_search_file.write(method + " ")
        if h is not None:
            ind_search_file.write(h)
        ind_search_file.write("\n")
        ind_search_file.write(",".join(map(str, ind_search_paths)))

    with open(all_costs_file_path, "w") as ind_costs_file:
        ind_costs_file.write(method + " ")
        if h is not None:
            ind_costs_file.write(h)
        ind_costs_file.write("\n")
        ind_costs = np.around(ind_costs, decimals=2)
        ind_costs_file.write(",".join(map(str, ind_costs)))

    with open(all_exec_times_file_path, "w") as ind_times_file:
        ind_times_file.write(method + " ")
        if h is not None:
            ind_times_file.write(h)
        ind_times_file.write("\n")
        ind_exec_times = np.around(ind_exec_times, decimals=2)
        ind_times_file.write(",".join(map(str, ind_exec_times)))


def output_to_file(puzzle_num, info, method, h):
    len_sol = print_solution_path(puzzle_num, info, method, h)
    len_search = print_search_path(puzzle_num, info, method, h)

    return [len_sol, len_search]


#######################################
# THE PROJECT STARTS RUNNING FROM HERE
#######################################

# for stats values
len_search_path = 0
total_cost = 0
execution_time = 0
num_no_sol = 0
len_sol_path = 0

ind_sol_path_count = []
ind_search_path_count = []
ind_total_costs = []
ind_execution_times = []

chosen_method = ""
chosen_h = ""

while chosen_method != "astar" and chosen_method != "ucs" and chosen_method != "gbfs":
    chosen_method = input("Chose an algorithm (ucs, gbfs, astar): ")

if chosen_method != "ucs":
    while chosen_h != "h0" and chosen_h != "h1" and chosen_h != "h2":
        chosen_h = input("Chose a heuristic (h0, h1, h2): ")

puzzle_width = input("Set the puzzle width (number): ")
puzzle_input = input("Set the name of the puzzles file: ")
print("Make sure the puzzles you put in " + puzzle_input + " have the right amount of numbers to fill the board!")

# Get initial state
with open(puzzle_input, "r") as puzzle_file:
    # Get the puzzle board with the correct dimensions for the game
    puzzles = np.genfromtxt(puzzle_file, dtype='int', delimiter=" ")

for index, puzzle in enumerate(puzzles):
    puzzle_board = generate_puzzle_board(puzzle, int(puzzle_width))

    print(index)
    print(puzzle_board)
    game = None
    if chosen_method == "ucs":
        game = generate_x_puzzle_game(puzzle_board, chosen_method, None)
        chosen_h = None
    elif chosen_method == "gbfs" or chosen_method == "astar":
        if chosen_h == "h1":
            game = generate_x_puzzle_game(puzzle_board, chosen_method, h1)
        elif chosen_h == "h2":
            game = generate_x_puzzle_game(puzzle_board, chosen_method, h2)
        elif chosen_h == "h0":
            game = generate_x_puzzle_game(puzzle_board, chosen_method, h0)
    q = queue.Queue()
    stop_threads = False
    t = Thread(target=run, args=(q, game, lambda: stop_threads,))
    t.start()
    timer = 0
    to_print = None

    while timer <= 58 and q.empty():
        time.sleep(1)
        timer += 1

    if timer >= 58:
        stop_threads = True

    t.join()
    to_print = q.get()

    sol_closed_list = to_print[0]

    if sol_closed_list is None:
        num_no_sol += 1
        ind_total_costs.append(0)
    else:
        ind_total_costs.append(sol_closed_list[-1].get_g_cost())
        total_cost += sol_closed_list[-1].get_g_cost()

    len_sol_search = output_to_file(index, to_print, chosen_method, chosen_h)

    ind_sol_path_count.append(len_sol_search[0])
    ind_search_path_count.append(len_sol_search[1])
    len_sol_path += len_sol_search[0]
    len_search_path += len_sol_search[1]
    ind_execution_times.append(to_print[1])
    execution_time += to_print[1]

# Print the statistics files
print_stats_file(chosen_method, chosen_h, len_sol_path, len_search_path, num_no_sol, total_cost, execution_time,
                 len(puzzles), ind_sol_path_count, ind_search_path_count, ind_total_costs, ind_execution_times)



