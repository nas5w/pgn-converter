from os import path
from os.path import isfile, join
import utils

dirname = path.dirname(__file__)

LICHESS_INPUT_DIR = path.join(dirname, "lichess-to-chessbase", "input")
LICHESS_OUTPUT_DIR = path.join(dirname, "lichess-to-chessbase", "output")
CHESSBASE_INPUT_DIR = path.join(dirname, "chessbase-to-lichess", "input")
CHESSBASE_OUTPUT_DIR = path.join(dirname, "chessbase-to-lichess", "output")

lichess_input_files = utils.get_files_in_directory(LICHESS_INPUT_DIR, ".pgn")
lichess_output_files = utils.get_files_in_directory(LICHESS_OUTPUT_DIR, ".pgn")
chessbase_input_files = utils.get_files_in_directory(CHESSBASE_INPUT_DIR, ".pgn")
chessbase_output_files = utils.get_files_in_directory(CHESSBASE_OUTPUT_DIR, ".pgn")

# Get lichess todo list
lichess_todo = []
for filename in lichess_input_files:
    if filename not in lichess_output_files:
        lichess_todo.append(filename)

# Get chessbase todo list
chessbase_todo = []
for filename in chessbase_input_files:
    if filename not in chessbase_output_files:
        chessbase_todo.append(filename)

if len(lichess_todo) > 0:
    print("Converting lichess to chessbase...")
    for filename in lichess_todo:
        converted = utils.convert_lichess_to_chessbase(path.join(LICHESS_INPUT_DIR, filename))
        with open(path.join(LICHESS_OUTPUT_DIR, filename), "w") as f:
            f.write(converted)
        print(f"{filename}...DONE")


if len(chessbase_todo) > 0:
    print("Converting chessbase to lichess...")
    for filename in chessbase_todo:
        converted = utils.convert_chessbase_to_lichess(path.join(CHESSBASE_INPUT_DIR, filename))
        with open(path.join(CHESSBASE_OUTPUT_DIR, filename), "w") as f:
            f.write(converted)
        print(f"{filename}...DONE")