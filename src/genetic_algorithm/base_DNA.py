from copy import deepcopy

from src.genetic_algorithm.base_trait import BaseTrait


class BaseDNA:
    def __init__(self, traits: list, target):
        self.traits = traits
        self.size = len(traits)
        self.__check_traits()
        self.target = target

    def __repr__(self):
        return f"DNA: {self.traits}"

    def __check_traits(self):
        """
        Raises an exception if the traits are not unique
        """
        if (
            len(set([trait.get_id() for trait in self.traits]))
            != self.size
        ):
            raise Exception("Traits are not unique")

    def get_dna(self) -> list:
        """
        Get a copy of all traits for this DNA strand

        Returns:
            list: List of all traits
        """
        return deepcopy(self.traits)

    def get_trait(self, trait_id) -> BaseTrait:
        """
        Get a single trait from DNA by its id

        Args:
            trait_id: a unique identifier to determine the trait we want

        Returns:
            Trait: Trait with id trait_id
        """
        selected_trait = None
        for trait in self.traits:
            selected_trait = (
                trait if trait.get_id() == trait_id else selected_trait
            )
        return selected_trait

    def mutate(self, mutation_rate: float):
        """
        Mutate the this DNA strand with some probability 'mutation_rate'
        for each cell

        Args:
            mutation_rate (float): Determines the probability of mutating the
                                   dna strand (each trait)
        """
        pass

    @property
    def fitness(self) -> float:
        """
        Determines how well this DNA strand fits the target

        Args:
            target: The target we want to reach
        """
        pass

    @classmethod
    def cross_over(cls, parents: list):
        """
        Determines how to create child DNA from parent DNA
        """
        pass
