"""External representation and display representation of Scheme values."""
import json
from values import NIL, Pair, Symbol, Closure, Builtin


def format_value(value, display=False):
    if value is True:
        return "#t"
    if value is False:
        return "#f"
    if value is NIL:
        return "()"
    if isinstance(value, Symbol):
        return str(value)
    if isinstance(value, str):
        return value if display else json.dumps(value, ensure_ascii=False)
    if isinstance(value, Pair):
        parts = []
        current = value
        while isinstance(current, Pair):
            parts.append(format_value(current.car, display))
            current = current.cdr
        suffix = "" if current is NIL else " . " + format_value(current, display)
        return "(" + " ".join(parts) + suffix + ")"
    if isinstance(value, (Closure, Builtin)):
        return "#<procedure>"
    return str(value)
