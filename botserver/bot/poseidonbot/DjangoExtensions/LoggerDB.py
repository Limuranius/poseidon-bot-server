from ..Logger import LoggerInterface
from django.db.models import Model
from typing import Type
import datetime


class DatabaseLogger(LoggerInterface):
    _model: Type[Model]
    _bot_id: int

    def __init__(self, model: Type[Model], bot_id: int):
        self._model = model
        self._bot_id = bot_id

    def log(self, message: str):
        obj = self._model.objects.get(pk=self._bot_id)
        obj.log += f"{datetime.datetime.now()}   {message}\n"
        obj.save()