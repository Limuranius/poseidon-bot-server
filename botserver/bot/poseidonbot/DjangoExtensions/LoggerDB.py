from ..Logger import LoggerInterface
from django.db.models import Model
import datetime


class DatabaseLogger(LoggerInterface):
    __model_obj: Model

    def __init__(self, obj: Model):
        self.__model_obj = obj

    def log(self, message: str):
        self.__model_obj.refresh_from_db()  # Синхронизировать объект с БД
        self.__model_obj.log += f"{datetime.datetime.now()}   {message}\n"
        self.__model_obj.save()
