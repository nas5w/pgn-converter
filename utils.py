from os import listdir, path
import re
import math

def get_files_in_directory(dir, ext):
    all_files = listdir(dir)
    matches = [];
    for filename in all_files:
        root, end = path.splitext(filename)
        if end == ext:
            matches.append(filename)
    return matches

def convert_lichess_to_chessbase(file_path):
    with open(file_path) as f:
        file = f.read()
    # Replace emt with clk
    return file.replace("%clk", "%emt")

def convert_chessbase_to_lichess(file_path):
    with open(file_path) as f:
        file = f.read()
    # Change all "%emt" to "%clk"
    file = file.replace("%emt", "%clk")
    # Split by double line break
    file_parts = file.split("\n\n")
    # Every other line is the move data. Strip line breaks from those.
    i = 1
    while i < len(file_parts):
        # Get initial clock time
        clock_time = re.search("%clk (.*?)]", file_parts[i])
        time_control = clock_to_seconds(clock_time.group(1))
        # Insert time control
        file_parts[i-1] = f'{file_parts[i-1]}\n[TimeControl "{time_control}"]'
        # Remove line breaks
        file_parts[i] = file_parts[i].replace("\n", "")
        # Make sure clock isn't messed up
        file_parts[i] = re.sub("( :|: )", "", file_parts[i])
        i += 2

    return "\n\n".join(file_parts)

def clock_to_seconds(clock_time):
    hours, minutes, seconds = clock_time.split(":")
    total_seconds = int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)
    # Do some rounding (10 minutes)
    rounded_seconds = math.ceil(total_seconds / 600) * 600
    return f"{rounded_seconds}+0"