import subprocess

names_of_the_graph_file = ["003.txt", "015.txt", "030.txt"]
number_of_generations = [50, 200, 400]
population_sizes = [100, 200]
crossover_probabilities = [0.6, 0.9]
mutation_probabilities = [0.2, 0.02]

maximum_concurrent_process = 30
processes = []

for i in names_of_the_graph_file:
    for j in number_of_generations:
        for k in population_sizes:
            for l in crossover_probabilities:
                for m in mutation_probabilities:
                    args = ["python3", "main.py", i, j, k, l, m]
                    processes.append(subprocess.Popen(args))
                    while len(processes) > maximum_concurrent_process:
                        for n in processes:
                            poll = n.poll()
                            if poll is not None:
                                processes.remove(n)
                                break

