from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import CoinModel


class CoinsRepository:
    @classmethod
    def get(cls, session: Session, id_: int) -> Optional[CoinModel]:
        """
        Получение токена по `id`
        """

        stmt = select(CoinModel).where(CoinModel.id == id_)

        return session.scalar(stmt)

    @classmethod
    def get_by_symbol(cls, session: Session, symbol: str) -> Optional[CoinModel]:
        """
        Получение токена по коду
        """

        stmt = select(CoinModel).where(CoinModel.symbol == symbol)

        return session.scalar(stmt)
