from src.models import SourceModel
from src.schemas import AssetExchangeMetaSchema


class SourcesAdapter:
    @classmethod
    def to_model(cls, schema: AssetExchangeMetaSchema) -> SourceModel:
        """
        Создание модели источника (биржи) БД из схемы мета-информации о маркете

        ...

        Params
        ------
        `schema` : AssetExchangeMetaSchema
            Схема мета-информации маркета актива
        
        Returns
        -------
        SourceModel
            Модель источника
        """
        
        return SourceModel(name=schema.source)
