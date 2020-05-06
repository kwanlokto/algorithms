import unittest

from computation.math_algorithm.csp import CSP, Constraint
from computation.math_algorithm.expression import Expression, Term


class TestCSP(unittest.TestCase):
    def setUp(self):
        variables = ["a", "b"]
        self.csp = CSP(variables)

        a = Term(coefficient=5, variable="a")
        b = Term(coefficient=6, variable="b")
        constraint = Constraint(Expression([a, b]), 11)
        self.csp.add_constraint(constraint)

    def test_minimize_constraint(self):
        def test(a, b):
            return a - b

        assert self.csp.minimize(test) == -1.8333333333333333
