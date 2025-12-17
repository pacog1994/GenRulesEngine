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
    Evaluates -> Executes -> Outputs
    """
    parser: Callable[[Dict[str, Any]], list[Rule]] = field(default_factory=lambda: Parser().parse_rules)
    evaluator: Callable[[Dict[str, Any]], RuleResult] = field(default_factory=lambda: Evaluator().evaluate_rule)
    executor: Callable[[Dict[str, Any]], list[RuleResult]] = field(default_factory=lambda: Executor().execute)
    rules: list[Rule] = field(default_factory=list)


    def load(self, context: Dict[str, Any]) -> None:
        self.rules = self.parser(context)

    def run(self, context: Dict[str, Any]) -> list[RuleResult]:
        results: list[RuleResult] = []

        for rule in self.rules:
            result = self.evaluator(rule, context)
            result = self.executor(rule, context, result)
            results.append(result)

        return results