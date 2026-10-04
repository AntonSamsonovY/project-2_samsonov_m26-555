import time
from copy import deepcopy
from functools import wraps

import prompt


def create_cacher():
    """Создать замыкание для хранения результатов и очистки кеша."""
    cache = {}

    def cache_result(key, value_func):
        """Вычислить результат один раз; ошибки не кешировать."""
        if key in cache:
            print("Результат получен из кеша.")
            return deepcopy(cache[key])

        result = value_func()
        if result is not None:
            cache[key] = deepcopy(result)

        return result

    def clear_cache():
        """Сбросить результаты после изменения данных."""
        cache.clear()

    cache_result.clear = clear_cache
    return cache_result


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
            answer = (
                prompt.string(f"Подтвердите действие '{action_name}' (y/n): ")
                .strip()
                .lower()
            )

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
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд")
        return result

    return wrapper
