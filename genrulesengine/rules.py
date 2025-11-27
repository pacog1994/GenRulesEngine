from typing import Any

class Rules:
    def __init__(self, conditions: list[Any], actions: list[Any]):
        self.conditions = conditions
        self.actions = actions
