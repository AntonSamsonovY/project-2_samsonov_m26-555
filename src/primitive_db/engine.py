import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import create_table, drop_table, insert, select, update
from primitive_db.parser import (
    parse_condition,
    parse_set_clause,
    parse_values,
)
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def welcome():
    """Показать приветствие и доступные команды."""
    print("Примитивная база данных")
    print("Команды:")
    print("  create_table <имя> <колонка:тип> ... — создать таблицу")
    print("  drop_table <имя> — удалить таблицу")
    print("  list_tables — показать список таблиц")
    print("  insert into <имя> values (...) — добавить запись")
    print("  select from <имя> [where колонка = значение] — показать записи")
    print("  update <имя> set колонка = значение where условие — изменить записи")
    print("  help — показать справку")
    print("  exit — выйти")


def handle_update(command):
    """Проверить команду изменения и сохранить обновлённые записи."""
    parts = shlex.split(command, posix=False)

    if len(parts) < 4 or parts[2] != "set":
        raise ValueError(
            "Формат: update <имя> set колонка = значение "
            "where колонка = значение"
        )

    try:
        where_index = parts.index("where", 3)
    except ValueError as error:
        raise ValueError("Для update обязательно условие where.") from error

    table_name = parts[1]
    set_clause = parse_set_clause(" ".join(parts[3:where_index]))
    where_clause = parse_condition(" ".join(parts[where_index + 1:]))

    metadata = load_metadata("db_meta.json")

    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует.")

    schema = dict(column.split(":") for column in metadata[table_name])
    types = {"int": int, "str": str, "bool": bool}

    for clause in (set_clause, where_clause):
        for column, value in clause.items():
            if column not in schema:
                raise ValueError(f"Колонка '{column}' не существует.")

            if type(value) is not types[schema[column]]:
                raise ValueError(
                    f"Колонка '{column}' ожидает тип '{schema[column]}'."
                )

    table_data = load_table_data(table_name)
    updated_data = update(table_data, set_clause, where_clause)
    save_table_data(table_name, updated_data)
    print("Команда изменения выполнена.")


def run():
    """Запустить цикл ввода команд."""
    welcome()

    while True:
        command = prompt.string("Введите команду: ").strip()

        if not command:
            continue

        try:
            parts = shlex.split(command)
            if not parts:
                continue

            action = parts[0]

            if action == "exit":
                print("До свидания!")
                break
            elif action == "help":
                welcome()
            elif action == "create_table":
                if len(parts) < 3:
                    raise ValueError(
                        "Формат: create_table <имя> <колонка:тип> ..."
                    )

                metadata = load_metadata("db_meta.json")
                create_table(metadata, parts[1], parts[2:])
                save_metadata("db_meta.json", metadata)
                print(f"Таблица '{parts[1]}' создана.")
            elif action == "drop_table":
                if len(parts) != 2:
                    raise ValueError("Формат: drop_table <имя>")

                metadata = load_metadata("db_meta.json")
                drop_table(metadata, parts[1])
                save_metadata("db_meta.json", metadata)
                print(f"Таблица '{parts[1]}' удалена.")
            elif action == "list_tables":
                metadata = load_metadata("db_meta.json")

                if not metadata:
                    print("Таблиц пока нет.")
                else:
                    for table_name in metadata:
                        print(f"  {table_name}")
            elif action == "insert":
                insert_parts = command.split(maxsplit=4)

                if (
                    len(insert_parts) != 5
                    or insert_parts[1] != "into"
                    or insert_parts[3] != "values"
                ):
                    raise ValueError(
                        "Формат: insert into <имя> values (...)"
                    )

                table_name = insert_parts[2]
                values = parse_values(insert_parts[4])
                metadata = load_metadata("db_meta.json")
                table_data = insert(metadata, table_name, values)
                save_table_data(table_name, table_data)
                print(
                    f"Запись добавлена в '{table_name}', "
                    f"ID: {table_data[-1]['ID']}."
                )
            elif action == "select":
                select_parts = command.split(maxsplit=3)

                if len(select_parts) < 3 or select_parts[1] != "from":
                    raise ValueError(
                        "Формат: select from <имя> "
                        "[where колонка = значение]"
                    )

                table_name = select_parts[2]
                metadata = load_metadata("db_meta.json")

                if table_name not in metadata:
                    raise ValueError(
                        f"Таблица '{table_name}' не существует."
                    )

                column_names = [
                    column.split(":")[0]
                    for column in metadata[table_name]
                ]
                where_clause = None

                if len(select_parts) == 4:
                    condition_parts = select_parts[3].split(maxsplit=1)

                    if (
                        len(condition_parts) != 2
                        or condition_parts[0] != "where"
                    ):
                        raise ValueError(
                            "Формат условия: where колонка = значение"
                        )

                    where_clause = parse_condition(condition_parts[1])

                    for column in where_clause:
                        if column not in column_names:
                            raise ValueError(
                                f"Колонка '{column}' не существует."
                            )

                table_data = load_table_data(table_name)
                rows = select(table_data, where_clause)
                table = PrettyTable()
                table.field_names = column_names

                for row in rows:
                    table.add_row([row[column] for column in column_names])

                print(table)
            elif action == "update":
                handle_update(command)
            else:
                print("Неизвестная команда. Введите help.")
        except ValueError as error:
            print(f"Ошибка: {error}")