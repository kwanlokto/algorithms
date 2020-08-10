import string

import numpy as np

from computation.genetic_algorithm.build_quote.population import Population
from computation.machine_learning.models.multilayer_perceptron import MLP

if __name__ == "__main__":
    # Genetic algorithm to reconstruct 'testing'
    quote = "testing"
    new_population = Population(10, quote)
    traits = {i: string.ascii_lowercase for i in range(len(quote))}
    new_population.create_new_population(traits)

    for _ in range(1000):
        new_population.natural_selection()
        new_population.next_generation(0.10)
    print(new_population.get_most_fit_dna())

    # Learn XOR function
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    nn = MLP(x, y)

    i = 0
    while i < 100000:
        i += 1
        nn.feedforward()
        nn.backprop()
    print(nn.output)
