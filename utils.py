from os import listdir, path
import re

dirname = path.dirname(__file__)

def get_files_in_directory(dir, ext):
    all_files = listdir(path.join(dirname, dir))
    matches = [];
    for filename in all_files:
        root, end = path.splitext(filename)
        if end == ext:
            matches.append(filename)
    return matches

def convert_lichess_to_chessbase(file_path):
    with open(path.join(dirname, file_path)) as f:
        file = f.read()
    # Replace emt with clk
    return file.replace("%clk", "%emt")

def convert_chessbase_to_lichess(file_path):
    with open(path.join(dirname, file_path)) as f:
        file = f.read()
    # Change all "%emt" to "%clk"
    file = file.replace("%emt", "%clk")
    # Split by double line break
    file_parts = file.split("\n\n")
    # Every other line is the move data. Strip line breaks from those.
    i = 1
    while i < len(file_parts):
        file_parts[i] = file_parts[i].replace("\n", "")
        # Make sure clock isn't messed up
        file_parts[i] = re.sub("( :|: )", "", file_parts[i])
        i += 2

    return "\n\n".join(file_parts)
