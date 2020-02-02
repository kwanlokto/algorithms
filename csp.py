import itertools

import numpy as np
from numpy.linalg import LinAlgError

from expression import Expression, Term


class CSP:
    """
    A constraint satisfaction problem which can also be used to minimize a function
    """

    def __init__(self, variables):
        self.variables = variables  # should contain all variables
        self.constraints = [
            Constraint(Expression([Term(-1, variable)]), 0) for variable in variables
        ]  # all variables should be >= 0

    def add_constraint(self, constraint):
        """
        Add a Constraint to the CSP. 
        Raise a ValueError excpetion if an unknown variable is found in the constraint

        Args:
            constraint (Constraint): Constraint to add
        """
        # TODO: check if constraint uses variables that are not in the domain
        self.constraints.append(constraint)

    def minimize(self, fcn):
        """
        Minimize fcn with respect to self.constraints 

        Args:
            fcn (Function): Linear function to minimize
        Return:
            float: Min value returned by fcn within the constraints
        """
        if len(self.constraints) < len(self.variables):
            raise ValueError("Function is not constrained to an enclosed domain")

        # Create self.constraint subsets of size len(columns.keys())
        poi = []
        for constraints in itertools.combinations(
            self.constraints, len(self.variables)
        ):
            try:
                poi.append(self.get_poi(constraints))
            except LinAlgError:
                print(
                    f"{constraints} produces a non square matrix or have dependent rows"
                )

        # Remove all points that don't satisfy all constraints
        for point in poi:
            assignment = {
                self.variables[i]: point[i] for i in range(len(self.variables))
            }

            for constraint in self.constraints:
                if not constraint.satisfied(assignment):
                    poi.remove(point)
                    break

        # Calculate the min
        min_value = None
        for sat_point in poi:
            assignment = {
                self.variables[i]: sat_point[i] for i in range(len(self.variables))
            }
            value = fcn(**assignment)
            if min_value is None or value < min_value:
                min_value = value

        return min_value

    def get_poi(self, constraints):
        """
        Calculate the constraints' point(s) of intersection using linear algebra. Create a matrix from the constraints 
        which we then use to solve. 
            - If there is no solution that means that the constraints are not linearly independent, which means no solution.
            - If there are multiple solutions then 
        Args:
            constraints (list): A subset of self.constraints and size of list is equivalent to the number of variables
        """

        # Create the matrix we want to solve
        num_columns = len(self.variables)
        matrix = []
        constants = []

        for constraint in constraints:
            expression = constraint.expression
            row = np.zeros(num_columns)

            for term in expression.terms:
                # Add the coefficient to the correct column
                col_num = self.variables.index(term.variable)
                row[col_num] = term.coefficient

            matrix.append(row)
            constants.append(constraint.upper_bound - expression.constant)
        matrix = np.array(matrix)
        return np.linalg.solve(matrix, constants)


class Constraint:
    def __init__(self, expression, upper_bound):
        """
        Args:
            expression (Expression): Function expression
            upper_bound (float): Upper bound on function results
        """
        self.expression = expression
        self.upper_bound = upper_bound

    def satisfied(self, assignment):
        """
        Returns true or false depending on whether the variable assignment is allowed

        Args:
            assignment (dict): key is variable name, and value is the value it is assigned
        Returns:
            bool: Whether assignment was successful or not
        """
        return self.expression.solve(assignment) <= self.upper_bound

    def __repr__(self):
        return f"{self.expression} < {self.upper_bound}"


if __name__ == "__main__":
    variables = ["a", "b"]
    csp = CSP(variables)

    a = Term(5, "a")
    b = Term(6, "b")
    constraint1 = Constraint(Expression([a, b]), 11)
    csp.add_constraint(constraint1)


    def test(a, b):
        return a - b

    print(csp.minimize(test))
