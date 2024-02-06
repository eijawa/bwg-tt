from src.models import CoinModel
from src.schemas import AssetInfoSchema


class CoinsAdapter:
    @classmethod
    def to_model(cls, schema: AssetInfoSchema) -> CoinModel:
        """
        Преобразование схемы актива в модель токена БД

        ...

        Params
        ------
        `schema` : AssetInfoSchema
            Схема актива

        Returns
        -------
        CoinModel
            Модель токена
        """
        
        return CoinModel(symbol=schema.symbol, name=schema.name)
