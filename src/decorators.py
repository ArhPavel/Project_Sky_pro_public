import functools
from typing import Any, Optional


def log(filename: Optional[str] = None) -> Any:
    """Декоратор, который будет автоматически логировать начало и
    конец выполнения    функции, а также ее результаты или возникшие
     ошибки"""
    def decorator(func: Any) -> Any:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            name = func.__name__

            def write(msg: str) -> None:
                if filename:
                    f = open(filename, "a")
                    f.write(msg + "\n")
                    f.close()
                else:
                    print(msg)

            try:
                result = func(*args, **kwargs)
                write(f"{name} ok")
                return result
            except Exception as e:
                inputs = f"{args!r}, {kwargs!r}"
                write(f"{name} error: {type(e).__name__}. Inputs: {inputs}")
                raise

        return wrapper

    return decorator
