from argparse import ArgumentParser
import random

from . import global_vars

# --------- TESTING SETTINGS ----------------

MOCK_get_console_parameters = True
MOCK_CLI_PASSWORD_START_POSITION = 1
MOCK_CLI_PASSWORD_STOP_POSITION = 3
MOCK_CLI_OUTPUT_FOLDER = ""

MOCK_checkup_last_word = True
INFO_print_main_variables = True
INFO_password_generator = True

# -------------------------------------------

MAIN_VARS = global_vars.MainVariables()
if MOCK_get_console_parameters:
    MAIN_VARS.PASSWORD_START_POSITION = MOCK_CLI_PASSWORD_START_POSITION
    MAIN_VARS.PASSWORD_STOP_POSITION = MOCK_CLI_PASSWORD_STOP_POSITION
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
        print(f"CHARSET = {MAIN_VARS.CHARSET}\n"
              f"PASSWORD_START_POSITION = {MAIN_VARS.PASSWORD_START_POSITION}\n"
              f"PASSWORD_STOP_POSITION = {MAIN_VARS.PASSWORD_STOP_POSITION}\n"
              f"OUTPUT_FOLDER = {MAIN_VARS.OUTPUT_FOLDER if MAIN_VARS.OUTPUT_FOLDER else 'current'}")


def checkup_last_word(func):
    if MOCK_checkup_last_word:
        return "".join(random.choices(MAIN_VARS.CHARSET, k=MAIN_VARS.PASSWORD_STOP_POSITION))
    return func


def password_generator(func):
    # if INFO_password_generator:
    # print(passgen.word)
    # print(passgen.embedded_loops)
    return func


# -------------------------------------

print("--- Test Mode is Enable. ---\n")
print_main_variables()
