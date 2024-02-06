from typing import List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class CoinModel(Base):
    __tablename__ = "coins"
    __table_args__ = (
        UniqueConstraint("name", "symbol", name="uix_coins_name_symbol"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(64))

    # Для простоты выставлю unique,
    # хотя CoinGecko доказал, что это не так
    symbol: Mapped[str] = mapped_column(String(12), unique=True)

    assets_exchanges: Mapped[List["AssetExchangeModel"]] = relationship(
        back_populates="coin"
    )
