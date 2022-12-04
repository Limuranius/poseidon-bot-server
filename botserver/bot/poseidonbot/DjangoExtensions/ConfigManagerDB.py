from ..ConfigManager import ConfigManagerInterface
from django.db.models import Model
from typing import Type


class ConfigManagerDB(ConfigManagerInterface):
    _model: Type[Model]
    _related_config_id: int

    def __init__(self, model: Type[Model], related_config_id: int):
        super().__init__()
        self._model = model
        self._related_config_id = related_config_id
        self.load()

    def load(self) -> None:
        obj = self._model.objects.get(pk=self._related_config_id)
        self._config.ExecuteAt = obj.open_time
        self._config.Date = obj.date
        self._config.MinTimeLength = obj.min_duration
        self._config.MaxTimeLength = obj.max_duration
        self._config.MachineNumber = obj.machine_number
        self._config.TimeIntervals = [(obj.time_from, obj.time_before)]
        self._user_data.username = obj.login
        self._user_data.password = obj.password
        self._config.POST_COUNT_BEFORE_UPDATE = 3
        self._config.LOG_SCHEDULES = False
