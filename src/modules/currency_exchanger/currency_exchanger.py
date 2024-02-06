import logging
from decimal import Decimal

import httpx

from src.core import settings

logger = logging.getLogger("CurrencyExchanger")


class _CurrencyExchanger:
    """
    Класс для конвертации валют между собой

    ...

    Notes
    -----
    Данные о конвертации основаны на API сервисе FreeCurrency.
    При первом запуске производится загрузка данных об обмене для `default_currency`
    """

    def __init__(self, default_currency: str) -> None:
        """
        Params
        ------
        `default_currency` : str
            Валюта по-умолчанию
        """

        self.__default_currency = default_currency

        # Объект для кэширования полученных данных
        self.__EXCHANGES: dict[str, dict[str, Decimal]] = {}

        self.__load_exchanges(self.__default_currency)

    def exchange(self, base_currency: str, value: Decimal, currency: str) -> Decimal:
        """
        Перевод из одной валюты в другую

        ...

        Params
        ------
        `base_currency` : str
            Валюта, из которой осуществляется перевод
        `value` : Decimal
            Количество валюты для перевода
        `currency` : str
            Валюта, в которую осуществляется перевод

        Returns
        -------
        Decimal
            Итоговое количество валюты после перевода

        Raises
        ------
        AssertionError
            - Если указаная валюта не поддерживается
        """

        assert base_currency in self.currencies
        assert currency in self.currencies

        logger.debug(
            f"Перевод {value} [{base_currency}] -> [{currency}]"
        )

        return value * self.rate(base_currency=base_currency, currency=currency)

    def rate(self, base_currency: str, currency: str) -> Decimal:
        """
        Получение соотношения для обмена одной валюты к другой.
        1:N

        ...

        Params
        ------
        `base_currency` : str
            Валюта, из которой осуществляется перевод
        `currency` : str
            Валюта, в которую осуществляется перевод

        Returns
        -------
        Decimal
            Соотношение для перевода валюты

        Raises
        ------
        AssertionError
            - Если указаная валюта не поддерживается
        """

        assert base_currency in self.currencies
        assert currency in self.currencies

        if base_currency not in self.__EXCHANGES:
            self.__load_exchanges(base_currency=base_currency)

        return self.__EXCHANGES[base_currency][currency]

    @property
    def currencies(self) -> set[str]:
        """
        Множество поддерживаемых валют для конвертации
        """

        return self.__EXCHANGES[self.__default_currency].keys()

    def __load_exchanges(self, base_currency: str) -> None:
        """
        Подгрузка данных для конвертации относительно валюты `base_currency`
        """

        r = httpx.get(
            "https://api.freecurrencyapi.com/v1/latest",
            params={
                "apikey": settings.FREECURRENCY.API_KEY,
                "base_currency": base_currency.upper(),
            },
        )

        if r.status_code != 200:
            raise Exception(r.text)

        self.__EXCHANGES[base_currency] = {
            k.lower(): Decimal(str(v)) for k, v in r.json()["data"].items()
        }


CurrencyExchanger = _CurrencyExchanger(default_currency=settings.DEFAULT_CURRENCY)
