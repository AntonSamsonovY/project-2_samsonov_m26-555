VALID_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    """Добавить описание новой таблицы в метаданные."""
    if not table_name.isidentifier():
        raise ValueError("Некорректное имя таблицы.")

    if table_name in metadata:
        raise ValueError(f"Таблица '{table_name}' уже существует.")

    if not columns:
        raise ValueError("Укажите хотя бы одну колонку.")

    schema = ["ID:int"]
    column_names = {"ID"}

    for column in columns:
        parts = column.split(":")
        if len(parts) != 2:
            raise ValueError(f"Ожидается имя:тип, получено '{column}'.")

        name, column_type = parts

        if not name.isidentifier():
            raise ValueError(f"Некорректное имя колонки '{name}'.")

        if name in column_names:
            raise ValueError(f"Колонка '{name}' уже существует.")

        if column_type not in VALID_TYPES:
            raise ValueError(f"Неизвестный тип '{column_type}'.")

        column_names.add(name)
        schema.append(column)

    metadata[table_name] = schema
    return metadata


def drop_table(metadata, table_name):
    """Удалить описание существующей таблицы."""
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует.")

    del metadata[table_name]
    return metadata