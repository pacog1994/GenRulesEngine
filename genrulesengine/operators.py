from typing import Any, Callable, Dict

# Type for operator functions: (left, right) -> bool
OperatorFn = Callable[[Any, Any], bool]
# Type for operator dict
OPERATORS: Dict[str, OperatorFn] = {}

def register(name: str):
    def decorator(func: OperatorFn):
        OPERATORS[name] = func
        return func
    return decorator

# equal
@register("=")
def eq(l, r):
    return l == r

# not equal
@register("!=")
def ne(l, r):
    return l != r

# greater-than
@register(">")
def gt(l, r):
    try:
        return l > r
    except TypeError:
        return False

# greater-than-or-equal
@register(">=")
def gte(l, r):
    try:
        return l >= r
    except TypeError:
        return False

# less-than
@register("<")
def lt(l, r):
    try:
        return l < r
    except TypeError:
        return False

# less-than-or-equal
@register("<=")
def lte(l, r):
    try:
        return l <= r
    except TypeError:
        return False

# Check to see if left is inside right
@register("in")
def op_in(l, r):
    try:
        return l in r
    except TypeError:
        return False

# Check to see if left contains right
@register("contains")
def contains(l, r):
    try:
        return r in l
    except TypeError:
        return False

