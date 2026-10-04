from primitive_db.constants import TYPE_MAP, VALID_TYPES
from primitive_db.decorators import confirm_action, log_time
from primitive_db.utils import load_table_data


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


@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удалить описание существующей таблицы."""
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует.")

    del metadata[table_name]
    return metadata


@log_time
def insert(metadata, table_name, values):
    """Добавить запись с проверкой типов и автоматическим ID."""
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует.")

    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        raise ValueError(f"Ожидается значений: {len(columns)}.")

    record = {}

    for column, value in zip(columns, values):
        name, column_type = column.split(":")

        if type(value) is not TYPE_MAP[column_type]:
            raise ValueError(
                f"Колонка '{name}' ожидает тип '{column_type}'."
            )

        record[name] = value

    table_data = load_table_data(table_name)
    next_id = max((row["ID"] for row in table_data), default=0) + 1
    record = {"ID": next_id, **record}
    table_data.append(record)

    return table_data


@log_time
def select(table_data, where_clause=None):
    """Выбрать все записи или записи по условию равенства."""
    if where_clause is None:
        return table_data.copy()

    return [
        row
        for row in table_data
        if all(
            row.get(column) == value
            for column, value in where_clause.items()
        )
    ]


def update(table_data, set_clause, where_clause):
    """Изменить записи, соответствующие условию."""
    if not set_clause or not where_clause:
        raise ValueError("Укажите изменения и условие.")

    if "ID" in set_clause:
        raise ValueError("Изменять ID нельзя.")

    for row in table_data:
        if all(
            row.get(column) == value
            for column, value in where_clause.items()
        ):
            row.update(set_clause)

    return table_data


@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Вернуть записи, не соответствующие условию удаления."""
    if not where_clause:
        raise ValueError("Для удаления обязательно условие.")

    return [
        row
        for row in table_data
        if not all(
            row.get(column) == value
            for column, value in where_clause.items()
        )
    ]


def info(metadata, table_name):
    """Получить описание таблицы и количество записей."""
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует.")

    table_data = load_table_data(table_name)

    return {
        "name": table_name,
        "columns": metadata[table_name],
        "row_count": len(table_data),
    }
