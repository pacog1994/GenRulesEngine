from dataclasses import dataclass
from typing import Any, Dict
from genrulesengine.models.rules.rule import RuleResult, Rule
from genrulesengine.registry.actions.action import actions

"""
This class is meant to abstract the executing functionality for the engine
"""
@dataclass
class Executor:
    def execute(self, rule: Rule, data: Dict[str, Any], result: RuleResult) -> RuleResult:
        if not result.triggered:
            return result

        outputs = {}

        for action_name in list(rule.action_names):
            outputs[action_name] = actions.dispatch(action_name, data)
            result.actions_executed.append(action_name)

        result.output = outputs
        return result

