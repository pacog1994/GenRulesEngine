from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from genrulesengine.models.conditions.condition import ConditionTree
from genrulesengine.registry.actions.action import actions

@dataclass
class Rule:
    """
    Logical mapping of conditions to evaluate and the actions to execute when the conditions are met
    :param label: name of the rule
    :param conditions: list of conditions that need to be met to satisfy the rule
    :param action_names: list of names that map to actions taken after satisfying conditions
    """
    id: int
    label: str
    conditions: ConditionTree
    action_names: list[str]
    depends_on: list[int] = field(default_factory=list)
    # description: Optional[str]
    # priority: Optional[int]


    def execute(self, cxt):
        for action in self.action_names:
            actions.registry[action].dispatch(cxt)

@dataclass
class RuleResult:
    """
    Object representing the results of a rule execution
    :param label: name of the rule
    :param triggered: trigger flag
    :param actions_executed: list of actions executed
    :param output: output of the executed actions
    """
    label: str
    triggered: bool
    actions_executed: list[str]
    output: Optional[Dict[str, Any]] | None
    skipped: bool = False
