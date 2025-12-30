from dataclasses import dataclass
from typing import Any, Dict
from genrulesengine.registry.operators.operator import operators
from genrulesengine.models.conditions.condition import Condition, ConditionGroup, ConditionTree
from genrulesengine.models.rules.rule import Rule, RuleResult


def _get_nested_value(field: str, data: Dict[str, Any])->Any:
    """
    Helper Method to get nested value from dictionary
    :param field: target key
    :param data:  dict object
    :return: target value
    """
    keys = field.split(".")
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            raise KeyError(f"Key: {key} does not exist")
    return value


@dataclass
class Evaluator:

    def evaluate_condition(self, condition: Condition, context: Dict[str, Any]) -> bool:
        """
        Instance method to evaluate the condition
        :param condition: expression to evaluate
        :param context: input data the rule evaluates against coming from external source
        :return: True or False
        """
        _input = _get_nested_value(condition.field, context)
        if not operators.registry[condition.operator]:
            raise ValueError(f"invalid operator detected: {condition.operator}")

        try:
            # on comparison, input and value should be compared through intent
            if (type(_input) != type(condition.value) and
                    (condition.operator != "in" and condition.operator != "contains")):
                condition.value = type(_input)(condition.value)
        except ValueError:
            pass
        return operators.dispatch(condition.operator, _input, condition.value)

    def evaluate_condition_group(self, cg: ConditionGroup, context: Dict[str, Any]) -> bool:
        """
        Evaluates the condition group recursively, due to potential nested condition groups
        :param cg: condition group
        :param context: input data
        :return: True or False
        """
        if cg.any:
            # internal any flag, passes if ANY node passes
            passes = False
            for node in cg.any:
                if isinstance(node, ConditionGroup):
                    if self.evaluate_condition_group(node, context):
                        passes = True
                        continue
                else:
                    if self.evaluate_condition(node, context):
                        passes = True
                        break
            if not passes:
                return False

        if cg.all:
            for node in cg.all:
                if isinstance(node, ConditionGroup):
                    if not self.evaluate_condition_group(node, context):
                        return False
                else:
                    if not self.evaluate_condition(node, context):
                        return False

        # If reaches the end of check, return True
        return True

    def evaluate_condition_tree(self, ct: ConditionTree, context: Dict[str, Any]) -> bool:
        """
        Evaluate the root node of the tree
        :param ct: condition tree
        :param context: input data
        :return: True or False
        """
        return self.evaluate_condition_group(ct.root, context)

    def evaluate_rule(self, rule: Rule, data: Dict[str, Any], prev_results: Dict[int, RuleResult] ) -> RuleResult:
        """
        Evaluate and return the corresponding result
        :param rule: rule to evaluate
        :param data: incoming data to evaluate against
        :param prev_results: tracker for processed rule results, used for dependency checking
        :return: True or False
        """

        # make a skip boolean and use list to track resolved_dependencies
        for dependency_id in rule.depends_on:
            dependency_results = prev_results.get(dependency_id)
            if not dependency_results or not dependency_results.triggered:
                return RuleResult(
                    label=rule.label,
                    triggered=False,
                    actions_executed=[],
                    output=None,
                    skipped=True,
                )

        triggered = self.evaluate_condition_tree(rule.conditions, data)

        return RuleResult(
            label=rule.label,
            triggered=triggered,
            skipped=False,
            actions_executed=[],
            output=None
        )
