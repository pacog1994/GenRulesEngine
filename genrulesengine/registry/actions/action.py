from typing import Any, Dict
from genrulesengine.utils.decorator_registry import DecoratorRegistry

actions = DecoratorRegistry()

# built-in functions
@actions.register("approve")
def approve(_: Dict[str, Any] = None) -> str:
    return "approved"

@actions.register("deny")
def deny(_: Dict[str, Any] = None) -> str:
    return "deny"

@actions.register("login")
def login(d: Dict[str, Any] = None) -> str | None:
    for key in d:
        if key == "name":
            return f"{d[key]} is logged in"
    return None

@actions.register("logout")
def logout(d: Dict[str, Any] = None) -> str | None:
    for key in d:
        if key == "name":
            return f"{d[key]} is logged out"
    return None

