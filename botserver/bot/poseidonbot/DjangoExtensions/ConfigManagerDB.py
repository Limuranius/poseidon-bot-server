from ..ConfigManager import ConfigManagerInterface
from django.db.models import Model


class ConfigManagerDB(ConfigManagerInterface):
    __model_obj: Model

    def __init__(self, obj: Model):
        super().__init__()
        self.__model_obj = obj
        self.load()

    def load(self) -> None:
        self.__model_obj.refresh_from_db()  # Синхронизировать объект с БД
        self._config.ExecuteAt = self.__model_obj.open_datetime
        self._config.Date = self.__model_obj.date
        self._config.MinTimeLength = self.__model_obj.min_duration
        self._config.MaxTimeLength = self.__model_obj.max_duration
        self._config.MachineNumber = self.__model_obj.machine_number
        self._config.TimeIntervals = [(self.__model_obj.time_from, self.__model_obj.time_before)]
        self._user_data.username = self.__model_obj.owner.FEFU_username
        self._user_data.password = self.__model_obj.owner.FEFU_password
        self._config.POST_COUNT_BEFORE_UPDATE = 3
        self._config.LOG_SCHEDULES = False
