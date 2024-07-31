import threading
from abc import ABCMeta, abstractmethod


class ILogger(metaclass=ABCMeta):
    @abstractmethod
    def get_instance(self):
        pass

    @abstractmethod
    def reset_instance(self):
        pass

    @abstractmethod
    def set_log_filepath(self, filepath):
        pass

    @abstractmethod
    def log(self, level, message):
        pass

    @abstractmethod
    def get_log_file(self):
        pass

    @abstractmethod
    def flush(self):
        pass


class LoggerImpl(ILogger):
    __instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            with cls._lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance

    # def __init__(self):
    #     if not hasattr(self, 'initialized'):
    #         self.initialized = True
    #         self._log_lock = threading.Lock()
    #         self.filepath = ''
    #         self.level = ""
    #         self.message = 'default init message'

    def get_instance(self):
        return self.__instance

    #
    def reset_instance(self):
        self.__instance = None

    def set_log_filepath(self, filepath):
        self.filepath = filepath

    def log(self, level, message):
        self.level = level
        self.message = message
        with self._lock:
            with open(self.filepath, 'a') as f:
                f.write(f"[{self.level}] - " + self.message + '\n')

    def get_log_file(self):
        return self.filepath

    def flush(self):
        print("flush the message")


if __name__ == '__main__':
    logger = LoggerImpl()
    logger2 = LoggerImpl()

    print(logger.get_instance())
    logger.set_log_filepath("test.log")
    logger.log("INFO", "This message is from logger1!")

    print(logger2.get_instance())
    # able to log messages without mentioning filepath for logger2 as it was already init in logger1
    logger2.log("DEBUG", "This message is from logger2!")

    print(logger is logger2)
    print(logger.get_log_file())

    logger3 = LoggerImpl()
    print("hey:", logger3.get_instance())
    logger3.log("ERROR", "This message is from logger3!")

    # print(hasattr(logger, 'get_instance'))
    # print(hasattr(logger, 'initialized'))
    # print(hasattr(logger, 'reset_instance'))
    # print(hasattr.__doc__)
