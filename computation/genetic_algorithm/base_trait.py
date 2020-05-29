from copy import deepcopy
from random import choice, random


class BaseTrait:
    def __init__(self, trait_id, trait_pool: list = None):
        self.__id = trait_id
        self.__trait_pool = trait_pool
        # every possible trait has equal probability to be chosen
        self.value = None
        self.randomly_set_value()

    def __eq__(self, other):
        return isinstance(other, BaseTrait) and other.__id == self.__id

    def __repr__(self):
        return f"{self.__id}: {self.value}"

    def get_id(self):
        """
        Gets the id for the current Trait

        Returns:
            Object: ID for current Trait
        """
        return self.__id

    def get_value(self):
        """
        Gets the value associated with this Trait

        Returns:
            Object: value for current Trait
        """
        return self.value

    def set_value(self, new_value):
        """
        Update the value for the current Trait
        """
        self.value = new_value

    def get_trait_pool(self) -> list:
        """
        Get all possible values that can be assigned to this trait

        Returns:
            List: The trait pool
        """
        return deepcopy(self.__trait_pool)

    def randomly_set_value(self):
        """
        Randomly update this traits value
        """
        self.set_value(
            choice(self.__trait_pool)
            if self.__trait_pool is not None
            else random()
        )

    @classmethod
    def combine_trait_pool(cls, first_trait, second_trait):
        """
        Combine the trait pool for the same trait but different pools
        """
        if first_trait.equal(second_trait):
            new_trait_pool = [
                *first_trait.get_trait_pool(),
                *second_trait.get_trait_pool(),
            ]

            # TODO: Need to find some way to simplify it while maintaining
            # ratios
            return cls(first_trait.__id, new_trait_pool)

        raise Exception("Cannot merge trait pools of two different traits")
