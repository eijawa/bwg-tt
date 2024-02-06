import logging

from src.core import exc as AppExceptions
from src.schemas import AssetExchangeSchema

from .base import BaseExchange

logger = logging.getLogger("CoinGeckoExchange")


class CoinGeckoExchange(BaseExchange):
    name = "coingecko"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Кэш-мапы нужны, тк CoinGecko использует не стандартные коды токенов, 
        # а их собственный id в своей системе

        ## Кэш-мапа для преобразования кодов в id CoinGecko
        self._SYMBOLS_TO_IDS_MAP = {}

        ## Кэш-мапа для преобразования id CoinGecko в коды
        self._IDS_TO_SYMBOLS_MAP = {}

        self.__load_maps()

    def stocks(self, codes: list[str]) -> list[AssetExchangeSchema]:
        logger.debug(f"Получение рынка монет для биржи {self.name}")

        ids = self.__map_symbols_to_ids(symbols=codes)

        try:
            raw_data = self._provider.retrieve(codes=ids)

            data = self._adapter.convert_to_asset_exchange(
                source=self.name,
                data=raw_data,
                ids_to_symbols_map=self._IDS_TO_SYMBOLS_MAP,
            )
        except (AppExceptions.CalledMethodIntervalError, Exception) as e:
            if isinstance(e, AppExceptions.CalledMethodIntervalError):
                logger.warning(str(e))

            data = []

        return data

    def __map_symbols_to_ids(self, symbols: list[str]) -> list[str]:
        """
        Преобразование списка кодов в список id CoinGecko

        ...

        Params
        ------
        `symbols` : list[str]
            Список кодов токенов

        Returns
        -------
        list[str]
            Список id CoinGecko

        Notes
        -----
        Это safe-method, то есть он вернёт результат даже в случае, 
        если отсутствия на бирже нужных токенов.
        Хотя это и будет пустой список
        """
        
        logger.debug(
            f"Преобразование кодов {symbols!r} в идентификаторы биржи {self.name}"
        )

        ids = []

        for s in symbols:
            id_ = self._SYMBOLS_TO_IDS_MAP.get(s.lower(), "")

            if id_:
                ids.append(id_)

        logger.debug(f"Результат преобразования: {ids!r}")

        return ids

    def __load_maps(self) -> None:
        market = self._provider.market()

        for m in market:
            # Выбираем токены без платформы, чтобы избежать повторов данных
            if m["platforms"]:
                continue

            self._IDS_TO_SYMBOLS_MAP[m["id"]] = m["symbol"]
            self._SYMBOLS_TO_IDS_MAP[m["symbol"]] = m["id"]
