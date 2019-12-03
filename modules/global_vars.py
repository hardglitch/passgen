import os.path


class MainVariables:

    def __init__(self,
                 start: int = 0,
                 stop: int = 0,
                 output: str = "",
                 size: int = 10 * 1024 * 1024 * 1024,  # 10 Gb
                 resume: bool = False,
                 ):

        self.CHARSET = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                       r"0123456789!@#$%^&*()-_+=~`[]{}|\:;""'<>,.?/ "
        self.FORBIDDEN_CHARS = r"!%^&*-_+=~`{}|\:""'<>?/ "
        self.CHARSET_SIZE = len(self.CHARSET)
        self.PASSWORD_START_POSITION: int = abs(start)
        self.PASSWORD_STOP_POSITION: int = abs(stop)
        if self.PASSWORD_STOP_POSITION < self.PASSWORD_START_POSITION >= 1:
            self.PASSWORD_START_POSITION, self.PASSWORD_STOP_POSITION = \
                self.PASSWORD_STOP_POSITION, self.PASSWORD_START_POSITION

        self.OUTPUT_FOLDER: str = os.getcwd() if not output or output == "" else os.path.abspath(fr"{output}")
        self.OUTPUT_FILE_SIZE: int = size
        self.RESUME: bool = resume
        self.LATEST_WORD = self.CHARSET[-1] * self.PASSWORD_STOP_POSITION
