from datetime import datetime
from decimal import Decimal

from src.core.db import SessionLocal
from src.crud.services import AssetsExchangesService
from src.schemas import AssetExchangeMetaSchema, AssetExchangeSchema, AssetInfoSchema


def test_create() -> None:
    with SessionLocal() as session:
        obj = AssetExchangeSchema(
            asset=AssetInfoSchema(symbol="btc", value=Decimal("1.0")),
            quote=AssetInfoSchema(symbol="usdt", value=Decimal("40012.543456")),
            meta=AssetExchangeMetaSchema(
                source="coingecko", rt=datetime.now(), lut=datetime.now()
            ),
        )

        model = AssetsExchangesService.create(session=session, obj=obj, sync=True)

        assert model

        session.delete(model)
