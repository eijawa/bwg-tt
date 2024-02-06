from src.modules.stocks_collector.providers import BinanceRESTAPIProvider


def test_retrieve() -> None:
    provider = BinanceRESTAPIProvider()

    data = provider.retrieve(["BTC", "ETH"])

    assert data
    assert data["version"] == "v3"
    assert data["data"]
