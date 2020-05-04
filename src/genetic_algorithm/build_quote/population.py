import math
from random import choice

from src.genetic_algorithm.base_population import BasePopulation
from src.genetic_algorithm.build_quote.DNA import DNA


class Population(BasePopulation):
    def __init__(self, size, target):
        super().__init__(DNA, size, target)
        self.perfect_score = 1

    def natural_selection(self):
        self.mating_pool = []
        max_fitness = max([dna.fitness for dna in self.population])

        # Based on fitness, each member will get added to the population
        #   - Higher fitness -> more children
        #   - Lower fitness -> less children
        for dna in self.population:
            # Arbitratrary multiply for monte carlo method
            num_partners = (
                math.ceil(dna.fitness / max_fitness * 100)
                if max_fitness > 0
                else 1
            )

            # TODO: want to copy the dna so we don't mutate the object
            self.mating_pool.extend([dna for _ in range(num_partners)])

    def next_generation(self, mutation_rate=0):
        """
        Replace the current generation of DNA with their children
        """
        next_generation = []
        for _ in range(self.size):
            p1 = choice(self.mating_pool)
            p2 = choice(self.mating_pool)
            child = DNA.cross_over([p1, p2], self.target)
            child.mutate(mutation_rate)

            next_generation.append(child)
        self.population = next_generation

    @property
    def is_done(self):
        best = self.get_most_fit_dna()
        return self.perfect_score == best.fitness
