from sqlalchemy.orm import Session

from src.models import AssetExchangeModel
from src.schemas import AssetExchangeSchema

from ..adapters import AssetsExchangesAdapter
from ..repositories import CoinsRepository, SourcesRepository
from .coins_s import CoinsService
from .sources_s import SourcesService


class AssetsExchangesService:
    @classmethod
    def create(
        cls, session: Session, obj: AssetExchangeSchema, sync: bool = False
    ) -> AssetExchangeModel:
        """
        Создание записи о активе на основе схемы данных

        ...

        Params
        ------
        `obj` : AssetExchangeSchema
            Схема данных актива
        `sync` : bool
            Флаг для синхронизации.
            Синхронизация означает создание связанных объектов при их отсутствии
            Default: False

        Returns
        -------
        AssetExchangeModel
            Модель актива в БД

        Raises
        ------
        Exception
            - Возникает в случае, если флаг `sync` установлен в False
              и связанный объект не существует
        """

        model_ = AssetsExchangesAdapter.to_model(obj)

        _source = SourcesRepository.get_by_name(session=session, name=obj.meta.source)
        _coin = CoinsRepository.get_by_symbol(session=session, symbol=obj.asset.symbol)

        if _source is None:
            if not sync:
                raise Exception(f"Отсутствует источник {obj.meta.source!r}")

            _source = SourcesService.create(session=session, obj=obj.meta)

        if _coin is None:
            if not sync:
                raise Exception(f"Отсутствует токен {obj.asset.symbol!r}")

            _coin = CoinsService.create(session=session, obj=obj.asset)

        model_.source = _source
        model_.coin = _coin

        session.add(model_)

        session.commit()

        return model_
