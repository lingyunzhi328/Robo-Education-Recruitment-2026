"""Read S-expressions into symbols, atoms and Pair chains."""
import re
from lexer import StringToken, tokenize
from values import NIL, SchemeError, Symbol, make_list


INTEGER = re.compile(r"[+-]?\d+\Z")
FLOAT = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?\Z|[+-]?\d+[eE][+-]?\d+\Z")


def parse(source):
    tokens = tokenize(source)
    position = 0

    def read():
        nonlocal position
        if position >= len(tokens):
            raise SchemeError("unexpected end of input")
        token = tokens[position]
        position += 1
        if isinstance(token, StringToken):
            return token.value
        if token == "(":
            items = []
            tail = NIL
            while position < len(tokens) and tokens[position] != ")":
                if tokens[position] == ".":
                    if not items:
                        raise SchemeError("a dotted list needs a head")
                    position += 1
                    tail = read()
                    if position >= len(tokens) or tokens[position] != ")":
                        raise SchemeError("a dotted list has exactly one tail")
                    break
                items.append(read())
            if position >= len(tokens):
                raise SchemeError("missing closing parenthesis")
            position += 1
            return make_list(items, tail)
        if token in (")", "."):
            raise SchemeError(f"unexpected token: {token}")
        if token == "'":
            return make_list([Symbol("quote"), read()])
        if token == "#t":
            return True
        if token == "#f":
            return False
        if INTEGER.fullmatch(token):
            return int(token)
        if FLOAT.fullmatch(token):
            return float(token)
        return Symbol(token)

    expressions = []
    while position < len(tokens):
        expressions.append(read())
    return expressions
