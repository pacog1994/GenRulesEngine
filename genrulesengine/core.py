class Engine:
    def __init__(self, *rules):
        self.rules = rules

    def run(self, state):
        for rule in self.rules:
            if rule.condition(state):
                return rule.action(state)
        return None

