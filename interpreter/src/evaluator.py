"""Evaluation, special forms and application with lexical scope."""
from environment import Environment
from values import (NIL, Pair, Symbol, Closure, Builtin, SchemeError,
                    is_true, list_items)


def check_arity(arguments, minimum, maximum=None):
    if len(arguments) < minimum or (maximum is not None and len(arguments) > maximum):
        raise SchemeError("wrong number of arguments")


def parameters(value):
    names = list_items(value)
    if not all(isinstance(name, Symbol) for name in names):
        raise SchemeError("parameter names must be symbols")
    if len(set(names)) != len(names):
        raise SchemeError("duplicate parameter name")
    return names


def evaluate_sequence(expressions, environment):
    result = None
    for expression in expressions:
        result = evaluate(expression, environment)
    return result


def apply(procedure, arguments):
    if isinstance(procedure, Builtin):
        try:
            return procedure.function(*arguments)
        except (TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
            raise SchemeError(f"{procedure.name}: {error}") from error
    if isinstance(procedure, Closure):
        if len(arguments) != len(procedure.parameters):
            raise SchemeError("wrong number of arguments for closure")
        local = Environment(zip(procedure.parameters, arguments), procedure.environment)
        return evaluate_sequence(procedure.body, local)
    raise SchemeError("operator is not a procedure")


def evaluate(expression, environment):
    if isinstance(expression, Symbol):
        return environment.lookup(expression)
    if not isinstance(expression, Pair):
        return expression
    forms = list_items(expression)
    head, args = forms[0], forms[1:]
    special = str(head) if isinstance(head, Symbol) else None
    if special == "quote":
        check_arity(args, 1, 1)
        return args[0]
    if special == "if":
        check_arity(args, 2, 3)
        if is_true(evaluate(args[0], environment)):
            return evaluate(args[1], environment)
        return evaluate(args[2], environment) if len(args) == 3 else None
    if special == "cond":
        for index, clause in enumerate(args):
            parts = list_items(clause)
            check_arity(parts, 1)
            is_else = isinstance(parts[0], Symbol) and parts[0] == "else"
            if is_else and index != len(args) - 1:
                raise SchemeError("else must be the final cond clause")
            test = True if is_else else evaluate(parts[0], environment)
            if is_true(test):
                return evaluate_sequence(parts[1:], environment) if len(parts) > 1 else test
        return None
    if special in ("and", "or"):
        result = special == "and"
        for argument in args:
            result = evaluate(argument, environment)
            if (special == "and" and not is_true(result)) or (special == "or" and is_true(result)):
                return result
        return result
    if special == "define":
        check_arity(args, 2)
        target = args[0]
        if isinstance(target, Pair):
            if not isinstance(target.car, Symbol):
                raise SchemeError("function name must be a symbol")
            name = target.car
            value = Closure(parameters(target.cdr), args[1:], environment)
        else:
            check_arity(args, 2, 2)
            if not isinstance(target, Symbol):
                raise SchemeError("variable name must be a symbol")
            name, value = target, evaluate(args[1], environment)
        environment[name] = value
        return name
    if special == "lambda":
        check_arity(args, 2)
        return Closure(parameters(args[0]), args[1:], environment)
    if special == "let":
        check_arity(args, 2)
        bindings = []
        for binding in list_items(args[0]):
            parts = list_items(binding)
            check_arity(parts, 2, 2)
            if not isinstance(parts[0], Symbol):
                raise SchemeError("binding name must be a symbol")
            bindings.append((parts[0], evaluate(parts[1], environment)))
        return evaluate_sequence(args[1:], Environment(bindings, environment))
    if special == "begin":
        return evaluate_sequence(args, environment)
    # Applicative order: evaluate the operator and arguments before apply.
    procedure = evaluate(head, environment)
    return apply(procedure, [evaluate(arg, environment) for arg in args])
