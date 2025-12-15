import json
from dataclasses import dataclass
from typing import Any, Dict

from genrulesengine.models.conditions.condition import Condition, ConditionGroup, ConditionTree
from genrulesengine.models.rules.rule import Rule
""" Supported Rules Engine config file
{
    "rules": [{
        // metadata support ---------------
        "id",
        "label",
        "description",
        "version",
        "priority",
        ...,
        //--------------------
        "conditions": {
            "any": [
                        {
                            "field": "",
                            "operator": "",
                            "value": ""
                        },
                        {...}
                    ],
            "all": [
                        {...}
                   ]
        },
        "actions": ["", "..."]
    }, {...}],
    // do later alongside metadata ------------------------------------
    "ruleset": {
        ....   
    }
    // do later -------------------------------------
    "options": {
    
    }
}
"""

""" Supported Rules Engine input file
    
"""
@dataclass
class Parser:

    def parse_condition(self, data: Dict[str, Any]) -> Condition:
        try:
           return Condition(
               field=data["field"],
               operator=data["operator"],
               value=data["value"]
           )
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")

    def parse_condition_group(self, data: Dict[str, Any]) -> ConditionGroup:
        try:
            return ConditionGroup(
                all=[self.parse_node(node) for node in data.get("all", [])],
                any=[self.parse_node(node) for node in data.get("any", [])]
            )
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")

    def parse_node(self, data: Dict[str, Any]):
        if "field" in data:
            return self.parse_condition(data)
        return self.parse_condition_group(data)

    def parse_condition_tree(self, data: Dict[str, Any]) -> ConditionTree:
        try:
            return ConditionTree(root=self.parse_condition_group(data["conditions"]))
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")

    def parse_rule(self, data: Dict[str, Any]) -> Rule:
        try:
            return Rule(
                label=data["label"],
                conditions=self.parse_condition_tree(data),
                action_names=data["actions"]
            )
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")



