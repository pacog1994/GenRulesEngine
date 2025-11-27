from typing import Dict, Any
from genrulesengine.operators.operators import operators

class Condition:

    def __init__(self, field: str, operator: str, value: Any):
        """
            Initialize instance
            :param field: A string match of an existing attribute
            :param operator: built-in symbol that performs an operation
            :param value: Value to compare against
        """
        self.field = field
        self.operator = operator
        self.value = value

    def evaluate(self, context: Dict[str, Any])->bool:
        """
        Instance method to evaluate the condition
        :param context: input data the rule evaluates against coming from external source
        :return: True or False
        """
        _input = context.get(self.field)
        if not operators.registry[self.operator]:
            raise ValueError(f"invalid operator detected: {self.operator}")

        try:
            # on comparison, input and value should be compared through intent
            if type(_input) != type(self.value):
                self.value = type(_input)(self.value)
        except ValueError:
            pass
        return operators.dispatch(self.operator, _input, self.value)