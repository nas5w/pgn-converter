from os import listdir, path
from os.path import isfile, join

LICHESS_DIR = "./lichess"
CHESSBASE_DIR = "./chessbase"

def get_files_in_directory(dir, ext):
    all_files = listdir(dir)
    matches = [];
    for filename in all_files:
        root, end = path.splitext(filename)
        if end == ext:
            matches.append(filename)
    return matches

lichess_files = get_files_in_directory(LICHESS_DIR, ".pgn")
chessbase_files = get_files_in_directory(CHESSBASE_DIR, ".pgn")

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

def convert_lichess_to_chessbase(filename):
    with open(f"{LICHESS_DIR}/{filename}") as f:
        file = f.read()
    # Replace emt with clk
    return file.replace("%emt", "%clk")

if len(lichess_todo) > 0:
    print("Converting lichess to chessbase...")
    for filename in lichess_todo:
        converted = convert_lichess_to_chessbase(filename)
        with open(f"{CHESSBASE_DIR}/{filename}", 'w') as f:
            f.write(converted)
        print(f"{filename}...DONE")


if len(chessbase_todo) > 0:
    print("Converting chessbase to lichess...")