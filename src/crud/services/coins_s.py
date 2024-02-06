from sqlalchemy.orm import Session

from src.models import CoinModel
from src.schemas import AssetInfoSchema

from ..adapters import CoinsAdapter


class CoinsService:
    @classmethod
    def create(cls, session: Session, obj: AssetInfoSchema) -> CoinModel:
        """
        Создание записи о токене из схемы данных
        """

        model_ = CoinsAdapter.to_model(obj)

        session.add(model_)

        session.commit()

        return model_
