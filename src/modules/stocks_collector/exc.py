class StocksCollectorError(Exception):
    """
    Общий класс для ошибок модуля
    """

    ...


class ExchangeError(StocksCollectorError):
    """
    Общий класс для ошибок биржи
    """

    ...


class ProviderError(StocksCollectorError):
    """
    Общий класс для ошибок получателя
    """

    ...


class TooManyRequestError(ProviderError):
    """
    Ошибка обозначает превышение доступного лимита на количество запросов
    """

    ...


class AdapterError(StocksCollectorError):
    """
    Общий класс для ошибок адаптера
    """

    ...
