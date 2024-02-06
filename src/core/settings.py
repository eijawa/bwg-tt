from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_APP_ROOT = Path(__file__).parent.parent


class CoinGecko(BaseModel):
    """
    Настройки для работы с CoinGecko
    """

    # API ключ для взаимодействия с биржей CoinGecko
    API_KEY: str


class FreeCurrency(BaseModel):
    """
    Настройки для работы с FreeCurrency
    """

    # API ключ для взаимодействия с обменником FreeCurrency
    API_KEY: str


class Postgres(BaseModel):
    """
    Настройки для работы с Postgres
    """

    DBUSER: str
    DBPASS: str
    DBHOST: str
    DBPORT: str
    DBNAME: str


# FIXME: build
# Такой формат не работает, если использовать билдеры (nuitka)
class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            _APP_ROOT.parent / "environments" / ".env",
            _APP_ROOT.parent / "environments" / ".db.env",
        ),
        env_file_encoding="UTF-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    APP_ROOT: Path = Field(default=_APP_ROOT, frozen=True)
    DEBUG: bool = False

    # Время активации (в секундах) фоновых процессов
    UPDATE_INTERVAL_SECONDS: int

    # Коды токенов, за которыми ведётся наблюдение
    COLLECTIBLE_COINS_SYMBOLS: list[str] = ["BTC", "ETH"]

    # Валюта, используемая по-умолчанию
    DEFAULT_CURRENCY: str = "usd"

    # Секция с настройками для CoinGecko
    COINGECKO: CoinGecko

    # Секция с настройками для FreeCurrency
    FREECURRENCY: FreeCurrency

    # Секция с настройками для Postgres
    POSTGRES: Postgres

    @property
    def db_connection_string(self) -> str:
        """
        Строка подключения к БД без указания протокола

        ...

        Returns
        -------
        str
            Строка подключения к БД без протокола
            Example: ://user:password@host:port/name
        """

        return "://{user}:{password}@{host}:{port}/{name}".format(
            user=self.POSTGRES.DBUSER,
            password=self.POSTGRES.DBPASS,
            host=self.POSTGRES.DBHOST,
            port=self.POSTGRES.DBPORT,
            name=self.POSTGRES.DBNAME,
        )


settings = _Settings()
