import pytest

from genrulesengine.models.conditions.conditions import Condition, ConditionGroup
from genrulesengine.utils.evaluator import Evaluator

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

@pytest.fixture
def healthcare_context():
    return {
        "patient": {
            "age": 67,
            "conditions": ["diabetes", "hypertension"],
        },
        "plan": {
            "type": "medicare",
            "active": True
        },
        "visit_reason": "checkup"
    }


def test_condition_initialization():
    condition = Condition("age", "=", "18")
    assert condition is not None
    assert condition.field == "age"
    assert condition.operator == "="
    assert condition.value == "18"

def test_condition_evaluation(profile_context):
    condition = Condition("account.created_year", ">", "2000")
    assert Evaluator().evaluate_condition(condition, profile_context) is True

def test_all_success(healthcare_context):
    lst = [Condition("patient.age", ">", "25"), Condition("patient.conditions", "contains", "diabetes")]
    conditions = ConditionGroup(lst)
    assert all([Evaluator().evaluate_condition(condition, healthcare_context) for condition in conditions.all])

def test_all_failure(healthcare_context):
    lst = [Condition("patient.age", ">", "25"), Condition("patient.conditions", "contains", "anxiety disorder")]
    conditions = ConditionGroup(lst)
    assert all([Evaluator().evaluate_condition(condition, healthcare_context)
                for condition in conditions.all]) is False

def test_any_success(healthcare_context):
    lst = [Condition("patient.age", "<=", "18"), Condition("patient.conditions", "contains", "hypertension")]
    conditions = ConditionGroup(None, lst)
    assert any([Evaluator().evaluate_condition(condition, healthcare_context) for condition in conditions.any])

def test_any_failure(healthcare_context):
    lst = [Condition("patient.age", "<=", "18"), Condition("patient.plan", "in", ["aetna", "cigna", "kaiser"])]
    conditions = ConditionGroup(None, lst)
    assert any([Evaluator().evaluate_condition(condition, healthcare_context)
                for condition in conditions.any]) is False

