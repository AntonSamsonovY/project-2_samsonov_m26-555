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