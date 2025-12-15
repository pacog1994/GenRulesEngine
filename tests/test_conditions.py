import pytest

from genrulesengine.models.conditions.condition import Condition, ConditionGroup, ConditionTree
from genrulesengine.core.evaluator import Evaluator

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

@pytest.fixture
def default_profile_condition_tree():
    _all = [Condition("account.status", "=", "active"), Condition("account.created_year", ">", 2000)]
    _any = [Condition("age", "=", "32"), Condition("occupation", "in", ["administrator", "ceo"])]
    root_all = [Condition("location.state", "=", "MI")]
    root_any = [ConditionGroup(_any, _all), Condition("account.created_year", "<=", 2030)]
    root = ConditionGroup(root_all, root_any)
    return ConditionTree(root)

def test_condition_initialization():
    condition = Condition("age", "=", "18")
    assert condition is not None
    assert condition.field == "age"
    assert condition.operator == "="
    assert condition.value == "18"

def test_condition_evaluation(profile_context):
    condition = Condition("account.created_year", ">", "2000")
    assert Evaluator().evaluate_condition(condition, profile_context) is True

    # inject wrong created_year
    profile_context["account"]["created_year"] = 1999
    assert Evaluator().evaluate_condition(condition, profile_context) is False

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

def test_condition_group_evaluation(profile_context):
    _all = [Condition("account.status", "=", "active"), Condition("account.created_year", ">", 2000)]
    _any = [Condition("age", "<", "32"), Condition("occupation", "in", ["engineer", "administrator", "ceo"])]
    condition_group = ConditionGroup(_all, _any)
    assert Evaluator().evaluate_condition_group(condition_group, profile_context) is True

    # inject wrong status data
    profile_context["account"]["status"] = "inactive"
    condition_group = ConditionGroup(_all,_any)
    assert Evaluator().evaluate_condition_group(condition_group, profile_context) is False

def test_condition_tree_evaluation_success(default_profile_condition_tree, profile_context):
    assert Evaluator().evaluate_condition_tree(default_profile_condition_tree, profile_context) is True

def test_condition_tree_evaluation_failure(default_profile_condition_tree, profile_context):
    # inject wrong state data
    profile_context["location"]["state"] = "WY"
    assert Evaluator().evaluate_condition_tree(default_profile_condition_tree, profile_context) is False