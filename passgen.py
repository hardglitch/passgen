from argparse import ArgumentParser
import sys
import re
import os.path

from modules import global_vars, tests


@tests.get_console_parameters
def get_console_parameters() -> []:  # list
    # Get external console parameters
    # > python passgen.py 1 5 -o "c:/output/"
    parser = ArgumentParser()
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


@tests.password_generator
def password_generator():
    # generate strings
    # write every string into 'tmp_dict' file
    # return last generated string on error

    with open(main_variables.OUTPUT_FOLDER + r"\tmp_dict", "a") as file:

        # last_word - is first unwritten word in 'last_dict' file, but it's last in generating chain
        # start word = word from 'last_word' file
        # or 'a'*3 -> 'aaa' (for example)
        word: str = last_word if last_word else main_variables.CHARSET[0] * main_variables.PASSWORD_START_POSITION

        # forming embedded loops: word length = 7 -> 7 loops -> dict['char1':0, 'char2':0 .. 'char7':0]
        # where 0 - char position in CHARSET
        embedded_loops: dict = {f"char{i+1}": 0 for i in range(main_variables.PASSWORD_STOP_POSITION)}

        # encode 'word' to char positions in CHARSET
        # 'aah8' -> dict['char1':0, 'char2':0, 'char3':8, 'char4':61]
        for i, char in enumerate(embedded_loops):
            embedded_loops[char] = main_variables.CHARSET.find(word[i])

        # while True:
        #     if file.writable():
        #         file.write(fr"{word}")  # for example 'aa' or 'v7-'
        #         file.write("\r\n")
        #     else:
        #         return fr""


# -----------------------------


if __name__ == "__main__":

    cli_args = get_console_parameters()
    main_variables = global_vars.MainVariables(cli_args.start, cli_args.stop, cli_args.output)

    # password_generator()
