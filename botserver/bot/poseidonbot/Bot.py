import time
import datetime
from .ScheduleSolver import ScheduleSolver
import requests
import bs4
import json
from .ConfigManager import ConfigManagerInterface
from .Logger import LoggerInterface
from typing import Dict
from threading import Thread
from enum import Enum
import traceback

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"

FEFU_URL = "https://esa.dvfu.ru/"
POSEIDON_INDEX_URL = "https://poseidon.dvfu.ru/index.php"
POSEIDON_AUTH_URL = "https://poseidon.dvfu.ru/includes/auth.php"
POSEIDON_GET_EVENTS_URL = "https://poseidon.dvfu.ru/includes/get-events.php"
POSEIDON_POST_EVENTS_URL = "https://poseidon.dvfu.ru/includes/check-events.php"


class BotStatus(Enum):
    NOT_STARTED = 1  # Метод run() ещё не был запущен
    RUNNING = 2  # Метод run() был запущен и бот работает
    FINISHED = 3  # Бот закончил выполнение метода run()
    ERRORS_OCCURRED = 4  # При выполнении работы произошли ошибки


class Bot:
    _session: requests.Session
    _poseidon_headers: dict
    _config_manager: ConfigManagerInterface
    _solver: ScheduleSolver
    _logger: LoggerInterface
    status: BotStatus = BotStatus.NOT_STARTED  # Статус бота

    def __init__(self, config_manager: ConfigManagerInterface, logger: LoggerInterface):
        self._session = requests.Session()
        self._poseidon_headers = {}
        self._config_manager = config_manager
        self._solver = ScheduleSolver(self._config_manager)
        self._logger = logger

    def __check_authed_at_FEFU(self) -> bool:
        """Возвращает True, если бот залогинен на сайте ДВФУ"""
        return self._session.cookies.get("_univer_identity") is not None

    def __auth_at_FEFU(self) -> None:
        """Авторизуется на сайте ДВФУ под учёткой пользователя и собирает все необходимые куки"""

        self._logger.log("Signing in to esa.dvfu.ru...")

        # Заходим на страницу ДВФУ
        response = self._session.get(FEFU_URL, headers={
            "User-Agent": USER_AGENT
        })
        # Получаем метатеги страницы
        page_metas = _get_metas(response.text)

        # Логинимся в учётную запись ДВФУ
        data = {
            "_csrf_univer": page_metas["csrf-token"],
            "csrftoken": page_metas["csrf-token-value"],
            "username": self._config_manager.username,
            "password": self._config_manager.password,
            "bu": POSEIDON_INDEX_URL,
        }
        self._session.post(FEFU_URL, data=data, headers={
            "User-Agent": USER_AGENT
        })
        if self.__check_authed_at_FEFU():
            self._logger.log("Login successful!")
        else:
            raise Exception("Incorrect FEFU credentials")

    def __auth_at_Poseidon(self) -> None:
        """Логинится на сайте Посейдона, используя куки, полученные при авторизации на сайте ДВФУ"""

        self._logger.log("Signing in to poseidon.dvfu.ru...")

        # Заходим на страницу посейдона
        response = self._session.get(POSEIDON_INDEX_URL, headers={
            "User-Agent": USER_AGENT
        })
        # Получаем CSRF токен страницы
        page_metas = _get_metas(response.text)
        self._poseidon_headers = {
            "User-Agent": USER_AGENT,
            "X-CSRF-TOKEN": page_metas["csrf_token"],
            "X-csrftoken": page_metas["csrf-token-value"]
        }
        # Отправляем запрос на авторизацию, иначе ничего не заработает
        auth_response = self._session.get(POSEIDON_AUTH_URL, headers=self._poseidon_headers)
        auth_json = auth_response.json()
        if auth_json["success"]:  # Удалось залогиниться в Посейдоне
            self._logger.log("Login successful!")
        else:
            raise Exception("Could not log into Poseidon")

    def __getScheduleStr(self) -> str:  # TODO: сделать, чтобы принимал на вход определённую дату
        """
        Запрашивает расписание с сайта.
        Возвращает ответ в виде строки.
        Если расписания на данный день ещё нет, то возвращает пустую строку.
        """
        response = self._session.get(POSEIDON_GET_EVENTS_URL,
                                     headers=self._poseidon_headers,
                                     params={
                                         "date": self._config_manager.Date.strftime("%a %b %d %Y")  # Mon May 02 2022
                                     })
        return response.text

    def __getScheduleJSON(self) -> dict:  # TODO: сделать, чтобы принимал на вход определённую дату
        """Запрашивает расписание с сайта и возвращает ответ в виде объекта JSON"""
        return json.loads(self.__getScheduleStr())

    def __updateSchedule(self, schedule_json: dict) -> None:
        """Обновляет расписание, полученное на определённый день"""
        self._logger.log("Updating schedule")
        self._solver.update_schedule(schedule_json)

    def __tryBookTime(self) -> bool:
        """
        Используя раннее полученное расписание, совершает POST_COUNT_BEFORE_UPDATE попыток записаться.
        Если записаться получилось, возвращает True. Иначе False.
        """
        fmt = "%d-%m-%Y %H:%M:%S"  # Формат даты, отправляемой на сервер. Например, 05-03-2022 07:00:00
        intervals = self._solver.getPerfectMatches()  # Интервалы, подходящие под параметры конфига
        for i in range(min(self._config_manager.POST_COUNT_BEFORE_UPDATE, len(intervals))):
            interval = intervals[i]
            data = {
                "start": interval[0].strftime(fmt),
                "end": interval[1].strftime(fmt),
                "number": str(self._config_manager.MachineNumber),  # Номер машинки
            }
            self._logger.log(f"Booking time from {data['start']} to {data['end']} on machine #{data['number']}...")
            book_response = self._session.post(POSEIDON_POST_EVENTS_URL,
                                               headers=self._poseidon_headers,
                                               data=data)  # Отправляем запрос на запись на определённое время
            book_response = json.loads(book_response.text)
            if book_response["success"]:  # Записаться получилось
                self._logger.log("Successful!")
                return True
            else:  # Время занято
                self._logger.log("Failed")
        return False

    def __waitTillDayOpen(self) -> dict:
        """
        В цикле проверяет, не появилось ли расписание на день записи.
        Когда оно появится, возвращает расписание в виде JSON-объекта.
        """
        self._logger.log(f"Getting schedule on {self._config_manager.Date}...")
        while True:
            schedule = self.__getScheduleStr()
            if schedule == "":  # День ещё не открылся
                self._logger.log("Day is not available yet")
                time.sleep(1)
            else:
                self._logger.log("Day opened!")
                return json.loads(schedule)

    def __waitUntil(self, exec_time: datetime.datetime) -> None:
        """Останавливает работу программы, пока часы не стукнут exec_time"""
        self._logger.log(f"Waiting until: {exec_time}")
        while datetime.datetime.now(exec_time.tzinfo) < exec_time:
            time.sleep(1)
        self._logger.log(f"Pizza time!")

    def run(self) -> None:
        self._logger.log("Bot started running.")
        if not self.can_auth():
            raise Exception("Incorrect FEFU credentials")
        else:
            self._logger.log("Correct FEFU credentials")
        self.status = BotStatus.RUNNING

        # Останавливаем программу, пока не наступит дата и время открытия записи
        t = self._config_manager.ExecuteAt - datetime.timedelta(
            seconds=20)  # Вычитаем 20 секунд, чтобы бот ещё успел залогиниться
        self.__waitUntil(t)

        # Логинимся на сайтах
        self.__auth_at_FEFU()
        self.__auth_at_Poseidon()

        # Ждём, когда на сайте появится расписание и записываем его в файл
        curr_schedule = self.__waitTillDayOpen()
        self.__updateSchedule(curr_schedule)

        while True:
            success = self.__tryBookTime()  # Пробуем записаться
            if success:  # Если записаться удалось, прекращаем попытки записаться
                break

            # Если записаться не удалось, заново обращаемся на сервер, смотрим, какие интервалы ещё не заняли
            self.__updateSchedule(self.__getScheduleJSON())
            if len(self._solver.getPerfectMatches()) == 0:  # Если не осталось ни одного свободного интервала
                self._logger.log("No matching intervals left. Task failed! Good luck next week!")
                break
        self._logger.log("Process finished.")
        self.status = BotStatus.FINISHED

    def run_log_exceptions(self) -> None:
        """Запускает бота и все возникающие исключения заносит в лог"""
        try:
            self.run()
        except Exception as e:
            self.status = BotStatus.ERRORS_OCCURRED
            self._logger.log(traceback.format_exc())
            self._logger.log("Bot finished with exceptions.")

    def run_in_background(self):
        t = Thread(target=self.run_log_exceptions, daemon=True)
        t.start()

    def update_config(self):
        """Обновляет данные конфига"""
        self._config_manager.load()

    def get_user_info(self) -> dict:
        """Получает различную информацию о пользователе, используя парсинг страниц ДВФУ"""
        pass  # TODO

    def can_auth(self) -> bool:
        """Проверяет правильность логина и пароля.
        Пытается авторизоваться и возвращает True, если авторизоваться удалось"""
        pass  # TODO

    def __get_dormitory_machines(self) -> list[int]:
        """Получает номера машинок в корпусе"""
        pass  # TODO

    def __get_day_open_time(self) -> list[datetime.time]:
        """Возвращает дни и время, когда открываются записи"""
        pass  # TODO


def _get_metas(response_text: str) -> Dict[str, str]:
    """Получает все meta-теги страницы"""
    soup = bs4.BeautifulSoup(response_text, features="html.parser")
    metas = soup.find_all("meta")
    return {meta.get("name"): meta.get("content") for meta in metas}
