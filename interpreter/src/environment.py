"""Nested lexical bindings; each closure retains its definition environment."""
from values import SchemeError


class Environment(dict):
    def __init__(self, bindings=(), parent=None):
        super().__init__(bindings)
        self.parent = parent

    def lookup(self, name):
        scope = self
        while scope is not None:
            if name in scope:
                return scope[name]
            scope = scope.parent
        raise SchemeError(f"unbound symbol: {name}")
