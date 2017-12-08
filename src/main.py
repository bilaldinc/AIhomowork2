import random
import os
import sys
import math

args = sys.argv
if len(args) < 2:
    print("missing arguments")
    exit(1)

name_of_the_graph_file = args[1]
number_of_generations = int(args[2])
population_size = int(args[3])
crossover_probability = float(args[4])
mutation_probability = float(args[5])
initial_adding_probability = float(args[6])
temperature = float(args[7])
repair_function_type = int(args[8])


if temperature < -1:
    # proportional to size if negative
    temperature = population_size / -temperature
else:
    temperature = temperature

# enable logging experiments to files
enable_logging = 1

# enable stdout info
enable_stdout = 0


def main():
    # read file ------------------------------------------------------
    f = open(name_of_the_graph_file, 'r')
    lines = f.readlines()
    f.close()

    number_of_nodes = int(lines[0])
    adjacency_matrix = [[0 for x in range(number_of_nodes)] for y in range(number_of_nodes)]
    vertex_weights = [0.0 for x in range(number_of_nodes)]

    counter = 0
    for i in lines[2:]:
        if counter < number_of_nodes:
            split = i.split(" ")[1].replace(',', '.')
            vertex_weights[counter] = float(split)

        if counter >= number_of_nodes:
            split = i.split(" ")
            x = int(split[0])
            y = int(split[1])
            adjacency_matrix[x][y] = 1

        counter += 1

    logs_avg = number_of_generations * [None]
    logs_best = number_of_generations * [None]
    # ----------------------------------------------------------------

    # create initial population --------------------------------------
    population = []
    mating_pool = population_size * [None]
    for i in range(population_size):
        example_solution = [0 for x in range(number_of_nodes)]
        if initial_adding_probability is -1:
            # random
            cardinality_of_set = int(random.random() * number_of_nodes) + 1
            for j in random.sample(range(0, len(number_of_nodes)), cardinality_of_set):
                example_solution[j] = 1

        else:
            # biased random
            for j in range(number_of_nodes):
                if random.random() < initial_adding_probability:
                    example_solution[j] = 1
                else:
                    example_solution[j] = 0

        population.append(example_solution)

    fitness_values = [0.0 for x in range(population_size)]
    cumulative_probabilities = [0.0 for x in range(population_size)]
    probabilities = [0.0 for x in range(population_size)]
    # ----------------------------------------------------------------

    # O(|V| * population_size * population_size * number_of_generations)
    # O(|V| * |V| * population_size * number_of_generations)
    maximum_fitness = - 1.0
    best_solution = number_of_nodes * [None]
    for k in range(number_of_generations):
        # repair population ----------------------------------------------
        # O(|V| * |V| * population_size)
        for i in population:
            if repair_function_type == 0:
                repair_solution_0(i, adjacency_matrix)
            elif repair_function_type == 1:
                repair_solution_1(i, adjacency_matrix, vertex_weights)
            elif repair_function_type == 2:
                repair_solution_2(i, adjacency_matrix, vertex_weights)
            else:
                print("ops error")
                exit(1)
        # ----------------------------------------------------------------
        # evaluate fitness & selecting probabilities & find get best------
        # O(|V| * population_size)
        sum_of_fitness_values = 0
        sum_of_fitness_values_exp = 0
        for i in range(population_size):
            fitness_values[i] = calculate_fitness(population[i], vertex_weights)
            sum_of_fitness_values += fitness_values[i]
            if temperature >= 0:
                sum_of_fitness_values_exp += math.exp(fitness_values[i] / temperature)
        cumsum = 0
        cumsum_exp = 0
        current_best = -1.0
        for i in range(population_size):
            if temperature >= 0:
                probabilities[i] = math.exp(fitness_values[i] / temperature) / sum_of_fitness_values_exp
                cumsum_exp += math.exp(fitness_values[i] / temperature)
                cumulative_probabilities[i] = cumsum_exp / sum_of_fitness_values_exp
            else:
                cumsum += fitness_values[i]
                cumulative_probabilities[i] = cumsum / sum_of_fitness_values
            if fitness_values[i] > maximum_fitness:
                maximum_fitness = fitness_values[i]
                best_solution = population[i]
            if fitness_values[i] > current_best:
                current_best = fitness_values[i]
        # ----------------------------------------------------------------

        # print & log average---------------------------------------------
        average = sum_of_fitness_values / float(len(fitness_values))
        logs_avg[k] = str(average) + "\n"
        logs_best[k] = str(current_best) + "\n"
        if enable_stdout == 1:
            print("gen : " + str(k) + "  average : " + str(average) + "  best : " + str(current_best))
        # ----------------------------------------------------------------

        # create mating pool-----------------------------------------------
        # O(population_size * population_size * |V|)
        for i in range(population_size):
            random_number = random.random()
            for j in range(population_size):
                if random_number < cumulative_probabilities[j]:
                    mating_pool[i] = list(population[j])
                    break
        # ----------------------------------------------------------------

        # crossover ------------------------------------------------------
        # O(|V| * population_size)
        for i in range(0, population_size, 2):
            if crossover_probability < random.random():
                crossover(mating_pool[i], mating_pool[i + 1])
        # ----------------------------------------------------------------

        # mutation ------------------------------------------------------
        # O(|V| * population_size)
        for i in range(population_size):
            if mutation_probability < random.random():
                mutation(mating_pool[i])
        # ----------------------------------------------------------------

        # create new population one O(|V| * population_size)
        for i in range(population_size):
            population[i] = list(mating_pool[i])

    # logging the experiment
    input_file_name = os.path.basename(name_of_the_graph_file).split(".")[0]
    if enable_logging == 1:
        if not os.path.exists("../logs"):
            os.makedirs("../logs")
        if not os.path.exists("../logs/" + input_file_name):
            os.makedirs("../logs/" + input_file_name)

        if not os.path.exists("../logs/" + input_file_name + "/avg"):
            os.makedirs("../logs/" + input_file_name + "/avg")
        if not os.path.exists("../logs/" + input_file_name + "/best"):
            os.makedirs("../logs/" + input_file_name + "/best")
        if not os.path.exists("../logs/" + input_file_name + "/best-solution"):
            os.makedirs("../logs/" + input_file_name + "/best-solution")

        file_name = "../logs/" + input_file_name + "/" + "/avg/" + input_file_name + "_g" + str(
            number_of_generations) + "_p" + str(population_size) + "_c" + str(crossover_probability) + "_m" + str(
            mutation_probability) + "_ip" + str(initial_adding_probability) + "_rp" + str(
            repair_function_type) + "_tmp" + str(int(temperature)) + "_avg"
        f = open(file_name + ".csv", 'w')
        for i in logs_avg:
            f.write(i)
        f.close()

        file_name = "../logs/" + input_file_name + "/" + "/best/" + input_file_name + "_g" + str(
            number_of_generations) + "_p" + str(population_size) + "_c" + str(crossover_probability) + "_m" + str(
            mutation_probability) + "_ip" + str(initial_adding_probability) + "_rp" + str(
            repair_function_type) + "_tmp" + str(int(temperature)) + "_best"
        f = open(file_name + ".csv", 'w')
        for i in logs_best:
            f.write(i)
        f.close()

        file_name = "../logs/" + input_file_name + "/" + "/best-solution/" + input_file_name + "_g" + str(
            number_of_generations) + "_p" + str(population_size) + "_c" + str(crossover_probability) + "_m" + str(
            mutation_probability) + "_ip" + str(initial_adding_probability) + "_rp" + str(
            repair_function_type) + "_tmp" + str(int(temperature)) + "_best_solution"
        f = open(file_name + ".csv", 'w')
        f.write("maximum fitness : " + str(maximum_fitness) + "\n")
        for i in best_solution:
            f.write(str(i) + "\n")
        f.close()


def crossover(solution1, solution2):
    # O(|V|)
    length = len(solution1)
    point = int(random.random() * (length - 1)) + 1
    for i in range(length):
        if i < point:
            temp = solution1[i]
            solution1[i] = solution2[i]
            solution2[i] = temp


def mutation(solution):
    # O(|V|)
    for i in random.sample(range(0, len(solution)), 10):
        # flip
        solution[i] = 1 - solution[i]


def calculate_fitness(solution, vertex_weights):
    # O(|V|)
    summation = 0
    for i in range(len(solution)):
        summation += solution[i] * vertex_weights[i]
    return summation


def check_solution_validity(solution, adjacency_matrix):
    # O(|V| * |V|)
    result = True
    for i in range(len(solution)):
        if solution[i] == 1:
            for j in range(len(solution)):
                if solution[j] == 1:
                        if adjacency_matrix[i][j] == 1:
                            return False

    return result


def repair_solution_0(solution, adjacency_matrix):
    # O(|V| * |V|)
    total_removed_vertex = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            for j in range(len(solution)):
                if solution[j] == 1:
                        if adjacency_matrix[i][j] == 1:
                            solution[i] = 0
                            total_removed_vertex += 1
                            break
    return total_removed_vertex


def repair_solution_1(solution, adjacency_matrix, vertex_weights):
    # Nodes are removed greedly according to number of edges
    # O(|V| * |V|)
    length = len(solution)
    number_of_connections = [0 for x in  range(length)]
    inner_adjacency_matrix = [[0 for x in range(length)] for y in range(length)]
    valid_solution = True
    total_removed_vertex = 0
    # O(|V| * |V|)
    for i in range(length):
        if solution[i] == 1:
            for j in range(length):
                if solution[j] == 1:
                    if adjacency_matrix[i][j] == 1:
                        valid_solution = False
                        number_of_connections[i] += 1
                        inner_adjacency_matrix[i][j] = 1

    # O(|V| * |V|)
    while not valid_solution:
        # find max gain
        # O(|V|)
        max_edge = 0
        max_edge_i = -1
        valid_solution = True
        for i in range(length):
            if number_of_connections[i] > 0:
                valid_solution = False
                if number_of_connections[i] >= max_edge:
                    max_edge = number_of_connections[i]
                    max_edge_i = i

        # remove vertex from solution etc.
        # O(|V|)
        if max_edge_i is not -1:
            solution[max_edge_i] = 0
            number_of_connections[max_edge_i] = 0
            total_removed_vertex += 1
            for i in range(length):
                if inner_adjacency_matrix[i][max_edge_i] is not 0:
                    inner_adjacency_matrix[i][max_edge_i] = 0
                    number_of_connections[i] -= 1
            for i in range(length):
                inner_adjacency_matrix[max_edge_i][i] = 0

    return total_removed_vertex


def repair_solution_2(solution, adjacency_matrix, vertex_weights):
    # Nodes are removed greedly according to gain value
    # Gain value for vertex x = (sum of weights of all vertexes that has edge with x)  -  (weight of x)
    # After every removal gains are recalculated.
    # O(|V| * |V|)
    length = len(solution)
    number_of_connections = [0 for x in  range(length)]
    gain = [0.0 for x in range(len(solution))]
    inner_adjacency_matrix = [[0 for x in range(length)] for y in range(length)]
    valid_solution = True
    total_removed_vertex = 0
    # O(|V| * |V|)
    for i in range(length):
        if solution[i] == 1:
            gain[i] = - vertex_weights[i]
            for j in range(length):
                if solution[j] == 1:
                    if adjacency_matrix[i][j] == 1:
                        valid_solution = False
                        number_of_connections[i] += 1
                        gain[i] += vertex_weights[j]
                        inner_adjacency_matrix[i][j] = 1

    # O(|V| * |V|)
    while not valid_solution:
        # find max gain
        # O(|V|)
        max_gain = 0
        max_gain_i = -1
        valid_solution = True
        for i in range(length):
            if number_of_connections[i] > 0:
                valid_solution = False
                # there are many arithmetic operation is performed on gain and floating point numbers are not ...
                # ... commutative. Initial equality may have been violated
                if gain[i] >= max_gain or (abs(gain[i] - max_gain) < 0.001):
                    max_gain = gain[i]
                    max_gain_i = i

        # don't erase this control
        if (max_gain_i is -1) and (valid_solution is False):
            print("stop ! ERROR")

        # remove vertex from solution recalculate gain etc.
        # O(|V|)
        if max_gain_i is not -1:
            solution[max_gain_i] = 0
            gain[max_gain_i] = -vertex_weights[max_gain_i]
            number_of_connections[max_gain_i] = 0
            total_removed_vertex += 1
            for i in range(length):
                if inner_adjacency_matrix[i][max_gain_i] is not 0:
                    inner_adjacency_matrix[i][max_gain_i] = 0
                    number_of_connections[i] -= 1
                    gain[i] -= vertex_weights[max_gain_i]
            for i in range(length):
                inner_adjacency_matrix[max_gain_i][i] = 0

    return total_removed_vertex


main()
