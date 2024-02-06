import logging
from datetime import datetime, timedelta

import httpx

from src.core.utils.deco import interval_limited

from .. import exc as ModuleExceptions
from .base import RESTAPIProvider

logger = logging.getLogger("BinanceRESTAPIProvider")


class BinanceRESTAPIProvider(RESTAPIProvider):
    BASE_URL = "https://api.binance.com/api/"

    LOGGER = logger

    def __init__(self, api_version: str = "v3") -> None:
        logger.debug(
            f"Инициализация REST API провайдера Binance версии API{api_version}"
        )

        super().__init__(api_version=api_version)

    # См. docs/SDF/Binance.md
    @interval_limited(interval=timedelta(seconds=60))
    def retrieve(self, codes: list[str]) -> dict:
        r = self.client.get("/ticker/price", params={
            "symbols": f"[{','.join(map(lambda c: '\"' + c.upper() + 'USDT' + '\"', codes))}]"
        })

        self._check_exc(r)

        return {"version": self._api_version, "data": r.json(), "rt": datetime.now()}

    def ping(self) -> bool:
        return self.client.get("/ping").status_code == 200

    def market(self) -> dict:
        """
        Получение информации по текущему состоянию маркета коинов.
        Список всех коинов на платформе Binance
        """

        r = self.client.get("/exchangeInfo")

        self._check_exc(r)

        return r.json()

    def _construct_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.BASE_URL + self._api_version,
        )
