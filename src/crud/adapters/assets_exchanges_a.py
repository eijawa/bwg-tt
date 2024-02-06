from decimal import Decimal

from src.models import AssetExchangeModel
from src.schemas import AssetExchangeMetaSchema, AssetExchangeSchema, AssetInfoSchema


class AssetsExchangesAdapter:
    @classmethod
    def to_model(cls, schema: AssetExchangeSchema) -> AssetExchangeModel:
        """
        Преобразование схемы данных,
        полученных в процессе подтягивания данных с бирж,
        в модель БД

        ...

        Params
        ------
        `schema` : AssetExchangeSchema
            Данные с биржи

        Returns
        -------
        AssetExchangeModel
            Модель БД
        """

        return AssetExchangeModel(
            value=schema.quote.value, rt=schema.meta.rt, lut=schema.meta.lut
        )

    @classmethod
    def to_schema(cls, model: AssetExchangeModel) -> AssetExchangeSchema:
        """
        Преобразование модели БД в схему данных с биржи

        ...

        Params
        ------
        `model` : AssetExchangeModel
            Модель БД

        Returns
        -------
        AssetExchangeSchema
            Схема данных с биржи
        """

        return AssetExchangeSchema(
            asset=AssetInfoSchema(symbol=model.coin.symbol, value=Decimal("1.0")),
            quote=AssetInfoSchema(symbol="usdt", value=Decimal(model.value)),
            meta=AssetExchangeMetaSchema(
                source=model.source.name, rt=model.rt, lut=model.lut
            ),
        )
