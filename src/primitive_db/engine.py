import shlex

import prompt

from primitive_db.core import create_table, drop_table, insert
from primitive_db.parser import parse_values
from primitive_db.utils import (
    load_metadata,
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
    print("  help — показать справку")
    print("  exit — выйти")


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
            else:
                print("Неизвестная команда. Введите help.")
        except ValueError as error:
            print(f"Ошибка: {error}")