from genrulesengine.rule import Rule

class RulesEngine:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def load_rules(self, config):
        pass

    def run(self, flag, cxt):
        for rule in self.rules:
            if flag == "ALL":
                if rule.evaluate_all(cxt):
                    rule.execute(cxt)
            elif flag == "ANY":
                if rule.evaluate_any(cxt):
                    rule.execute(cxt)



