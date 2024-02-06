from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import SourceModel


class SourcesRepository:
    @classmethod
    def get(cls, session: Session, id_: int) -> Optional[SourceModel]:
        """
        Получение источника по `id`
        """

        stmt = select(SourceModel).where(SourceModel.id == id_)
        
        return session.scalar(stmt)

    @classmethod
    def get_by_name(cls, session: Session, name: str) -> Optional[SourceModel]:
        """
        Получение источника по названию
        """

        stmt = select(SourceModel).where(SourceModel.name == name)
        
        return session.scalar(stmt)
