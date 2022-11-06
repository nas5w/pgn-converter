# PGN Converter

A simple python script to convert PGN formats between LiChess and ChessBase.

# Installation

Clone down the repository:

```bash
git clone git@github.com:nas5w/pgn-converter.git
```

`cd` into the directory and run the converter

```bash
cd pgn-converter
python convert.py
```

You should see an output explaining that there are no files to be converted:

```
-----
No new lichess to chessbase files.
-----
No new chessbase to lichess files.
```

# Converting files

## LiChess to ChessBase

If you have a `pgn` file from LiChess that needs to be converted to ChessBase, put the `pgn` file in the following directory:

`lichess-to-chessbase/input`

Then, re-run the converter script:

```bash
python convert.py
```

If the conversion has been successful, you should see the following output:

```
-----
Converting 1 lichess to chessbase file(s):
  my-game-file.pgn...DONE
-----
No new chessbase to lichess files.
```

## ChessBase to LiChess

If you have a `pgn` file from ChessBase that needs to be converted to LiChess, put the `pgn` file in the following directory:

`chessbase-to-lichess/input`

Then, re-run the converter script:

```bash
python convert.py
```

If the conversion has been successful, you should see the following output:

```
-----
No new lichess to chessbase files.
-----
Converting 1 chessbase to lichess file(s):
  my-game-file.pgn...DONE
```

# Contributing

If you see any issues or want to make and contributions, please open a GitHub issue and we can discuss!
