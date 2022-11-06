from os import listdir, path

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
    # Remove line breaks
    file = file.replace("\n", "")
    return file

    '''
1) Change all "%emt" to "%clk"
- Note: Lichess has spaces between { and [; ChessBase does not.  I don't think this needs to be altered, I've found it works in either format. 

2) Remove line breaks.  Note that after removing line breaks would need to check if a line break occurred in the middle of a clock time, resulting in 0: 00:00 or 0:00 :00 (instead of  0:00:00), or different permutations of this. It would be good also to check that a space is maintained between adjacent words.

3) Extra bonus: Add the "Time Control" field; this will make it so that when the pieces are in starting position in Lichess, the clock times are shown for both players (without it the clock doesn't show for each color until after each color's first move). I haven't found a way to input this into ChessBase (not sure if there is a way), so the file doesn't show anything for this field.
In the example file, I think the script could read white's first move clock time (1:20:00) and apply that as a time control. Note the clock times are in H:MM:SS.  The "TimeControl" field for Lichess is in seconds (the+20 at the end is increment; it's okay to always assume zero increment for these games).  
So the 1:20:00 time from white's first move would result in a new PGN line of [TimeControl "4800+0"]
    '''