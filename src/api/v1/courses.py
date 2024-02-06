import logging
from datetime import datetime, timedelta

from fastapi import Depends, Query, Response, status
from sqlalchemy.orm import Session

from src.api.deps import get_session
from src.api.v1 import api_router
from src.core import settings
from src.crud.repositories import AssetsExchangesRepository
from src.modules.currency_exchanger import CurrencyExchanger
from src.schemas.responses import CoinCourseSchema, CoinExchangeSchema

logger = logging.getLogger("APIv1/Courses")

interval = timedelta(seconds=settings.UPDATE_INTERVAL_SECONDS)
lat = datetime.now() - interval

# a.k.a популярный инструмент кеширования
cache = {}

# P.S. Мне требуемый возвращаемый формат вообще не нравится
# По ощущениям, лучше было бы возвращать массив формата:
# [
#     {
#         "source": "binance",
#         "direction": "BTC-USD",
#         "value": 540132.34536
#     },
#     {
#         "source": "coingecko",
#         "direction": "USDTERC-USD",
#         "value": 1.002
#     },
#     ...
# ]
# Поскольку данный формат позволяет получать информацию даже о тех коинах,
# которых не нашлось на одной из бирж.
# Дополнительно он более качественно раскрывается,
# когда ведётся постоянный мониторинг разных бирж

DEFAULT_CURRENCY = settings.DEFAULT_CURRENCY


@api_router.get(
    "/courses",
    summary="Информация по токенам",
    description="Получение последней информации по полученным токенам",
    status_code=status.HTTP_200_OK,
    response_model=CoinExchangeSchema,
    responses={
        status.HTTP_200_OK: {"model": CoinExchangeSchema},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Перевод в конечную валюту не поддерживается сервисом"
        },
    },
)
async def get_courses(
    symbols: set[str] = Query(
        description="Уникальный список символьных кодов токенов", example="BTC, ETH"
    ),
    currency: str = Query(
        default=DEFAULT_CURRENCY,
        description="Конечная валюта, в которую будет произведён перевод",
    ),
    session: Session = Depends(get_session),
) -> CoinExchangeSchema:
    currency = currency.lower()

    if currency not in CurrencyExchanger.currencies:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Перевод в конечную валюту невозможен",
        )

    symbols = [s.lower() for s in symbols]

    # ==============================

    global cache, lat, interval

    cache_key = (frozenset(symbols), currency)

    last_request = cache.get(cache_key, {})

    if not last_request or datetime.now() - last_request["lat"] >= interval:
        logger.debug(f"Обновление значения в кэше запросов по ключу: {cache_key!r}")

        latest_ = AssetsExchangesRepository.latest(session=session)

        if not latest_:
            raise Exception()

        exchanger = latest_.source.name

        assets = AssetsExchangesRepository.latest_assets_by_source(
            session=session, source_name=exchanger, symbols=symbols
        )

        data = _convert_to_schema(exchanger, assets)

        if currency != DEFAULT_CURRENCY:
            data = _exchange_currency(data, DEFAULT_CURRENCY, currency)

        last_request = {"data": data, "lat": datetime.now()}

        cache[cache_key] = last_request
    else:
        logger.debug(f"Используется кэшированный результат по ключу: {cache_key!r}")

    return last_request["data"]


def _convert_to_schema(exchanger, assets) -> CoinExchangeSchema:
    schema = CoinExchangeSchema(exchanger=exchanger, courses=[])
    for asset in assets:
        schema.courses.append(
            CoinCourseSchema(
                asset=asset.coin.symbol, quote=DEFAULT_CURRENCY, value=asset.value
            )
        )
    return schema


def _exchange_currency(
    coin_exchange_schema, base_currency, currency
) -> CoinExchangeSchema:
    for course in coin_exchange_schema.courses:
        course.quote = currency
        course.value = CurrencyExchanger.exchange(
            base_currency=base_currency, value=course.value, currency=currency
        )

    return coin_exchange_schema
