from threading import Thread
from .models import RecordModel
from .poseidonbot import Bot, BotStatus, DatabaseLogger, ConfigManagerDB, ConsoleLogger
import time


class BotMonitor:
    """
    Класс для мониторинга ботов.
    Каждый бот привязан к своей записи в модели RecordModel.
    Проверяет статусы ботов и делает соответствующие действия.
    """
    count = 0
    bots: dict[int, Bot] = dict()  # id записи бота: бот
    monitoring_interval = 5  # Сколько секунд между проверками

    @classmethod
    def create_startup_bots(cls):
        """Создаёт ботов для каждого запроса в базе данных"""
        objects = RecordModel.objects.all()
        for obj in objects:
            bot_id = obj.id
            bot = Bot(
                ConfigManagerDB(RecordModel, bot_id),
                # DatabaseLogger(RecordModel, bot_id)
                ConsoleLogger()
            )
            cls.bots[bot_id] = bot
            bot.run_in_background()

    @classmethod
    def update_bot_for_obj(cls, obj: RecordModel):
        """Обновляет конфигурацию у бота, связанного с obj.
        Либо создаёт нового бота, если у obj ещё нет привязанного бота"""
        if cls.bots.get(obj.id) is not None:  # Если уже есть привязанный бот
            cls.bots[obj.id].update_config()
        else:  # Если привязанного бота нет
            bot = Bot(
                ConfigManagerDB(RecordModel, obj.id),
                # DatabaseLogger(RecordModel, bot_id)
                ConsoleLogger()
            )
            cls.bots[obj.id] = bot
            bot.run_in_background()

    @classmethod
    def monitor_bots(cls):
        for bot_id, bot in cls.bots.items():
            # Добавить обработчики для разных статусов
            if bot.status == BotStatus.FINISHED:
                pass
            elif bot.status == BotStatus.ERRORS_OCCURRED:
                pass

    @classmethod
    def monitor_continuously(cls):
        while True:
            cls.monitor_bots()
            time.sleep(cls.monitoring_interval)

    @classmethod
    def run_in_background(cls):
        """Запускает мониторинг ботов на фоне"""
        t = Thread(target=cls.monitor_continuously, daemon=True)
        t.start()

