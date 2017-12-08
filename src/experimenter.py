import subprocess

names_of_the_graph_file = ["../inputs/003.txt", "../inputs/015.txt", "../inputs/030.txt"]
number_of_generations = ["50", "200", "400"]
population_sizes = ["100", "200"]
crossover_probabilities = ["0.6", "0.9"]
mutation_probabilities = ["0.2", "0.02"]

total_number_of_process = len(number_of_generations) * len(population_sizes) * len(crossover_probabilities) * \
                          len(mutation_probabilities) * len(names_of_the_graph_file)


maximum_concurrent_process = 50
created_processes_counter = 0

processes = []
processes_wait = []

for i in names_of_the_graph_file:
    for j in number_of_generations:
        for k in population_sizes:
            for l in crossover_probabilities:
                for m in mutation_probabilities:
                    args = ["python", "main.py", i, j, k, l, m]
                    process = subprocess.Popen(args)
                    created_processes_counter += 1
                    print(str(created_processes_counter) + " process is created out of " + str(total_number_of_process))
                    processes.append(process)
                    processes_wait.append(process)
                    while len(processes) > maximum_concurrent_process:
                        for n in processes:
                            poll = n.poll()
                            if poll is not None:
                                processes.remove(n)
                                break


print("last " + str(maximum_concurrent_process) + "processes")

for i in processes_wait:
    i.wait()
