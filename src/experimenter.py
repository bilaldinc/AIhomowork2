import subprocess

names_of_the_graph_file = ["../inputs/030.txt"]
number_of_generations = ["400"]
population_sizes = ["200"]
crossover_probabilities = ["0.6", "0.9"]
mutation_probabilities = ["0.2", "0.02"]
initial_adding_probabilities = ["0.025", "0.05", "0.3", "0.5", "1"]
temperature = ["-1", "0.5", "0.6", "0.7", "0.8", "1", "-2", "-3"]  # - means divide to pop size ,-1 means use old method
repair_function_types = ["2"]


# probabilities are exponentially weighted according to formula below
# P(i) = e^(f_i/temperature) / Σ_j e^(f_j / temperature)
# f_i = fitness value of an individual in the population
# as temperature goes to infinity distribution goes to uniform
# as temperature goes to zero distribution goes to greedy
# where the temperature equals to number of element in the population. it is almost same as tournament selection


total_number_of_process = len(number_of_generations) * len(population_sizes) * \
                          len(crossover_probabilities) * len(mutation_probabilities) * \
                          len(initial_adding_probabilities) * len(temperature) *\
                          len(repair_function_types) * len(names_of_the_graph_file)

maximum_concurrent_process = 35
created_processes_counter = 0

processes = []
processes_wait = []

for i in names_of_the_graph_file:
    for j in number_of_generations:
        for k in population_sizes:
            for l in crossover_probabilities:
                for m in mutation_probabilities:
                    for n in initial_adding_probabilities:
                        for o in temperature:
                            for p in repair_function_types:
                                args = ["python3", "main.py", i, j, k, l, m, n, o, p]
                                process = subprocess.Popen(args)
                                created_processes_counter += 1
                                print(str(created_processes_counter) + " process is created out of " + str(total_number_of_process))
                                processes.append(process)
                                processes_wait.append(process)
                                while len(processes) > maximum_concurrent_process:
                                    for r in processes:
                                        poll = r.poll()
                                        if poll is not None:
                                            processes.remove(r)
                                            break


print("last " + str(maximum_concurrent_process) + "processes")

for i in processes_wait:
    i.wait()

print("experiment is ended successfully")
