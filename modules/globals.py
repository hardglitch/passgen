import os.path
from . import tests


class MainVariables:
    def __init__(self, start, stop, output):
        self.CHARSET = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                       r"0123456789!@#$%^&*()-_+=~`[]{}|\:;""'<>,.?/ "
        self.PASSWORD_START_POSITION: int = abs(start)
        self.PASSWORD_STOP_POSITION: int = abs(stop)
        if self.PASSWORD_STOP_POSITION < self.PASSWORD_START_POSITION >= 1:
            self.PASSWORD_START_POSITION, self.PASSWORD_STOP_POSITION = \
                self.PASSWORD_STOP_POSITION, self.PASSWORD_START_POSITION

        self.OUTPUT_FOLDER: str = os.getcwd() if not output or output == "" else os.path.abspath(fr"{output}")

        tests.print_main_variables(self)
