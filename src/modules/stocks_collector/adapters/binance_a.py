from decimal import Decimal

from src.schemas import AssetExchangeMetaSchema, AssetExchangeSchema, AssetInfoSchema

from .base import BaseAdapter


class BinanceAdapter(BaseAdapter):
    def convert_to_asset_exchange(
        self, source: str, data: dict
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
            Полученные данные с биржи

        Returns
        -------
        list[AssetExchangeSchema]
            Схема актива
        """

        if not data["data"]:
            raise ValueError("Не найдено данных для преобразования")

        exchanges = []

        for d in data["data"]:
            name = d["symbol"].removesuffix("USDT")

            asset = AssetInfoSchema(
                symbol=name.lower(), value=Decimal("1.0")
            )

            # См. docs/SDF/Конвертация монет в валюту.md
            quote = AssetInfoSchema(
                symbol="usdt", value=Decimal(str(d["price"]))
            )

            meta = AssetExchangeMetaSchema(
                source=source, rt=data["rt"]
            )

            asset_exchange = AssetExchangeSchema(asset=asset, quote=quote, meta=meta)
            exchanges.append(asset_exchange)

        return exchanges
