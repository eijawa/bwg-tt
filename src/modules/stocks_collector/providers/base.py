from abc import abstractmethod
from logging import Logger
from typing import ClassVar
from weakref import finalize

import httpx

from .. import exc as ModuleExceptions


class Provider:
    @abstractmethod
    def retrieve(self, codes: list[str]) -> dict: ...

    @abstractmethod
    def ping(self) -> bool: ...


class BaseProvider(Provider):
    """
    Базовый класс провайдеров
    """

    def __init__(self) -> None:
        # Финализатор, на случай, если нужно будет что-то уничтожить или обязательно закрыть
        self._finalizer = finalize(self, self._on_destroy)

        self._is_active = None

    @property
    def is_active(self) -> bool:
        """
        Флаг активности провайдера.

        Если провайдером больше пользоваться нельзя,
        то возвращает False
        """

        if self._is_active is None:
            self._is_active = self.ping()

        return self._is_active

    def _on_destroy(self) -> None: ...


class RESTAPIProvider(BaseProvider):
    BASE_URL: ClassVar[str]

    LOGGER: ClassVar[Logger]

    def __init__(self, api_version: str) -> None:
        super().__init__()

        self._api_version = api_version

        self._client = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = self._construct_client()

        return self._client

    def _construct_client(self) -> httpx.Client:
        raise NotImplementedError()

    def _on_destroy(self) -> None:
        if self.client and not self.client.is_closed:
            self.client.close()

    def _check_exc(self, r) -> None:
        if r.status_code == 429:
            self._is_active = False

            err_msg = "Превышен лимит на количество запросов"

            self.LOGGER.critical(err_msg)
            self.LOGGER.debug(f"Отключение провайдера: {self.__class__.__name__}")

            raise ModuleExceptions.TooManyRequestError(err_msg)

        if r.status_code != 200:
            err_msg = r.text

            # Все эти коды означают,
            # что дальнейшая работа на этом провайдере невозможна
            if r.status_code in {401, 403, 503}:
                self._is_active = False

                self.LOGGER.critical(err_msg)
                self.LOGGER.debug(f"Отключение провайдера: {self.__class__.__name__}")
            else:
                self.LOGGER.error(err_msg)

            raise httpx.RequestError(err_msg)
