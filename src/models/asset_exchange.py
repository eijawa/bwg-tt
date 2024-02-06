from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class AssetExchangeModel(Base):
    __tablename__ = "assets_exchanges"
    __table_args__ = (Index("rt_idx", "rt"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    value: Mapped[Decimal] = mapped_column(DECIMAL())

    rt: Mapped[datetime] = mapped_column(DateTime())
    lut: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)

    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    source: Mapped["SourceModel"] = relationship(
        back_populates="assets_exchanges", lazy="joined"
    )

    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
    coin: Mapped["CoinModel"] = relationship(
        back_populates="assets_exchanges", lazy="joined"
    )
