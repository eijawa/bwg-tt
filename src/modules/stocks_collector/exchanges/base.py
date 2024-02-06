import logging
from abc import abstractmethod
from typing import ClassVar

from src.schemas import AssetExchangeSchema

from ..adapters.base import BaseAdapter
from ..providers.base import BaseProvider

logger = logging.getLogger("Exchange")


class Exchange:
    name: ClassVar[str]

    @abstractmethod
    def stocks(self, codes: list[str]) -> list[AssetExchangeSchema]: ...


class BaseExchange(Exchange):
    """
    Базовый класс для Биржи
    """

    def __init__(self, provider: BaseProvider, adapter: BaseAdapter) -> None:
        logger.debug(
            f"Инициализация биржи {self.name}:\nПровайдер:{provider.__class__.__name__}\nАдаптер:{adapter.__class__.__name__}"
        )

        self._provider = provider
        self._adapter = adapter

    @property
    def provider(self) -> BaseProvider:
        return self._provider
