import random

name_of_the_graph_file = "../inputs/003.txt"
number_of_generations = 5
population_size = 200
crossover_probability = 0.6
mutation_probability = 0.02
log = 1



def main():
    print("hello world")

    # read file ------------------------------------------------------
    f = open(name_of_the_graph_file, 'r')
    lines = f.readlines()
    f.close()

    number_of_nodes = int(lines[0])
    adjacency_matrix = [[0 for x in range(number_of_nodes)] for y in range(number_of_nodes)]
    vertex_weights = [0 for x in range(number_of_nodes)]

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

    logs = number_of_generations * [None]
    # ----------------------------------------------------------------

    # create initial population --------------------------------------
    population = []
    mating_pool = population_size * [None]
    for i in range(population_size):
        example_solution = []
        for j in range(number_of_nodes):
            example_solution.append(int(random.random() * 2))
        population.append(example_solution)

    fitness_values = [0.0 for x in range(population_size)]
    cumulative_probabilities = [0.0 for x in range(population_size)]
    # ----------------------------------------------------------------

    # O(|V| * population_size * population_size * number_of_generations)
    # O(|V| * |V| * population_size * number_of_generations)
    maximum_fitness = - 1.0
    best_solution = number_of_nodes * [None]
    for k in range(number_of_generations):
        # repair population ----------------------------------------------
        # O(|V| * |V| * population_size)
        for i in population:
            repair_solution(i, adjacency_matrix)
        # ----------------------------------------------------------------

        # evaluate fitness & selecting probabilities & find get best------
        # O(|V| * population_size)
        sum_of_fitness_values = 0
        for i in range(population_size):
            fitness_values[i] = calculate_fitness(population[i], vertex_weights)
            sum_of_fitness_values += fitness_values[i]
        cumsum = 0
        current_best = -1.0
        for i in range(population_size):
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
        logs[k] = str(average) + "," + str(current_best) + "\n"
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
    if log == 1:
        file_name = name_of_the_graph_file + "_g" + str(number_of_generations) + "_p" + str(population_size) + "_c" + str(crossover_probability) + "_m" + str(mutation_probability)
        f = open(file_name + ".csv", 'w')
        for i in logs:
            f.write(i)
        f.close()

        f = open(file_name + "_best" + ".csv", 'w')
        f.write("maximum fitness : " + str(maximum_fitness) + "\n")
        for i in best_solution:
            f.write(str(i) + "\n")
        f.close()


def repair_solution(solution, adjacency_matrix):
    # O(|V| * |V|)
    for i in range(len(solution)):
        if solution[i] == 1:
            for j in range(len(solution)):
                if solution[j] == 1:
                        if adjacency_matrix[i][j] == 1:
                            solution[i] = 0
                            break


def repair_solution_2(solution, adjacency_matrix):
    # O(|V| * |V|)
    for i in range(len(solution)):
        if solution[i] == 1:
            for j in range(len(solution)):
                if solution[j] == 1:
                        if adjacency_matrix[i][j] == 1:
                            solution[i] = 0
                            break


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


main()
