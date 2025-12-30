from dataclasses import dataclass, field
from typing import Any, Callable, Dict

from genrulesengine.models.rules.rule import Rule, RuleResult
from genrulesengine.core.parser import Parser
from genrulesengine.core.evaluator import Evaluator
from genrulesengine.core.executor import Executor

@dataclass
class Engine:
    """
    Class's intended design is engine orchestration
    """
    """
    Loads File -> Converts to Rule Models
    Orchestrates Rule Order
    Evaluates -> Executes -> Outputs
    """
    parser: Callable[[Dict[str, Any]], list[Rule]] = field(default_factory=lambda: Parser().parse_rules)
    evaluator: Callable[[Dict[str, Any]], RuleResult] = field(default_factory=lambda: Evaluator().evaluate_rule)
    executor: Callable[[Dict[str, Any]], list[RuleResult]] = field(default_factory=lambda: Executor().execute)
    rules: list[Rule] = field(default_factory=list)


    def load(self, context: Dict[str, Any]) -> None:
        self.rules = self.parser(context)

    def resolve_execution_order(self) -> list[Rule]:
        rule_map = {r.id: r for r in self.rules}
        visited = set()
        stack = []

        def topological_sort(node: Rule):
            if node.id in visited:
                return
            visited.add(node.id)
            for dep in rule.depends_on:
                topological_sort(rule_map[dep])
            stack.append(node)

        for rule in self.rules:
            topological_sort(rule)

        return stack

    def run(self, context: Dict[str, Any]) -> list[RuleResult]:
        ordered_rules = self.resolve_execution_order()
        results = []
        prev_results_tracker = {}

        for rule in ordered_rules:
            evaluated_result = self.evaluator(rule, context, prev_results_tracker)
            executed_result = self.executor(rule, context, evaluated_result)
            results.append(executed_result)
            prev_results_tracker[rule.id] = executed_result

        return results