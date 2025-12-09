from dataclasses import dataclass
from genrulesengine.models.conditions.conditions import ConditionTree
from genrulesengine.registry.actions.action import actions

@dataclass
class Rule:
    """
    Object wrapper for a set of conditions and actions
    :param name: name of the rule
    :param conditions: list of conditions that need to be met to satisfy the rule
    :param action_names: list of names that map to actions taken after satisfying conditions
    """
    name: str
    conditions: ConditionTree
    action_names: list[str]

    def execute(self, cxt):
        for action in self.action_names:
            actions.registry[action].dispatch(cxt)