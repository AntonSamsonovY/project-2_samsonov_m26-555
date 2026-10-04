import time
from functools import wraps

import prompt


def handle_db_errors(func):
    """Обработать ошибки при выполнении операции базы данных."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as error:
            print(f"Ошибка: отсутствует ключ {error}.")
        except ValueError as error:
            print(f"Ошибка значения: {error}")
        except FileNotFoundError as error:
            print(f"Файл не найден: {error.filename}")
        except Exception as error:
            print(f"Непредвиденная ошибка: {error}")

        return None

    return wrapper


def confirm_action(action_name):
    """Запросить подтверждение перед выполнением действия."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = prompt.string(
                f"Подтвердите действие '{action_name}' (y/n): "
            ).strip().lower()

            if answer != "y":
                print("Действие отменено.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Вывести время выполнения функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(
            f"Функция {func.__name__} выполнилась "
            f"за {elapsed:.3f} секунд"
        )
        return result

    return wrapper
