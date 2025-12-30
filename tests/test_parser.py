import pytest

import json
from genrulesengine.core.parser import Parser
from genrulesengine.models.conditions.condition import ConditionTree, ConditionGroup
from genrulesengine.models.rules.rule import Rule


@pytest.fixture
def parser():
    parser = Parser()
    return parser

@pytest.fixture
def sample_json():
    return json.loads('{"id": 1, "label": "Working Adult", "conditions":'
       '{"any": [{"field":"age", "operator": ">", "value": 18}, {"field":"age", "operator": "<", "value": 65}], '
       '"all": [{"field":"occupation", "operator":"=", "value": "false"}, {"field":"location", "operator":"=", "value": "wa"}]},'
       ' "actions": ["approve"]}')

def test_parse_rule(parser, sample_json):
    rule = parser.parse_rule({}, sample_json)
    assert isinstance(rule, Rule)
    assert rule.label == "Working Adult"
    assert isinstance(rule.action_names, list) and rule.action_names == ["approve"]
    assert isinstance(rule.conditions, ConditionTree)
    assert isinstance(rule.conditions.root, ConditionGroup)
    _all, _any = rule.conditions.root.all, rule.conditions.root.any
    assert len(_all) == 2
    all_cond1, all_cond2 = _all[0], _all[1]
    assert all_cond1.field == "occupation" and all_cond1.operator == "=" and all_cond1.value == "false"
    assert all_cond2.field == "location" and all_cond2.operator == "=" and all_cond2.value == "wa"
    any_cond1, any_cond2 = _any[0], _any[1]
    assert any_cond1.field == "age" and any_cond1.operator == ">" and any_cond1.value == 18
    assert any_cond2.field == "age" and any_cond2.operator == "<" and any_cond2.value == 65