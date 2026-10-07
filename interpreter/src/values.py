"""Runtime values, kept distinct from Python's truth and equality rules."""
from dataclasses import dataclass


class SchemeError(Exception):
    """A readable syntax or evaluation error."""


class Symbol(str):
    """A Scheme identifier, distinct from a Scheme string."""


class EmptyList:
    def __repr__(self):
        return "()"


NIL = EmptyList()


@dataclass(eq=False)
class Pair:
    car: object
    cdr: object


@dataclass(eq=False)
class Closure:
    parameters: list
    body: list
    environment: object


@dataclass(eq=False)
class Builtin:
    name: str
    function: object


def make_list(items, tail=NIL):
    for item in reversed(list(items)):
        tail = Pair(item, tail)
    return tail


def list_items(value):
    """Convert a proper list, rejecting an improper tail."""
    result = []
    while isinstance(value, Pair):
        result.append(value.car)
        value = value.cdr
    if value is not NIL:
        raise SchemeError("expected a proper list")
    return result


def is_number(value):
    return type(value) in (int, float)


def is_true(value):
    return value is not False
