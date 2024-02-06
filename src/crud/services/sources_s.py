from sqlalchemy.orm import Session

from src.models import SourceModel
from src.schemas import AssetExchangeMetaSchema

from ..adapters import SourcesAdapter


class SourcesService:
    @classmethod
    def create(cls, session: Session, obj: AssetExchangeMetaSchema) -> SourceModel:
        """
        Создание записи о источнике из схемы данных
        """

        model_ = SourcesAdapter.to_model(obj)

        session.add(model_)

        session.commit()

        return model_
