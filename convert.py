from os import path
from os.path import isfile, join
import utils

dirname = path.dirname(__file__)

LICHESS_DIR = "./lichess"
CHESSBASE_DIR = "./chessbase"

lichess_files = utils.get_files_in_directory(LICHESS_DIR, ".pgn")
chessbase_files = utils.get_files_in_directory(CHESSBASE_DIR, ".pgn")

# Get lichess todo list
lichess_todo = []
for filename in lichess_files:
    if filename not in chessbase_files:
        lichess_todo.append(filename)

# Get chessbase todo list
chessbase_todo = []
for filename in chessbase_files:
    if filename not in lichess_files:
        chessbase_todo.append(filename)

if len(lichess_todo) > 0:
    print("Converting lichess to chessbase...")
    for filename in lichess_todo:
        converted = utils.convert_lichess_to_chessbase(f"{LICHESS_DIR}/{filename}")
        with open(path.join(dirname, f"{CHESSBASE_DIR}/{filename}"), "w") as f:
            f.write(converted)
        print(f"{filename}...DONE")


if len(chessbase_todo) > 0:
    print("Converting chessbase to lichess...")
    for filename in chessbase_todo:
        converted = utils.convert_chessbase_to_lichess(f"{CHESSBASE_DIR}/{filename}")
        with open(path.join(dirname, f"{LICHESS_DIR}/{filename}"), "w") as f:
            f.write(converted)
        print(f"{filename}...DONE")