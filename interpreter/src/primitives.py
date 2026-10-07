"""The complete builtin library required by spec.md section 5."""
import operator
from functools import reduce
from environment import Environment
from printer import format_value
from values import (NIL, Pair, Symbol, Builtin, Closure, SchemeError,
                    is_number, is_true, make_list, list_items)


def require_numbers(values):
    if not all(is_number(value) for value in values):
        raise SchemeError("expected numbers")


def add(*values):
    require_numbers(values)
    return sum(values)


def multiply(*values):
    require_numbers(values)
    return reduce(operator.mul, values, 1)


def subtract(first, *rest):
    require_numbers((first,) + rest)
    return reduce(operator.sub, rest, first) if rest else -first


def integer_quotient(left, right):
    """Truncate toward zero without converting large integers to float."""
    if type(left) is not int or type(right) is not int:
        raise SchemeError("quotient expects integers")
    if right == 0:
        raise SchemeError("division by zero")
    result = abs(left) // abs(right)
    return -result if (left < 0) != (right < 0) else result


def divide(first, *rest):
    require_numbers((first,) + rest)
    if not rest:
        return 1.0 / first
    result = first
    for value in rest:
        result = (integer_quotient(result, value)
                  if type(result) is int and type(value) is int else result / value)
    return result


def is_list(value):
    while isinstance(value, Pair):
        value = value.cdr
    return value is NIL


def car(value):
    if not isinstance(value, Pair):
        raise SchemeError("car expects a pair")
    return value.car


def cdr(value):
    if not isinstance(value, Pair):
        raise SchemeError("cdr expects a pair")
    return value.cdr


def append(*lists):
    # All arguments except the last must be proper lists. The last may
    # also be a dotted tail, following the usual Scheme append convention.
    result = lists[-1] if lists else NIL
    for value in reversed(lists[:-1]):
        result = make_list(list_items(value), result)
    return result


def eq(left, right):
    if type(left) is bool or type(right) is bool:
        return type(left) is type(right) and left == right
    if is_number(left) and is_number(right):
        return left == right
    if isinstance(left, Symbol) and isinstance(right, Symbol):
        return left == right
    return left is right


def equal(left, right):
    # An explicit stack avoids Python recursion for deeply nested data.
    pending = [(left, right)]
    while pending:
        left, right = pending.pop()
        if isinstance(left, Pair) and isinstance(right, Pair):
            pending.extend([(left.car, right.car), (left.cdr, right.cdr)])
        elif type(left) is str and type(right) is str:
            if left != right:
                return False
        elif not eq(left, right):
            return False
    return True


def compare(operation, *values):
    return all(operation(a, b) for a, b in zip(values, values[1:]))


def numeric_predicate(operation, value):
    require_numbers((value,))
    return operation(value)


def display(value):
    print(format_value(value, display=True), end="")


def newline():
    print()


def initial_environment():
    functions = {
        "+": add, "-": subtract, "*": multiply, "/": divide,
        "quotient": integer_quotient, "modulo": operator.mod,
        "expt": operator.pow, "abs": abs,
        "not": lambda value: not is_true(value),
        "cons": Pair, "car": car, "cdr": cdr, "list": lambda *xs: make_list(xs),
        "length": lambda value: len(list_items(value)), "append": append,
        "null?": lambda value: value is NIL,
        "pair?": lambda value: isinstance(value, Pair), "list?": is_list,
        "number?": is_number, "boolean?": lambda value: type(value) is bool,
        "symbol?": lambda value: isinstance(value, Symbol),
        "string?": lambda value: type(value) is str,
        "procedure?": lambda value: isinstance(value, (Builtin, Closure)),
        "zero?": lambda value: numeric_predicate(lambda x: x == 0, value),
        "even?": lambda value: numeric_predicate(lambda x: x % 2 == 0, value),
        "odd?": lambda value: numeric_predicate(lambda x: x % 2 == 1, value),
        "eq?": eq, "equal?": equal, "display": display, "newline": newline,
    }
    for name, operation in [("=", operator.eq), ("<", operator.lt),
                            (">", operator.gt), ("<=", operator.le),
                            (">=", operator.ge)]:
        functions[name] = lambda *xs, op=operation: compare(op, *xs)
    return Environment((Symbol(name), Builtin(name, fn)) for name, fn in functions.items())
