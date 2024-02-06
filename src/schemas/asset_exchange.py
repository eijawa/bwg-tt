from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class AssetInfoSchema(BaseModel):
    name: str = ""
    symbol: str
    value: Decimal


class AssetExchangeMetaSchema(BaseModel):
    # Источник информации
    source: str

    # Время запроса сервером
    rt: datetime = Field(default_factory=datetime.now)

    # Последнее время обновления значения источника
    lut: Optional[datetime] = None


class AssetExchangeSchema(BaseModel):
    # Целевой объект
    asset: AssetInfoSchema

    # Цена за целевой объект относительно другого объекта
    quote: AssetInfoSchema

    meta: AssetExchangeMetaSchema
