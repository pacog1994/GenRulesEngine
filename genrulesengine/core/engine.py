from genrulesengine.models.rules.rule import Rule

class RulesEngine:
    """
    Class's intended design is engine orchestration
    TODO Implement
    """
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def list_rules(self) -> list[Rule]:
        return self.rules

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def load_rules(self, cxt):
        pass
        # use parser on json
        # normalize data
        # store in self.rules

    def run(self, flag, cxt):
        for rule in self.rules:
            if flag == "ALL":
                if rule.evaluate_all(cxt):
                    rule.execute(cxt)
            elif flag == "ANY":
                if rule.evaluate_any(cxt):
                    rule.execute(cxt)

