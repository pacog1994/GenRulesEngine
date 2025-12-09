from dataclasses import dataclass
from typing import Any, Dict
from genrulesengine.registry.operators.operator import operators
from genrulesengine.models.conditions.conditions import Condition, ConditionGroup, ConditionTree
from genrulesengine.models.rule import Rule


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
        TODO Evaluate the condition group recursively
        :param cxt: context
        :return:
        """


    def evaluate_condition_tree(self, ct: ConditionTree, context: Dict[str, Any]) -> bool:
        """
        TODO
        :param ct:
        :param context:
        :return:
        """

    def evaluate_rule(self, rule: Rule, context: Dict[str, Any]) -> bool:
        """
        TODO
        :param rule:
        :param context:
        :return:
        """

    def evaluate_rules(self, rules: list[Rule], context: Dict[str, Any])->bool:
        """
        Evaluate list of rules
        :param rules: list of rules
        :param context: incoming data
        :return: True or False
        """
        return all([self.evaluate_rule(rule, context) for rule in rules])