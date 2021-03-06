from copy import deepcopy


class Expression:
    """
    Linear expression. For constants a, b, c, ...
        ax + by + cz + ... + constant
    """

    def __init__(self, terms=[], constant=0):
        self.terms = terms
        self.constant = constant
        self.__simplify_expression()

    def solve(self, assignments):
        """
        Solve the expression by assigning the variables values from assignment
        Args:
            assignments (dict): each variable (key) is assigned a value
        Returns:
            float: solution for the given variable assignment
        """
        result = self.constant
        for term in self.terms:
            if term.variable in assignments:
                result += assignments[term.variable] * term.coefficient
            else:
                raise ValueError("Some variables are not assigned values.")
        return result

    def substitute(self, assignments):
        """
        Substitute variables with corresponding variable assignments

        Args:
            assignments (dict): each variable (key) is rewritten in terms of
                                other variables
        """
        found = True
        while found:
            found = False
            for var in assignments:
                found = (
                    self.__substitute_one_var(var, assignments[var])
                    if not found
                    else True
                )
        self.__simplify_expression()

    def __substitute_one_var(self, sub_var, fcn):
        """
        Substitute sub_var with fcn and update the terms

        Args:
            sub_var (str): variable we are substituting
            fcn (Expression): expression that is replacing the variable
        Returns:
            bool: Whether terms has been updated or not
        """
        found = False
        fcn = deepcopy(fcn)
        for i in range(len(self.terms)):
            replaced_term = self.terms[i]
            if replaced_term.variable == sub_var:
                found = True
                for term in fcn.terms:
                    term.coefficient *= replaced_term.coefficient
                self.constant += replaced_term.coefficient * fcn.constant
                self.terms.pop(i)
                self.terms.extend(fcn.terms)
        return found

    def __simplify_expression(self):
        """
        Remove all duplicate variables
        """
        new_terms = []
        while len(self.terms) > 0:
            for i in range(len(self.terms) - 1, 0, -1):
                if self.terms[0] == self.terms[i]:
                    term = self.terms.pop(i)
                    self.terms[0].coefficient += term.coefficient
            new_terms.append(self.terms.pop(0))
        self.terms = new_terms

    def __str__(self):
        readable_fcn = ""
        for term in self.terms:
            readable_fcn += f"{term} + "
        readable_fcn += str(self.constant)
        return readable_fcn


class Term:
    def __init__(self, coefficient, variable):
        """
        Args:
            coefficient (float): the term's coeffiecient
            variable (str): variable associated with this term
        """
        self.variable = variable
        self.coefficient = coefficient

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.variable == other.variable
        return False

    def __str__(self):
        return (
            f"{self.coefficient}{self.variable}"
            if self.coefficient > 0
            else f"({self.coefficient}){self.variable}"
        )
