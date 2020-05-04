import unittest

from src.math_algorithm.expression import Expression, Term


class TestExpression(unittest.TestCase):
    def setUp(self):
        a = Term(5, "a")
        b = Term(6, "b")
        c = Term(7, "c")
        self.fcn = Expression([a, b, c], 1)  # 5a + 6b + 7c + 1

    def test_simplify_expression(self):
        new_b = Expression([Term(4, "a")], 0)
        new_c = Expression([Term(3, "b")], 1)
        self.fcn.substitute({"b": new_b, "c": new_c})

        assert str(self.fcn) == "113a + 8"
