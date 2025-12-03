import inspect

import pytest

from genrulesengine.rule import Rule
from genrulesengine.conditions.condition import Condition

@pytest.fixture
def initialize():
    # setup conditions
    condition = Condition("age", ">=", 18)
    condition2 = Condition("age", "=", 21)
    conditions = [condition, condition2]

    # setup actions
    list_actions = ["approve", "login"]

    return Rule("age compliance", conditions, list_actions)

def test_initialization(initialize):
    rule = initialize
    for key, value in inspect.getmembers(rule):
        if key == "name":
            assert value is "age compliance"
        elif key == "conditions":
            assert isinstance(value, list)
            for cond in value:
                assert isinstance(cond, Condition)
        elif key == "list_actions":
            for action in value:
                assert isinstance(action, str)

def test_rule_evaluate_all(initialize):
    """
    Test to see if the rule fixture evaluates all correctly
    :param initialize: Rule fixture
    :return: nil
    """
    rule = initialize
    context = {"age": 21}
    assert rule.evaluate_all(context) is True
    context = {"age": 30}
    assert rule.evaluate_all(context) is False

def test_rule_evaluate_any(initialize):
    """
    Test to see if the rule fixture evaluates any correctly
    :param initialize: Rule fixture
    :return: nil
    """
    rule = initialize
    # check Condition1 -> age >= 18 true and Condition2 -> age == 21 false
    context = {"age": 50}
    assert rule.evaluate_any(context) is True
    # check both Conditions False
    context = {"age": 8}
    assert rule.evaluate_any(context) is False




