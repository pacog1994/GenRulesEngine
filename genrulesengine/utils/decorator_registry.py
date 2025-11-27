from typing import Any, Callable, Dict

# abstract callable function
Fn = Callable[..., Any]

class DecoratorRegistry:
    # registry that stores functions using a decorator
    def __init__(self):
        self.registry: Dict[str, Fn]  = {}

    def register(self, name: str):
        """
        registers the decorator function in the registry
        :param name: function being searched
        :return:
        """

        def decorator(fn: Fn):
            self.registry[name] = fn
            return fn
        return decorator

    def dispatch(self, name: str, *args, **kwargs):
        """
        Executes the function called and registered in the registry
        :param name: function being searched
        :param args: positional arguments
        :param kwargs: keyword arguments
        """

        # TODO: Add Type-Safe Checks

        if name not in self.registry:
            raise ValueError(f"Function '{name}' is not registered")
        return self.registry[name](*args, **kwargs)