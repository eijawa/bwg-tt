import logging
from datetime import datetime, timedelta

import httpx

from src.core import settings
from src.core.utils.deco import interval_limited

from .base import RESTAPIProvider

logger = logging.getLogger("CoinGeckoRESTAPIProvider")


class CoinGeckoRESTAPIProvider(RESTAPIProvider):
    BASE_URL = "https://api.coingecko.com/api/"

    LOGGER = logger

    def __init__(self, api_version: str = "v3") -> None:
        self.LOGGER.debug(
            f"Инициализация REST API провайдера CoinGecko версии API{api_version}"
        )

        super().__init__(api_version=api_version)

        self.__api_key = settings.COINGECKO.API_KEY

    # См. docs/SDF/CoinGecko.md
    @interval_limited(interval=timedelta(seconds=60))
    def retrieve(self, codes: list[str]) -> dict:
        r = self.client.get(
            "/simple/price",
            params={
                "ids": ",".join(codes),
                "vs_currencies": "usd",
                "precision": "full",
                "include_last_updated_at": True,
            },
        )

        self._check_exc(r)

        return {"version": self._api_version, "data": r.json(), "rt": datetime.now()}

    def ping(self) -> bool:
        return self.client.get("/ping").status_code == 200

    def market(self) -> dict:
        """
        Получение информации по текущему состоянию маркета коинов.
        Список всех коинов на платформе CoinGecko
        """

        r = self.client.get("/coins/list", params={"include_platform": True})

        self._check_exc(r)

        return r.json()

    def _construct_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.BASE_URL + self._api_version,
            params={"x_cg_api_key": self.__api_key},
        )
