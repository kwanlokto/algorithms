import math
from random import choice, random
from string import ascii_letters

from genetic_algorithms.base_DNA import BaseDNA


class DNA(BaseDNA):
    def mutate(self, mutation_rate: float):
        for char_idx in range(self.size):
            if random() < mutation_rate:
                self.traits[char_idx].randomly_set_value()

    @property
    def fitness(self):
        score = 0
        for char_idx in range(self.size):
            current_char = self.traits[char_idx]
            target_char = self.target[char_idx]
            if current_char.get_value() == target_char:
                score += 1
        return score / len(self.target)

    def __repr__(self):
        phrase = [
            trait.get_value() for trait in self.get_dna()
        ]  # just get the character
        return "DNA: " + "".join(phrase)

    @classmethod
    def cross_over(cls, parents: list, target):
        """
        Define how a new child is generated from parents
            - Used to pass down 'successful' traits

        Args:
            parent (list): List of DNA objects which have traits 
                           that the new child should have
        """
        parents_traits = zip(*[
            [trait.get_id() for trait in parent.get_dna()]
            for parent in parents
        ])

        if all([len(set(trait_id)) != 1 for trait_id in parents_traits]):
            raise Exception(
                "Number of traits for each parent must be the same")

        child_traits = []
        for p_idx in range(len(parents)):
            traits = parents[p_idx].get_dna()
            per_parent = math.ceil(len(traits) / len(parents))
            new_traits = [
                traits[t_idx] for t_idx in range(per_parent * p_idx, len(traits))
                if t_idx < min(per_parent * (p_idx + 1), len(traits))
            ]
            # TODO: make sure that the parents' traits are in the same order or this
            # will cause issues. OR find a way to bypass that
            child_traits = [
                *child_traits,
                *new_traits
            ]
        return cls(child_traits, target)
