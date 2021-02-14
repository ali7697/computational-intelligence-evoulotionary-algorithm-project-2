import random
import math
import statistics

import numpy as np


num_initial_generation = 100000
num_iterations = 50
global_min = -959.6407
prob_recombination = 0.4
learning_rate_sigma = 0.8 
alpha_recombination = 0.4


# The encoding is in this format: first x1 and then x2 and then the sigma
encodings = []

# calculate the fitness of a point
def calFitness(x):
    f_value = -(x[1] + 47) * math.sin(math.sqrt(abs(x[1] + x[0] / 2 + 47))) - x[0] * math.sin(
        math.sqrt(abs(x[0] - (x[1] + 47))))
    calculated_fitness = 10 / (abs(f_value - global_min)+0.01)
    return calculated_fitness

# Initializing the population
for i in range(num_initial_generation):
    encode = []
    encode = random.sample(range(-512, 512), 2)

    # important part. not sure if I'm doing this right
    encode.append(random.sample(range(10), 1)[0])
    # encode.append(random.random())
    encodings.append(encode)

# iterations
for it in range(num_iterations):
    children = []
    # mutating
    fitness = []
    children_fitness = []
    for index in range(num_initial_generation):
        x = encodings[index]
        # mutating the step size
        x[2] = x[2] * math.exp(-(learning_rate_sigma * random.random()))
        # mutating the genes
        x[0] = x[0] + x[2] * random.random()
        x[1] = x[1] + x[2] * random.random()

    #  recombination (it should produce 7 times the initial generation)
    for pairing in range(7 * (num_initial_generation // 2)):
        #  using alpha each pair of parents produces two children
        #  but if alpha is 0.5 then each pair produces one child
        parent1 = random.sample(encodings, 1)[0]
        parent2 = random.sample(encodings, 1)[0]
        child1 = []
        child2 = []
        if random.random() < alpha_recombination:
            child1.append(alpha_recombination * parent1[0] + (1 - alpha_recombination) * parent2[0])
            child2.append((1 - alpha_recombination) * parent1[0] + alpha_recombination * parent2[0])
            child1.append(alpha_recombination * parent1[1] + (1 - alpha_recombination) * parent2[1])
            child2.append((1 - alpha_recombination) * parent1[1] + alpha_recombination * parent2[1])
            child1.append(parent1[2])
            child2.append(parent2[2])
            children_fitness.append(calFitness(child1))
            children_fitness.append(calFitness(child2))
            children.append(child1)
            children.append(child2)
        else:
            children.append(parent1)
            children.append(parent2)
            children_fitness.append(calFitness(parent1))
            children_fitness.append(calFitness(parent2))

    # Choosing the survivors lets do mu and lambda
    # selection phase
    sum_fitness = sum(children_fitness)
    picking_probs = children_fitness.copy()
    for i in range(len(children_fitness)):
        picking_probs[i] = children_fitness[i] / sum_fitness
    encodings_key_indexes = np.random.choice(range(7*num_initial_generation),
                                             num_initial_generation, False, picking_probs)
    encodings = []
    fitness = []
    for ind in encodings_key_indexes:
        encodings.append(children[ind])
        fitness.append(children_fitness[ind])
    sum_average_dif = 0
    for i in fitness:
        sum_average_dif = sum_average_dif + 1/i
    print(it)
    print("average: ", statistics.mean(fitness))
    print("Max: ", max(fitness))
    print("Min: ", min(fitness))



print("\n")
j = fitness.index(max(fitness))
print(encodings[j])
x = encodings[j]
f_value = -(x[1] + 47) * math.sin(math.sqrt(abs(x[1] + x[0] / 2 + 47))) - x[0] * math.sin(
        math.sqrt(abs(x[0] - (x[1] + 47))))
print(f_value)
print(1/max(fitness))
