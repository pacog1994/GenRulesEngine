from genrulesengine.operators import OPERATORS

class TestOperators:
    def test_registration(self):
        assert "=" in OPERATORS
        assert "!=" in OPERATORS
        assert "<" in OPERATORS
        assert ">" in OPERATORS
        assert "<=" in OPERATORS
        assert ">=" in OPERATORS
        assert "in" in OPERATORS
        assert "contains" in OPERATORS

    def test_equality(self):
        eq, ne = OPERATORS["="], OPERATORS["!="]
        assert eq(5, 5) == True
        assert eq(5, 10) == False
        assert eq("wrong type", 1) is False
        assert ne(5, 6) == True
        assert ne(1, 1) == False
        assert ne("wrong type", 1) is True

    def test_comparison(self):
        gt, lt, gte, lte = OPERATORS[">"], OPERATORS["<"], OPERATORS[">="], OPERATORS["<="]
        assert gt(5, 1) == True
        assert gt(1, 1) == False
        assert gt(1, 2) == False
        assert lt(1, 5) == True
        assert lt(1, 1) == False
        assert lt(2, 1) == False
        assert gte(5, 1) == True
        assert gte(5, 5) == True
        assert gte(1, 5) == False
        assert lte(5, 1) == False
        assert lte(1, 1) == True
        assert lte(1, 2) == True

    def test_comparison_exceptions(self):
        gt, lt, gte, lte = OPERATORS[">"], OPERATORS["<"], OPERATORS[">="], OPERATORS["<="]
        assert gt("test", 1) == False
        assert lt("test", 1) == False
        assert gte("test", 1) == False
        assert lte("test", 1) == False

    def test_membership(self):
        op_in, contains = OPERATORS["in"], OPERATORS["contains"]
        arr = [1, 2, 3, 4, 5]
        assert op_in(1, arr) == True
        assert op_in(6, arr) == False
        assert contains(arr, 5) == True
        assert contains(arr, 10) == False

    def test_membership_exceptions(self):
        op_in, contains = OPERATORS["in"], OPERATORS["contains"]
        assert op_in("test", 1) == False
        assert op_in(1, [1, 2]) == True
        assert contains(1, 1) == False
        assert contains([1, 2, 3], 1) == True