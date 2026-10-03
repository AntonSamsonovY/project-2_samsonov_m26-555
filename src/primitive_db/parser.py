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

def parse_condition(text):
    """Разобрать условие вида колонка = значение."""
    parts = text.split("=", maxsplit=1)

    if len(parts) != 2:
        raise ValueError("Формат условия: колонка = значение")

    column = parts[0].strip()
    value_text = parts[1].strip()

    if not column.isidentifier():
        raise ValueError("Некорректное имя колонки.")

    values = parse_values(f"({value_text})")

    if len(values) != 1:
        raise ValueError("В условии должно быть одно значение.")

    return {column: values[0]}