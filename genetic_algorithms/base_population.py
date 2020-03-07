from copy import deepcopy
from random import choice, random

from genetic_algorithms.base_DNA import BaseDNA
from genetic_algorithms.base_trait import BaseTrait


class BasePopulation:
    def __init__(self, DNA: BaseDNA, size: int, target):
        self.population = []
        self.DNA = DNA
        self.target = target
        self.size = size
        self.mating_pool = []

    def __repr__(self):
        return "\n".join([repr(dna) for dna in self.population])

    def create_new_population(self, traits: dict):
        """
        Randomly generate self.size traits from traits

        Args:
            traits (dict): All traits in this population
                {
                    trait_id: [list of possible options for that trait]
                    trait_id: None  # indicates trait should have value betweeen 0 and 1
                    ...
                }
        """
        self.population = [
            self.DNA([
                BaseTrait(trait_id, traits[trait_id])
                for trait_id in traits
            ], self.target)
            for _ in range(self.size)
        ]

    def get_population(self) -> list:
        """
        Get a copy of the population

        Returns:
            List: List of all DNA strands
        """
        return deepcopy(self.population)

    # TODO: something isn't working
    def get_most_fit_dna(self) -> BaseDNA:
        """
        Get the most fit dna from the population
        """
        prev_fitness = -1
        most_fit_dna = None
        for dna in self.population:
            if dna.fitness > prev_fitness:
                prev_fitness = dna.fitness
                most_fit_dna = dna
        return most_fit_dna

    def natural_selection(self):
        """
        Update mating_pool list of DNA after one iteration of natural selection
            - Selects the 'most' fit DNA
        """
        pass

    def mutation(self, mutation_rate: float):
        """
        Mutate every DNA in the population with probability 'mutation_rate'

        Args:
            mutation_rate (float): Probability of a DNA mutating
        """
        self.population = [
            dna.mutate(mutation_rate) for dna in self.population
        ]
