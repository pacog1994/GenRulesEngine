import pytest
import json
from genrulesengine.core.engine import Engine
from genrulesengine.models.rules.rule import RuleResult


@pytest.fixture
def load_json():
    return json.loads('{"rules": [{"id": 1, "label": "Working Adult", "conditions":'
       '{"all": [{"field":"age", "operator": ">", "value": 18}, {"field":"age", "operator": "<", "value": 65}], '
       '"any": [{"field":"occupation", "operator":"=", "value": "engineer"}, {"field":"location", "operator":"=", "value": "wa"}]},'
       ' "actions": ["approve"]}, {"id": 2, "label": "Acknowledge Active User", "conditions":'
       '{"all": [{"field":"account.status", "operator": "=", "value": "active"}], '
       '"any": []},'
       ' "actions": ["login"]}]}')

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
        "account": {
            "status": "active",
            "created_year": 2019,
        }
    }

def test_engine_e2e(load_json, profile_context):
     engine = Engine()
     assert not engine.rules # empty
     # parse rules into a list and add into engines internal rules list
     engine.load(load_json) # not empty
     assert engine.rules
     results = engine.run(profile_context)
     assert isinstance(results, list) and len(results) == 2
     rule_result = results[0]
     assert isinstance(rule_result, RuleResult)
     assert rule_result.output["approve"] == "approved"
     rule_result2 = results[1]
     assert isinstance(rule_result2, RuleResult)
     assert rule_result2.output["login"] == "Bill is logged in"

     profile_context["age"] = 100
     results = engine.run(profile_context)
     rule_result = results[0]
     assert rule_result.output is None