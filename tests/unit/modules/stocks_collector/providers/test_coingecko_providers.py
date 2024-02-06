from src.core import settings  # noqa: F401
from src.modules.stocks_collector.providers import CoinGeckoRESTAPIProvider

# TODO: Заменить этот провайдер на фикстуру


def test_init() -> None:
    provider = CoinGeckoRESTAPIProvider()

    assert isinstance(provider, CoinGeckoRESTAPIProvider)


def test_retrieve() -> None:
    provider = CoinGeckoRESTAPIProvider()

    data = provider.retrieve(["binance"])

    assert data
    assert data["version"] == "v3"
    assert data["data"]
