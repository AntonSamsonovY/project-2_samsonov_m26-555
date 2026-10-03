import json


def parse_values(text):
    """Разобрать значения в круглых скобках."""
    text = text.strip()

    if not text.startswith("(") or not text.endswith(")"):
        raise ValueError("Значения должны быть в круглых скобках.")

    try:
        values = json.loads(f"[{text[1:-1]}]")
    except json.JSONDecodeError as error:
        raise ValueError(
            'Некорректные значения. Пример: ("Антон", 28, true)'
        ) from error

    for value in values:
        if type(value) not in (int, str, bool):
            raise ValueError("Допустимы только int, str и bool.")

    return values