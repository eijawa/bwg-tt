from datetime import timedelta

import pytest

from src.core.exc import CalledMethodIntervalError
from src.core.utils.deco import interval_limited


class ExampleCls:
    @interval_limited(timedelta(seconds=30))
    def long_interval(self) -> None:
        return None

    @interval_limited(timedelta(seconds=0))
    def short_interval(self) -> None:
        return None


def test_long_interval() -> None:
    cls_ = ExampleCls()

    cls_.long_interval()

    with pytest.raises(CalledMethodIntervalError):
        cls_.long_interval()


def test_short_interval() -> None:
    cls_ = ExampleCls()

    cls_.short_interval()
    cls_.short_interval()
