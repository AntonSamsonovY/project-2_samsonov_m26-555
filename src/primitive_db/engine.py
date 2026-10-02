import shlex

import prompt

from primitive_db.core import create_table
from primitive_db.utils import load_metadata, save_metadata


def welcome():
    """Показать приветствие и доступные команды."""
    print("Примитивная база данных")
    print("Команды:")
    print("  create_table <имя> <колонка:тип> ... — создать таблицу")
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
            else:
                print("Неизвестная команда. Введите help.")
        except ValueError as error:
            print(f"Ошибка: {error}")