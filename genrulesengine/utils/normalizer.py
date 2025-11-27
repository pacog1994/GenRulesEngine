from genrulesengine.utils.decorator_registry import DecoratorRegistry

"""
TODO Implement Normalizer using Decorator, this requires refactoring DecoratorRegistry and Overwriting register method
registry that stores and dispatches stored normalize Fns
normalizer = DecoratorRegistry()
"""

def normalize(_input: str, value: str):
        try:
            if type(_input) != type(value):
                value = type(_input)(value)
        except ValueError:
            pass
        return value


