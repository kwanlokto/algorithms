from copy import deepcopy


class Expression:
    def __init__(self, terms=[], constant=0):
        self.terms = terms
        self.constant = constant
        self.__simplify_expression()        
    
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
    
    def solve(self, assignment):
        result = self.constant
        for term in self.terms:
            if term.variable in assignment:
                result += assignment[term.variable] * term.coefficient
        return result

    def substitute(self, assignments):
        found = True

        while found:
            found = False
            for var in assignments:
                found = self.__substitute_one_var(var, assignments[var]) if not found else True
        self.__simplify_expression()

    def __substitute_one_var(self, sub_var, fcn):
        """
        Substitute sub_var with fcn and update the terms

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

    def __str__(self):
        readable_fcn = ""
        for term in self.terms:
            readable_fcn += f'{term} + '
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
        return f'{self.coefficient}{self.variable}' if self.coefficient > 0 else f'({self.coefficient}){self.variable}'


a = Term(5, 'a')
b = Term(6, 'b')
c = Term(7, 'c')
fcn = Expression([a, b, c], 1)
print(fcn)

new_b = Expression([Term(4, 'a')], 0)
new_c = Expression([Term(3, 'b')], 1)
fcn.substitute({'b': new_b, 'c': new_c})
print(fcn)
