import pytest

from genrulesengine.models.rules.rule import Rule, RuleResult
from genrulesengine.models.conditions.condition import Condition, ConditionGroup, ConditionTree
from genrulesengine.core.evaluator import Evaluator


@pytest.fixture
def initialize():
    # setup conditions
    _all = [Condition("age", ">=", 18)]
    _any = [Condition("age", "<", 65)]
    conditions = ConditionGroup(_all, _any)
    ct = ConditionTree(conditions)
    # setup actions
    list_actions = ["approve", "login"]
    return Rule("age compliance", ct, list_actions)


@pytest.fixture
def profile_context():
    return {
        "age": 32,
        "occupation": "engineer",
        "location": {
            "state": "MI",
            "city": "Detroit",
        },
        "account": {
            "status": "active",
            "created_year": 2019,
        }
    }


def test_initialization(initialize):
    rule = initialize
    assert isinstance(rule, Rule)
    assert isinstance(rule.conditions, ConditionTree)
    assert isinstance(rule.action_names, list)
    assert rule.label == "age compliance"


def test_rule_evaluation_and_execution_success(initialize, profile_context):
    rule = initialize
    result = Evaluator().evaluate_rule(rule, profile_context)
    assert isinstance(result, RuleResult)
    assert result.triggered is True
