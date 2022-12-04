import datetime


class LoggerInterface:
    def log(self, message: str):
        pass


class ConsoleLogger(LoggerInterface):
    def log(self, message: str):
        print(f"{datetime.datetime.now()}   {message}")


class FileLoggerDecorator(LoggerInterface):
    wrapped_logger: LoggerInterface
    file_path: str

    def __init__(self, logger: LoggerInterface, file_path: str):
        self.wrapped_logger = logger
        self.file_path = file_path

    def log(self, message: str):
        self.wrapped_logger.log(message)
        with open(self.file_path, "a") as file:
            file.write(f"{datetime.datetime.now()}   {message}\n")


