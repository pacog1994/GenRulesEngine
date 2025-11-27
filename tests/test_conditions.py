from genrulesengine.conditions.conditions import Condition

class TestConditions:
    def test_condition_initialization(self):
        condition = Condition("age", "=", "18")
        assert condition is not None
        assert condition.field == "age"
        assert condition.operator == "="
        assert condition.value == "18"

    def test_condition_evaluation(self):
        context = { "age": 18 }
        condition = Condition("age", "=", "18")
        assert condition.evaluate(context) is True
        # context2 = {"age": True}
        # assert condition.evaluate(context2) is False




