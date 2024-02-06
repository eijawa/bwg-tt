from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from src.models import AssetExchangeModel, CoinModel, SourceModel


class AssetsExchangesRepository:
    @classmethod
    def latest(cls, session: Session) -> Optional[AssetExchangeModel]:
        """
        Получение самого последнего объекта актива из БД
        """

        stmt = select(AssetExchangeModel).order_by(desc(AssetExchangeModel.rt)).limit(1)

        return session.scalar(stmt)

    @classmethod
    def latest_assets_by_source(
        cls, session: Session, source_name: str, symbols: list[str]
    ) -> list[AssetExchangeModel]:
        """
        Получение списка самых последних токенов 
        с фильтрацией по кодам 
        из конкретного источника

        ...

        Params
        ------
        `source_name` : str
            Название источника
        `symbols` : list[str]
            Список кодов токенов

        Returns
        -------
        list[AssetExchangeModel]
            Список последних активов
        """

        stmt = (
            select(AssetExchangeModel)
            .distinct(CoinModel.symbol)
            .join(SourceModel)
            .join(CoinModel)
            .where(SourceModel.name == source_name)
            .where(CoinModel.symbol.in_(symbols))
            .order_by(CoinModel.symbol, desc(AssetExchangeModel.rt))
        )

        return session.scalars(stmt).all()


# SELECT DISTINCT ON (coin_id) * FROM assets_exchanges
# WHERE source_id = 1 AND coin_id IN (2,3,4)
# ORDER BY coin_id ASC, rt DESC


# SELECT DISTINCT ON (ct.symbol) * FROM assets_exchanges aet
# JOIN (
# 	SELECT id, name FROM sources
# ) st
# ON aet.source_id = st.id
# JOIN (
# 	SELECT id, symbol FROM coins
# ) ct
# ON aet.coin_id = ct.id
# WHERE st.name = 'coingecko' AND ct.symbol IN ('btc','eth')
# ORDER BY ct.symbol ASC, rt DESC
