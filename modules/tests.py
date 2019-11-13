from argparse import ArgumentParser
import random
import functools

from . import global_vars

# --------- TESTING SETTINGS ----------------

MOCK_get_console_parameters = True
MOCK_CLI_PASSWORD_START_POSITION = 1
MOCK_CLI_PASSWORD_STOP_POSITION = 3
MOCK_CLI_OUTPUT_FOLDER = ""

MOCK_checkup_last_word = True

INFO_print_value = True
INFO_print_main_variables = True
INFO_password_generator = True

# -------------------------------------------

MAIN_VARS = global_vars.MainVariables()
if MOCK_get_console_parameters:
    MAIN_VARS.PASSWORD_START_POSITION = MOCK_CLI_PASSWORD_START_POSITION
    MAIN_VARS.PASSWORD_STOP_POSITION = MOCK_CLI_PASSWORD_STOP_POSITION
    if MOCK_CLI_OUTPUT_FOLDER:
        MAIN_VARS.OUTPUT_FOLDER = MOCK_CLI_OUTPUT_FOLDER


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
        print(f"--- Test Mode is Enable. ---\n\n"
              f"CHARSET = {MAIN_VARS.CHARSET}\n"
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


def password_generator(func):
    return func


def print_value(value):
    if INFO_print_value:
        print(value)


def create_embedded_loops(func):
    if INFO_password_generator:
        result = func()
        print_value(f"empty_embedded_loops = {result}")
    return lambda: result


def encode_word_to_char_positions_in_charset(func):
    if INFO_password_generator:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print_value(f"filled_embedded_loops = {result}")
        return wrapper
    return func

# -------------------------------------


print_main_variables()
