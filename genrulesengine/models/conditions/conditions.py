from dataclasses import dataclass
from typing import Any

@dataclass
class ConditionTree:
    """
    Due to the nested nature of the conditional logic,
    conditions is represented as a tree
    """
    root: ConditionGroup | None = None

@dataclass
class ConditionGroup:
    """
    Initialize a Condition Group, acts as a nested node
    for condition tree
    """
    all: list[Condition | ConditionGroup] | None = None
    any: list[Condition | ConditionGroup] | None = None


@dataclass
class Condition:
    """
    Initialize Condition Leaf Node
    :param field: A string match of an existing attribute
    :param operator: built-in symbol that performs an operation
    :param value: Value to compare against
    """
    field: str
    operator: str
    value: Any


