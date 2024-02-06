import logging
from typing import Optional

from src.schemas import AssetExchangeSchema

from .exchanges.base import BaseExchange

logger = logging.getLogger("StocksCollector")


class StocksCollector:
    def __init__(self, *exchange: BaseExchange) -> None:
        self._exchanges = exchange

    def collect(self, codes: list[str]) -> list[AssetExchangeSchema]:
        """
        Сбор данных о токенах с бирж

        ...

        Params
        ------
        `codes` : list[str]
            Список кодов токенов

        Returns
        -------
        list[AssetExchangeSchema]
            Список полученных данных о токенах

        Notes
        -----
        Если активной биржи не найдено,
        то всегда будет возвращаться пустой список

        !important
        Все данные о токенах собираются относительно другого токена - USDT
        """

        logger.debug("Старт сбора данных о коинах с бирж")

        active_exchange: Optional[BaseExchange] = None

        for e in self._exchanges:
            if e.provider.is_active:
                active_exchange = e
                break

        if not active_exchange:
            logger.critical("Не найдено активной биржи")

            return []

        logger.debug(f"Найдена активная биржа: {active_exchange.name}")

        return active_exchange.stocks(codes=codes)
