from argparse import ArgumentParser
import random
import functools

from . import global_vars

# --------- TESTING SETTINGS ----------------

MOCK_get_console_parameters = True
MOCK_CLI_PASSWORD_START_POSITION = 1
MOCK_CLI_PASSWORD_STOP_POSITION = 2
MOCK_CLI_OUTPUT_FOLDER = ""

MOCK_checkup_last_word = True

INFO_print_value = True             # enable all INFO_...
INFO_print_main_variables = True
INFO_password_generator = True

# -------------------------------------------

MAIN_VARS = global_vars.MainVariables()
if MOCK_get_console_parameters:
    MAIN_VARS.PASSWORD_START_POSITION = MOCK_CLI_PASSWORD_START_POSITION
    MAIN_VARS.PASSWORD_STOP_POSITION = MOCK_CLI_PASSWORD_STOP_POSITION
    if MOCK_CLI_OUTPUT_FOLDER:
        MAIN_VARS.OUTPUT_FOLDER = MOCK_CLI_OUTPUT_FOLDER


def print_value(value):
    if INFO_print_value:
        print(value)


def get_console_parameters(func):
    if MOCK_get_console_parameters:
        parser = ArgumentParser()
        parser.start = MOCK_CLI_PASSWORD_START_POSITION
        parser.stop = MOCK_CLI_PASSWORD_STOP_POSITION
        parser.output = MOCK_CLI_OUTPUT_FOLDER
        return lambda: parser
    return func


def print_main_variables():
    if INFO_print_main_variables:
        print_value(f"--- Test Mode is Enable. ---\n\n"
                    f"CHARSET = {MAIN_VARS.CHARSET}\n"
                    f"CHARSET_SIZE = {MAIN_VARS.CHARSET_SIZE}\n"
                    f"PASSWORD_START_POSITION = {MAIN_VARS.PASSWORD_START_POSITION}\n"
                    f"PASSWORD_STOP_POSITION = {MAIN_VARS.PASSWORD_STOP_POSITION}\n"
                    f"OUTPUT_FOLDER = {MAIN_VARS.OUTPUT_FOLDER if MAIN_VARS.OUTPUT_FOLDER else 'current'}\n")


def checkup_last_word(func):

    def tmp_result():
        return lambda: "".join(random.choices(MAIN_VARS.CHARSET, k=MAIN_VARS.PASSWORD_STOP_POSITION))

    # 'result_as_function' is a function
    result_as_function = tmp_result() if MOCK_checkup_last_word else func()

    if INFO_password_generator:
        # print 'result_as_string' as a result of function 'result_as_function()'
        result_as_string = result_as_function()
        print_value(f"last_word = {result_as_string}")
        return lambda: result_as_string  # string

    return result_as_function  # function


def print_password_generator_info(func, value):
    if INFO_password_generator:
        @functools.wraps(func)
        def wrapper(*args):
            result = func(*args)
            print_value(f"{value} = {result}")
            return result
        return wrapper
    return func


def create_embedded_loops(func):
    if INFO_password_generator:
        @functools.wraps(func)
        def wrapper(*args):
            result = func(*args)
            print_value(f"empty_char_positions = {result}")
            return result
        return wrapper
    return func


def decode_word_to_char_positions_in_charset(func):
    if INFO_password_generator:
        @functools.wraps(func)
        def wrapper(*args):
            result = func(*args)
            print_value(f"filled_char_positions = {result}")
            return result
        return wrapper
    return func


def get_next_char_position(func):
    if INFO_password_generator:
        @functools.wraps(func)
        def wrapper(*args):
            result = func(*args)
            print_value(f"get_next_char_position = {result}")
            return result
        return wrapper
    return func


def get_next_char_positions(func):
    if INFO_password_generator:
        @functools.wraps(func)
        def wrapper(*args):
            result = func(*args)
            print_value(f"get_next_char_positions = {result}")
            return result
        return wrapper
    return func


def encode_char_positions_to_word(func):
    if INFO_password_generator:
        @functools.wraps(func)
        def wrapper(*args):
            result = func(*args)
            print_value(f"encode_char_positions_to_word = {result}")
            return result
        return wrapper
    return func

# -------------------------------------


print_main_variables()
