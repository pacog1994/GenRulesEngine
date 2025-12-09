from typing import Any
from genrulesengine.utils.decorator_registry import DecoratorRegistry

actions = DecoratorRegistry()

# built-in functions
@actions.register("approve")
def approve():
    return "approved"

@actions.register("deny")
def deny():
    return "deny"

@actions.register("login")
def login(cxt):
    for key in cxt:
        if key == "name":
            print(f"{cxt[key]} is logged in")
            return cxt[key]
    return None

@actions.register("logout")
def logout(cxt):
    print(f"{cxt.name} is logged out")

