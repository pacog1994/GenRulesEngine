import pytest
import json
from genrulesengine.core.engine import Engine
from genrulesengine.models.rules.rule import RuleResult


@pytest.fixture
def load_json():
    return json.loads(
      '{"rules": ['
      '{"id": 1, "label": "Working Adult", "conditions":'
      '{"all": [{"field":"age", "operator": ">", "value": 18}, {"field":"age", "operator": "<", "value": 65}], '
      '"any": [{"field": "occupation", "operator": "in", "value": ["engineer", "analyst", "scientist"]},'
      ' {"field": "physically_able", "operator": "=", "value": "Y"}]}, "actions": ["approve"], '
      '"depends_on": ["Acknowledge Active User"]},'
      '{"id": 2, "label": "Determine Eligible Residency", "conditions":'
      '{"all": [{"field":"location.state", "operator": "in", "value": ["MI", "WA", "CA", "IL", "VA", "NY"]}],'
      '"any": []}, "actions": ["approve"], "depends_on": ["Acknowledge Active User"]},'
      '{"id": 3, "label": "Login User", "conditions":'
      '{"all": [], "any": []}, "actions": ["login"], "depends_on": ["Working Adult", "Determine Eligible Residency"]},'
      '{"id": 4, "label": "Acknowledge Active User", "conditions":'
      '{"all": [{"field":"account.status", "operator": "=", "value": "active"}], '
      '"any": []}, "actions": ["acknowledge"], "depends_on": []}]}')


@pytest.fixture
def profile_context():
    return {
        "name": "Bill",
        "age": 32,
        "occupation": "engineer",
        "location": {
            "state": "MI",
            "city": "Detroit",
        },
        "physically_able": "Y",
        "account": {
            "status": "active",
            "created_year": 2019,
        }
    }


def test_engine_e2e(load_json, profile_context):
    engine = Engine()
    assert not engine.rules  # empty
    # parse rules into a list and add into engines internal rules list
    engine.load(load_json)  # not empty
    assert engine.rules
    results = engine.run(profile_context)
    assert isinstance(results, list) and len(results) == 4
    rule_result = results[0]
    assert rule_result.label == "Acknowledge Active User"
    assert rule_result.output["acknowledge"] == "acknowledged"
    rule_result2 = results[1]
    assert rule_result2.label == "Working Adult"
    assert rule_result2.output["approve"] == "approved"
    rule_result3 = results[2]
    assert rule_result3.label == "Determine Eligible Residency"
    assert rule_result3.output["approve"] == "approved"
    rule_result4 = results[3]
    assert rule_result4.label == "Login User"
    assert rule_result4.output["login"] == "Bill is logged in"
