from datetime import datetime, timedelta
from functools import wraps

from src.core import exc as AppExceptions


def interval_limited(interval: timedelta):
    """
    Декоратор для ограничения вызова функции класса в пределах интервала

    ...

    Params
    ------
    `interval` : timedelta
        Интервал для ограничения вызова функции

    Notes
    -----
    Работает только на методах экземпляра класса.
    Не тестировалось на методах класса
    """

    def _interval_limited(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name_ = f"__{func.__name__}_last_called_time"
            self_ = args[0]

            now_ = datetime.now()

            if getattr(self_, name_, None) is None:
                setattr(self_, name_, now_ - interval)

            passed_ = now_ - getattr(self_, name_)

            if passed_ < interval:
                raise AppExceptions.CalledMethodIntervalError(
                    f"С момента последнего вызова функции {func.__qualname__} прошло: {passed_} < {interval}"
                )
            else:
                setattr(self_, name_, now_)

            return func(*args, **kwargs)

        return wrapper

    return _interval_limited
