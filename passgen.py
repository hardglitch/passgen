import argparse
import os.path
import sys
from modules import tests, globals


@tests.get_console_parameters
def get_console_parameters() -> argparse:
    # Get external console parameters
    # > python passgen.py 1 5 -o "c:/output/"

    parser = argparse.ArgumentParser()
    parser.add_argument("start", type=int, help="Start Position (>=1)")
    parser.add_argument("stop", type=int, help="Stop Position")
    parser.add_argument("-o", "--output", nargs="?", help="Output Directory")
    return parser.parse_args(sys.argv[1:])


@tests.checkup_last_word
def checkup_last_word() -> str:
    # checkup 'last_word' file and return last_word value
    try:
        # 'last_word' file exist
        with open(main_variables.OUTPUT_FOLDER + r"\last_word", "r") as file:
            for line in file:
                if line != "":
                    last_word = re.sub(r"^\s+|\n|\r|\s+$", '', line)
                    return last_word

    except FileNotFoundError:
        # 'last_word' file not exist
        pass


def password_generator():
    # generate strings
    # write every string into 'tmp_dict' file
    # return last generated string on error

    with open(main_variables.OUTPUT_FOLDER + r"\tmp_dict", "a") as file:

        # start word = last word from 'last_word' file
        # or 'a'*3 -> 'aaa' (for example)
        last_word = checkup_last_word()
        word: str = last_word if last_word else main_variables.CHARSET[0] * main_variables.PASSWORD_START_POSITION

        # forming embedded loops: word length = 7 -> 7 loops -> char1, char2 .. char7
        embedded_loops: dict = {f"char{i+1}": 0 for i in range(main_variables.PASSWORD_STOP_POSITION)}

        while True:
            if file.writable():
                file.write(fr"{word}")  # 'aa'  //  'v7-'
                file.write("\r\n")



                # # find position 'a' in CHARSET -> 0
                # # 'a' is last char from 'aa'
                # # run once
                # char_position_in_charset = main_variables.CHARSET.find(word[-1:])  # 0
                #
                # # next char
                # next_char = main_variables.CHARSET[char_position_in_charset + 1]   # 'b' (after 'a')
            else:
                return fr""


# -----------------------------


if __name__ == "__main__":

    cli_args = get_console_parameters()
    main_variables = globals.MainVariables(cli_args.start, cli_args.stop, cli_args.output)

    password_generator()
