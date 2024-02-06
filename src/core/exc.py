class AppError(Exception):
    """
    Базовая ошибка приложения
    """

    ...


class CalledMethodIntervalError(AppError):
    """
    Ошибка обращения к методу через время раньше положенного интервала
    """

    ...
