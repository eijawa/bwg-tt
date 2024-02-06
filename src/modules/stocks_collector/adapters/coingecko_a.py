from decimal import Decimal

from src.schemas import AssetExchangeMetaSchema, AssetExchangeSchema, AssetInfoSchema

from .base import BaseAdapter


class CoinGeckoAdapter(BaseAdapter):
    def convert_to_asset_exchange(
        self, source: str, data: dict, ids_to_symbols_map: dict
    ) -> list[AssetExchangeSchema]:
        """
        Преобразование полученных данных в схему актива,
        используемую дальше в приложении

        ...

        Params
        ------
        `source` : data
            Источник полученных данных
        `data` : dict
            Полученные данные с CoinGecko
        `ids_to_symbols_map` : dict
            Таблица для сопоставления id CoinGecko с кодами токенов

        Returns
        -------
        list[AssetExchangeSchema]
            Схема актива
        """

        if not data["data"]:
            raise ValueError("Не найдено данных для преобразования")

        exchanges = []

        for asset_name, quote_data in data["data"].items():
            asset = AssetInfoSchema(
                symbol=ids_to_symbols_map[asset_name], value=Decimal("1.0")
            )

            # См. docs/SDF/Конвертация монет в валюту.md
            quote = AssetInfoSchema(
                symbol="usdt", value=Decimal(str(quote_data["usd"]))
            )

            meta = AssetExchangeMetaSchema(
                source=source, rt=data["rt"], lut=quote_data["last_updated_at"]
            )

            asset_exchange = AssetExchangeSchema(asset=asset, quote=quote, meta=meta)
            exchanges.append(asset_exchange)

        return exchanges
