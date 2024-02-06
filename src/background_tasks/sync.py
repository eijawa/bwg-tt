from datetime import datetime, timedelta
from threading import Thread

from src.core import settings
from src.core.db import SessionLocal
from src.crud.services import AssetsExchangesService
from src.modules.stocks_collector import StocksCollector
from src.modules.stocks_collector.adapters import BinanceAdapter, CoinGeckoAdapter
from src.modules.stocks_collector.exchanges import BinanceExchange, CoinGeckoExchange
from src.modules.stocks_collector.providers import (
    BinanceRESTAPIProvider,
    CoinGeckoRESTAPIProvider,
)


def task() -> None:
    """
    Бэкграунд задача по получению и сохранению в БД информации по токенам
    """

    stocks_collector = StocksCollector(
        BinanceExchange(provider=BinanceRESTAPIProvider(), adapter=BinanceAdapter()),
        CoinGeckoExchange(
            provider=CoinGeckoRESTAPIProvider(), adapter=CoinGeckoAdapter()
        ),
    )

    interval = timedelta(seconds=settings.UPDATE_INTERVAL_SECONDS)
    lct = datetime.now() - interval

    while True:
        now_ = datetime.now()
        passed_ = now_ - lct

        if passed_ < interval:
            continue
        else:
            lct = now_

        data = stocks_collector.collect(codes=settings.COLLECTIBLE_COINS_SYMBOLS)

        # Чтобы не открывать новое подключение
        if not data:
            continue

        with SessionLocal() as session:
            for a_e in data:
                AssetsExchangesService.create(session=session, obj=a_e, sync=True)


THREAD = Thread(target=task, daemon=True)
