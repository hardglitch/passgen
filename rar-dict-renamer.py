import os.path
import sys
import re
import argparse


def get_console_parameters() -> argparse:
    """ Get external console parameters
        > python rar-dict-renamer.py -d "c:/docs/" -z 2
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", nargs="?", help="Work Directory")
    parser.add_argument("-z", type=int, default=3, help="SIze of A Zero Filling")
    return parser.parse_args(sys.argv[1:])


def checkup_last_dict() -> list:

    # 0. Check up 'last_dict' file
    params = []
    try:
        # 'last_dict' file exist
        with open(WORK_DIRECTORY + r"\last_dict", "r") as file:
            for line in file:
                if line != "":
                    line = re.sub(r"^\s+|\n|\r|\s+$", '', line)
                    params = line.split(":", maxsplit=1)

    except FileNotFoundError:
        # 'last_dict' file not exist

        # 0.1. Find rar-file with max-number
        last_number = ""
        last_chars = ""
        for file in WORK_DIRECTORY_LIST:
            if file.endswith(".rar"):
                if re.match(fr"(\d{ {ZERO_FILLING} }\. )", file):
                    # copy number of 'last_dict' file
                    last_number = file[:ZERO_FILLING]
                    # copy second part of 'last_dict' file name (after " - ")
                    last_chars = file[file.rfind(" ") + 1:-4]
                else:
                    last_number = "1"
                    # copy second part of 'last_dict' file name (after "-")
                    last_chars = file[file.rfind("-")+1:-4]
                    # rename first file
                    old_filename = os.path.join(WORK_DIRECTORY, file)
                    new_filename = os.path.join(WORK_DIRECTORY, fr"{last_number:0>{ZERO_FILLING}}. "
                                                                fr"{file.replace('-', ' - ', 1)}")
                    try:
                        os.rename(old_filename, new_filename)
                    except FileNotFoundError:
                        print(f"Unable to rename old file '{old_filename}' to new file '{new_filename}'.")
                break

        # 0.2. Create 'last-dict' file
        with open(WORK_DIRECTORY + r"\last_dict", "w") as file:
            file.write(fr"{last_number:0>{ZERO_FILLING}}:{last_chars}")

        params = [last_number, last_chars]

    return params  # (number, chars)


def find_and_rename_raw_rar_file(params: list) -> list:
    for file in WORK_DIRECTORY_LIST:
        if file.endswith(".rar") and file.startswith(params[1][:-1]) or file.startswith(params[1][:-2]):
            old_filename = os.path.join(WORK_DIRECTORY, file)
            new_number = str(int(params[0]) + 1)
            new_filename = os.path.join(WORK_DIRECTORY, fr"{new_number:0>{ZERO_FILLING}}. "
                                                        fr"{file.replace('-', ' - ', 1)}")
            try:
                os.rename(old_filename, new_filename)
            except FileNotFoundError:
                print(f"Unable to rename old file '{old_filename}' to new file '{new_filename}'.")
            return [new_number, file[file.rfind("-")+1:-4]]
    return params


def file_tree_processing():
    first_last_dict_params = checkup_last_dict()
    last_dict_params = first_last_dict_params

    # rescan Work Directory after checkup_last_dict()
    global WORK_DIRECTORY_LIST
    WORK_DIRECTORY_LIST = sorted(os.listdir(WORK_DIRECTORY), key=len)       # sorted by length

    for file in WORK_DIRECTORY_LIST:
        if file.endswith(".rar") and not re.match(fr"(\d{ {ZERO_FILLING} }\. )", file):
            last_dict_params = find_and_rename_raw_rar_file(last_dict_params)

    # write 'last_number' and 'last_chars' to 'last_dict' file
    if first_last_dict_params != last_dict_params:
        with open(WORK_DIRECTORY + r"\last_dict", "w") as file:
            file.write(fr"{last_dict_params[0]:0>{ZERO_FILLING}}:{last_dict_params[1]}")


# -----------------------------

if __name__ == "__main__":

    console_arguments = get_console_parameters()

    WORK_DIRECTORY = os.path.abspath(fr"{console_arguments.dir}")           # directory
    WORK_DIRECTORY_LIST = sorted(os.listdir(WORK_DIRECTORY), key=len)       # sorted by length
    ZERO_FILLING = int(console_arguments.z)                                 # 00001 - zero filling

    file_tree_processing()
