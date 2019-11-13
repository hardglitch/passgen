from argparse import ArgumentParser
import sys
import re

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
    # checkup 'last_word' file and return 'last_word' value
    try:
        # 'last_word' file exist
        with open(main_variables.OUTPUT_FOLDER + r"\last_word", "r") as last_word_file:
            # last_word - is a single word in 'last_word' file, but it's last in generating chain
            # last_word = word from 'last_word' file    or   'a'*3 -> 'aaa' (for example)
            word_from_last_word_file = last_word_file.readline()
            word_from_last_word_file = re.sub(r"^\s+|\n|\r|\s+$", '', word_from_last_word_file)
            last_word: str = word_from_last_word_file if word_from_last_word_file \
                else main_variables.CHARSET[0] * main_variables.PASSWORD_START_POSITION
            return last_word

    except FileNotFoundError:
        # 'last_word' file not exist
        pass


@tests.password_generator
def password_generator():
    # generate strings
    # write every string into 'tmp_dict' file
    # return last generated string on error

    @tests.create_embedded_loops
    def create_embedded_loops() -> dict:
        # forming embedded loops: word length = 7 -> 7 loops -> dict['char1':0, 'char2':0 .. 'char7':0]
        # where 0 - char position in CHARSET
        return {f"char{i+1}": 0 for i in range(main_variables.PASSWORD_STOP_POSITION)}

    @tests.encode_word_to_char_positions_in_charset
    def encode_word_to_char_positions_in_charset(word, loops) -> dict:
        # encode 'word' to char positions in CHARSET
        # 'aah8' -> dict['char1':0, 'char2':0, 'char3':8, 'char4':61]
        for i, char in enumerate(loops):
            loops[char] = main_variables.CHARSET.find(word[i])
        return loops

    with open(main_variables.OUTPUT_FOLDER + r"\tmp_dict", "a") as tmp_dict_file:

        embedded_loops = create_embedded_loops()
        last_word = checkup_last_word()
        encode_word_to_char_positions_in_charset(last_word, embedded_loops)

        # while True:
        #     if tmp_dict_file.writable():
        #         tmp_dict_file.write(fr"{word}")  # for example 'aa' or 'v7-'
        #         tmp_dict_file.write("\r\n")
        #     else:
        #         return fr""


# -----------------------------


if __name__ == "__main__":

    cli_args = get_console_parameters()
    main_variables = global_vars.MainVariables(cli_args.start, cli_args.stop, cli_args.output)

    password_generator()
