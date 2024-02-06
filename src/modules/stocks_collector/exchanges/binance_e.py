import logging

from src.core import exc as AppExceptions
from src.schemas import AssetExchangeSchema

from .base import BaseExchange

logger = logging.getLogger("BinanceExchange")


class BinanceExchange(BaseExchange):
    name = "binance"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Множество для указания поддерживаемых токенов для запроса
        self._SUPPORTED_CODES = set(self.__get_supported_codes())

    def stocks(self, codes: list[str]) -> list[AssetExchangeSchema]:
        logger.debug(f"Получение рынка монет для биржи {self.name}")

        logger.debug(f"Очистка кодов: {codes!r}")

        # Очистка невозможных для получения информации токенов,
        # тк иначе будет ошибка запроса
        supported_codes = [c.upper() for c in codes if c.upper() in self._SUPPORTED_CODES]

        logger.debug(f"Очищенные коды: {supported_codes!r}")

        try:
            raw_data = self._provider.retrieve(codes=supported_codes)

            data = self._adapter.convert_to_asset_exchange(
                source=self.name,
                data=raw_data,
            )
        except (AppExceptions.CalledMethodIntervalError, Exception) as e:
            if isinstance(e, AppExceptions.CalledMethodIntervalError):
                logger.warning(str(e))

            data = []

        return data

    def __get_supported_codes(self):
        for s in self._provider.market()["symbols"]:
            if s["quoteAsset"] == "USDT":
                yield s["baseAsset"]
