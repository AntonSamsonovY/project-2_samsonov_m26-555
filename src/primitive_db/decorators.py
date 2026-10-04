import time
from functools import wraps

import prompt


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
