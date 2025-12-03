from typing import Any
from genrulesengine.conditions.condition import Condition
from genrulesengine.actions.actions import actions


class Rule:
    def __init__(self, name: str, conditions: list[Condition], action_names: list[str]):
        """
        Object wrapper for a set of conditions and actions
        :param name: name of the rule
        :param conditions: list of conditions that need to be met to satisfy the rule
        :param action_names: list of names that map to actions taken after satisfying conditions
        """
        self.name = name
        self.conditions = conditions
        self.action_names = action_names

    def evaluate_all(self, cxt):
        return all([condition.evaluate(cxt) for condition in self.conditions])

    def evaluate_any(self, cxt):
        return any([condition.evaluate(cxt) for condition in self.conditions])

    def execute(self, cxt):
        for a_name in self.action_names:
            actions.registry[a_name].dispatch(cxt)