import prompt


def welcome():
    """Показать приветствие и доступные команды."""
    print("Примитивная база данных")
    print("Команды:")
    print("  help — показать справку")
    print("  exit — выйти")


def run():
    """Запустить цикл ввода команд."""
    welcome()

    while True:
        command = prompt.string("Введите команду: ").strip()

        if command == "exit":
            print("До свидания!")
            break
        elif command == "help":
            welcome()
        elif not command:
            continue
        else:
            print("Неизвестная команда. Введите help.")