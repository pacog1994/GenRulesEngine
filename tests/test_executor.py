# import pytest
#
# from genrulesengine.models.conditions.condition import Condition, ConditionGroup, ConditionTree
# from genrulesengine.models.rules.rule import Rule, RuleResult
# from genrulesengine.core.evaluator import Evaluator
# from genrulesengine.core.executor import Executor
#
# @pytest.fixture
# def initialize_rule():
#     # setup conditions
#     _all = [Condition("age", ">=", 18)]
#     _any = [Condition("age", "<", 65)]
#     conditions = ConditionGroup(_all, _any)
#     ct = ConditionTree(conditions)
#     # setup actions
#     list_actions = ["approve", "login"]
#     return Rule(1, "age compliance", ct, list_actions, [])
#
# @pytest.fixture
# def profile_context():
#     return {
#         "name": "Bill",
#         "age": 32,
#         "occupation": "engineer",
#         "location": {
#             "state": "MI",
#             "city": "Detroit",
#         },
#         "account": {
#             "status": "active",
#             "created_year": 2019,
#         }
#     }
#
# def test_rule_execution(initialize_rule, profile_context):
#     rule = initialize_rule
#     result = Evaluator().evaluate_rule(rule, profile_context, {})
#     executed_result = Executor().execute(rule, profile_context, result)
#     assert isinstance(executed_result, RuleResult)
#     # check to see if the actions in rule have been processed
#     assert executed_result.output[rule.action_names[0]] == "approved"
#     assert executed_result.output[rule.action_names[1]] == "Bill is logged in"
#
#
