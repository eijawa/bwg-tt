from decimal import Decimal

from pydantic import BaseModel, Field, computed_field


class CoinCourseSchema(BaseModel):
    """
    Схема курса токена к другому активу в отношении 1:1
    """

    asset: str = Field(exclude=True)
    quote: str = Field(exclude=True)

    value: Decimal

    @computed_field
    @property
    def direction(self) -> str:
        return self.asset.upper() + "-" + self.quote.upper()


class CoinExchangeSchema(BaseModel):
    """
    Схема последнего снимка рынка токенов конкретной биржи
    """

    exchanger: str
    courses: list[CoinCourseSchema]
