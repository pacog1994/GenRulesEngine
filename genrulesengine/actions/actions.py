class Action:
    def __init__(self, name: str, handler):
        self.name = name
        self.handler = handler

    def execute(self, context: dict):
        return self.handler(context)