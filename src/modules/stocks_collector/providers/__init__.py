"""
Модуль провайдеров

Провайдеры получают сырые данные и могут осуществлять малейшую их обработку,
но в основном оставляют "как есть", чтобы эти данные преобразовал уже другой механизм
"""

from .binance_p import BinanceRESTAPIProvider
from .coingecko_p import CoinGeckoRESTAPIProvider
