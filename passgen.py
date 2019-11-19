from argparse import ArgumentParser
import os.path
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
    parser.add_argument("-r", "--resume", nargs="?", help="To resume Writing of a Dictionary")
    return parser.parse_args(sys.argv[1:])


@tests.checkup_last_word
def checkup_last_word() -> str:
    # checkup 'last_word' file and return 'last_word' value
    with open(main_variables.OUTPUT_FOLDER + r"\last_word", "r") as last_word_file:
        if not FileNotFoundError:
            # last_word - is a single word in 'last_word' file, but it's last in generating chain
            # last_word = word from 'last_word' file    or   'a'*3 -> 'aaa' (for example)
            word_from_last_word_file = last_word_file.readline()
            word_from_last_word_file = re.sub(r"^\s+|\n|\r|\s+$", '', word_from_last_word_file)
            last_word: str = word_from_last_word_file if word_from_last_word_file \
                else main_variables.CHARSET[0] * main_variables.PASSWORD_START_POSITION
            return last_word


def password_generator():
    # generate strings
    # write every string into 'tmp_dict' file
    # return last generated string on error

    @tests.create_empty_char_positions
    def create_empty_char_positions() -> dict:
        # word length = 7 -> dict{'char1':0, 'char2':0 .. 'char7':0}
        # where 0 - char position in CHARSET
        return {f"char{i+1}": 0 for i in range(main_variables.PASSWORD_STOP_POSITION)}

    @tests.decode_word_to_char_positions
    def decode_word_to_char_positions(word: str, char_pos: dict) -> (dict, int):
        # decode 'word' to char positions in CHARSET
        # 'aah8' -> dict{'char1':0, 'char2':0, 'char3':8, 'char4':61}
        i = 0
        for i, char in enumerate(char_pos):
            char_pos[char] = main_variables.CHARSET.find(word[i])
        return char_pos, i+1

    @tests.get_next_char_positions
    def get_next_char_positions(char_pos: dict, word_size: int) -> dict:

        def set_char_pos(w_size: int):
            char_pos[f"char{w_size}"] = char_pos[f"char{w_size}"] + 1 \
                if 0 <= char_pos[f"char{w_size}"] < main_variables.CHARSET_SIZE - 1 else 0
            return char_pos[f"char{w_size}"]  # just feed back

        def recursive_checkup(w_size):
            if set_char_pos(w_size) == 0 and w_size > 0:
                w_size -= 1
                recursive_checkup(w_size)

        recursive_checkup(word_size)
        return char_pos

    @tests.encode_char_positions_to_word
    def encode_char_positions_to_word(char_pos: dict) -> str:
        # encode char positions in word
        # dict{'char1':0, 'char2':0, 'char3':8, 'char4':61} -> 'aah8'
        word = ""
        for pos in char_pos.values():
            word = f"{word}{main_variables.CHARSET[pos]}"
        return word

    def is_dict_file_size_normal(path: str) -> bool:
        return True if os.path.getsize(path) <= main_variables.OUTPUT_FILE_SIZE else False

    def name_filtering(name: str) -> str:
        for i in main_variables.FORBIDDEN_CHARS:
            name = name.replace(i, "_")
        return name

    def rename_tmp_dict_file():
        # rename 'tmp_dict' file to '<first_string>-<last_string>.txt'
        old_name = file_full_path
        new_name: str = f"{main_variables.OUTPUT_FOLDER}\\{first_string}-{last_string}.txt"

        try:
            os.rename(old_name, new_name)
        except PermissionError:
            print(f"Unable create file '{new_name}'")

    file_full_path: str = main_variables.OUTPUT_FOLDER + r"/tmp_dict"
    with open(file_full_path, "a") as tmp_dict_file:
        empty_char_positions = create_empty_char_positions()
        last_word = checkup_last_word()
        first_string = name_filtering(last_word)
        char_positions, char_quantity = decode_word_to_char_positions(last_word, empty_char_positions)

        while True:
            if tmp_dict_file.writable() and last_word and is_dict_file_size_normal(file_full_path):
                tmp_dict_file.write(fr"{last_word}")  # for example 'aa' or 'v7-'
                tmp_dict_file.write("\r\n")

                try:
                    char_positions = get_next_char_positions(char_positions, char_quantity)
                    last_word = encode_char_positions_to_word(char_positions)
                except KeyError:
                    last_string = name_filtering(last_word)
                    break
            else:
                break

    rename_tmp_dict_file()

# -----------------------------


if __name__ == "__main__":

    cli_args = get_console_parameters()
    main_variables = global_vars.MainVariables(cli_args.start, cli_args.stop, cli_args.output)

    password_generator()
