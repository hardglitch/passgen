import argparse
import os.path
import sys
import random
from modules import globals


MOCK_get_console_parameters = True
MOCK_checkup_last_word = True
TEST_print_main_variables = True

if MOCK_get_console_parameters:
    print("--- Test Mode is Enable. ---\n")
    PARSER_START = 1
    PARSER_STOP = 2


def get_console_parameters(func):
    if MOCK_get_console_parameters:
        parser = argparse.ArgumentParser()
        parser.start = PARSER_START
        parser.stop = PARSER_STOP
        parser.output = ""
        return parser
    return func


def print_main_variables(main_vars):
    if TEST_print_main_variables:
        print(f"CHARSET = {main_vars.CHARSET}\n"
              f"PASSWORD_START_POSITION = {main_vars.PASSWORD_START_POSITION}\n"
              f"PASSWORD_STOP_POSITION = {main_vars.PASSWORD_STOP_POSITION}\n"
              f"OUTPUT_FOLDER = {main_vars.OUTPUT_FOLDER}")


def checkup_last_word(func):
    if MOCK_checkup_last_word:
        return "".join(random.choices(main_vars.CHARSET, k=main_vars.PASSWORD_STOP_POSITION))
    return func
