from typing import Any, Callable, Dict
from genrulesengine.utils.decorator_registry import DecoratorRegistry

# Registry stores and dispatches operator Fns
operators = DecoratorRegistry()

# built-in functions

# equal
@operators.register("=")
def eq(l, r):
    return l == r

# not equal
@operators.register("!=")
def ne(l, r):
    return l != r

# greater-than
@operators.register(">")
def gt(l, r):
    try:
        return l > r
    except TypeError:
        return False

# greater-than-or-equal
@operators.register(">=")
def gte(l, r):
    try:
        return l >= r
    except TypeError:
        return False

# less-than
@operators.register("<")
def lt(l, r):
    try:
        return l < r
    except TypeError:
        return False

# less-than-or-equal
@operators.register("<=")
def lte(l, r):
    try:
        return l <= r
    except TypeError:
        return False

# Check to see if left is inside right
@operators.register("in")
def op_in(l, r):
    try:
        return l in r
    except TypeError:
        return False

@operators.register("not in")
def not_in(l, r):
    try:
        return not l in r
    except TypeError:
        return False

# Check to see if left contains right
@operators.register("contains")
def contains(l, r):
    try:
        return r in l
    except TypeError:
        return False

# Multivalue Operators ---------------------------------
@operators.register("contains_any")
def contains_any(l, r: list[Any]) -> bool:
    try:
        for v in r:
            if v in l:
                return True
        return False
    except TypeError:
        return False

@operators.register("contains_all")
def contains_all(l, r: list[Any]) -> bool:
    try:
        for v in r:
            if v not in l:
                return False
        return True
    except TypeError:
        return False