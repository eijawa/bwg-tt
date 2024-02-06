from abc import abstractmethod

from src.schemas import AssetExchangeSchema


class Adapter:
    @abstractmethod
    def convert_to_asset_exchange(self, data: dict) -> list[AssetExchangeSchema]:
        """
        Преобразование полученных данных в схему актива,
        используемую дальше в приложении

        ...

        Params
        ------
        `data` : dict
            Полученные данные

        Returns
        -------
        list[AssetExchangeSchema]
            Схема актива

        Notes
        -----
        Этот метод будет перегружаться в наследниках,
        поэтому стоит всегда проверять его параметры
        """

        ...


class BaseAdapter(Adapter):
    """
    Базовый класс для адаптеров
    """

    ...
