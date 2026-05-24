from genrulesengine.registry.operators.operator import operators

def test_registration():
    assert "=" in operators.registry
    assert "!=" in operators.registry
    assert "<" in operators.registry
    assert ">" in operators.registry
    assert "<=" in operators.registry
    assert ">=" in operators.registry
    assert "in" in operators.registry
    assert "contains" in operators.registry

def test_equality():
    eq, ne = operators.registry["="], operators.registry["!="]
    assert eq(5, 5) == True
    assert eq(5, 10) == False
    assert eq("wrong type", 1) is False
    assert ne(5, 6) == True
    assert ne(1, 1) == False
    assert ne("wrong type", 1) is True

def test_comparison():
    gt, lt, gte, lte = operators.registry[">"], operators.registry["<"], operators.registry[">="], operators.registry["<="]
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

def test_comparison_exceptions():
    gt, lt, gte, lte = operators.registry[">"], operators.registry["<"], operators.registry[">="], operators.registry["<="]
    assert gt("test", 1) == False
    assert lt("test", 1) == False
    assert gte("test", 1) == False
    assert lte("test", 1) == False

def test_membership():
    op_in, contains = operators.registry["in"], operators.registry["contains"]
    arr = [1, 2, 3, 4, 5]
    assert op_in(1, arr) == True
    assert op_in(6, arr) == False
    assert contains(arr, 5) == True
    assert contains(arr, 10) == False

def test_membership_exceptions():
    op_in, contains = operators.registry["in"], operators.registry["contains"]
    assert op_in("test", 1) == False
    assert op_in("test", "test") == True
    assert op_in(1, [1, 2]) == True
    assert contains(1, 1) == False
    assert contains([1, 2, 3], 1) == True

def test_exclude_membership():
    not_in = operators.registry["not in"]
    assert not_in(1, [2, 3]) == True
    assert not_in(2, [1, 2, 3]) == False

def test_multivalue_contains():
    contains_any, contains_all = operators.registry["contains_any"], operators.registry["contains_all"]
    assert contains_any([1, 2, 3, 4, 5], [0, 7, 9, 1, 6]) == True
    assert contains_any([1,2], [3, 4, 5]) == False
    assert contains_all([1, 2, 3 ,4], [1, 2]) == True
    assert contains_all([1, 2, 3], [1, 2, 4, 5]) == False
    assert contains_any("The brown fox jumps over the fence", ["yellow", "orange", "brown"]) == True
    assert contains_any("Hello World", ["Test", "This"]) == False