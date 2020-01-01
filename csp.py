import itertools

import numpy as np
from numpy.linalg import LinAlgError


class MinCSP:
    """
    A constraint satisfaction problem which can also be used to 
    """
    def __init__(self, variables):
        self.variables = variables  # should contain all variables
        self.constraints = []
    
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
        Args:
            fcn (Function): Function to minimize
        """        
        if self.constraints < len(self.variables):
            raise ValueError("Function is not constrained to an enclosed domain")
        
        # Create self.constraint subsets of size len(columns.keys())
        poi = []
        for constraints in itertools.combinations(self.constraints, len(self.variables)):
            try:
                poi.append(self.get_poi(constraints))
            except LinAlgError:
                print(f'{constraints} produces a non square matrix or have dependent rows')
        
        # Remove all points that don't satisfy all constraints
        for point in poi:
            assignment = {self.variables[i]: point[i] for i in range(len(self.variables))}
            
            for constraint in self.constraints:
                if not constraint.satisfied(assignment):
                    poi.remove(point)
                    break
        
        # Calculate the min
        min_value = None
        for sat_point in poi:
            assignment = {self.variables[i]: sat_point[i] for i in range(len(self.variables))}
            value = fcn(**assignment)
            if min_value is None or value < min_value:
                min_value = value
        
        return min_value



    def get_poi(self, constraints):
        """
        Calculate the constraints' point(s) of intersection using linear algebra. Create a matrix from the constraints which we then use to solve. 
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
            for term in expression.terms:
                matrix.append(np.zeros(num_columns))
                
                # Add the coefficient to the correct column
                col_num = self.variables.index(term.variable)
                matrix[col_num] = term.coefficient
            
            constants.append(constraint.upper_bound - expression.constant)
        matrix = np.array(matrix)
        return np.linalg.solve(matrix, constants)


class Constraint:
    def __init__(self, expression, lower_bound=None, upper_bound=None):
        if lower_bound is None and upper_bound is None:
            raise ValueError("Constraint be bounded above or below")
        if lower_bound and upper_bound:
            raise ValueError("There is no constraint on this expression")
        self.expression = expression
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    def satisfied(self, assignment):
        """
        Returns true or false depending on whether the variable assignment is allowed

        Args:
            assignment (dict): key is variable name, and value is the value it is assigned
        Returns:
            bool: Whether assignment was successful or not
        """
        satisifed = True
        result = self.expression.solve(assignment)
        if self.lower_bound:
            satisifed = result >= self.lower_bound
        if self.upper_bound:
            satisifed = result <= self.upper_bound if satisifed else False
        
        return satisifed
