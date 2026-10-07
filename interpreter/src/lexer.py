"""Tokenize comments, parentheses, quotation and escaped strings."""
from dataclasses import dataclass
from values import SchemeError


@dataclass(frozen=True)
class StringToken:
    value: str


def tokenize(source):
    tokens = []
    position = 0
    escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
    while position < len(source):
        char = source[position]
        if char.isspace():
            position += 1
        elif char == ";":
            end = source.find("\n", position)
            position = len(source) if end < 0 else end + 1
        elif char in "()'":
            tokens.append(char)
            position += 1
        elif char == '"':
            position += 1
            buffer = []
            while position < len(source) and source[position] != '"':
                char = source[position]
                if char == "\\":
                    position += 1
                    if position >= len(source) or source[position] not in escapes:
                        raise SchemeError("invalid string escape")
                    char = escapes[source[position]]
                buffer.append(char)
                position += 1
            if position >= len(source):
                raise SchemeError("unterminated string")
            tokens.append(StringToken("".join(buffer)))
            position += 1
        else:
            start = position
            while (position < len(source) and not source[position].isspace()
                   and source[position] not in "()';\""):
                position += 1
            tokens.append(source[start:position])
    return tokens
