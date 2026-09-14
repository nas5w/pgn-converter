import tempfile
import unittest
import os

import utils


class TempFileMixin:
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = self._tmpdir.name

    def write_pgn(self, name, content):
        path = os.path.join(self.tmp_path, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path


class TestGetFilesInDirectory(TempFileMixin, unittest.TestCase):
    def test_finds_matching_extension(self):
        for name in ("a.pgn", "b.pgn", "c.txt"):
            open(os.path.join(self.tmp_path, name), "w").close()
        result = utils.get_files_in_directory(self.tmp_path, ".pgn")
        self.assertEqual(sorted(result), ["a.pgn", "b.pgn"])

    def test_no_matches(self):
        open(os.path.join(self.tmp_path, "a.txt"), "w").close()
        result = utils.get_files_in_directory(self.tmp_path, ".pgn")
        self.assertEqual(result, [])

    def test_empty_directory(self):
        result = utils.get_files_in_directory(self.tmp_path, ".pgn")
        self.assertEqual(result, [])

    def test_case_sensitive(self):
        for name in ("a.PGN", "b.pgn"):
            open(os.path.join(self.tmp_path, name), "w").close()
        result = utils.get_files_in_directory(self.tmp_path, ".pgn")
        self.assertEqual(result, ["b.pgn"])


LICHESS_SAMPLE = (
    '[Event "Rated Classical game"]\n'
    '[Site "https://lichess.org/abc123"]\n'
    '[Date "2021.07.30"]\n'
    '[White "player1"]\n'
    '[Black "player2"]\n'
    '[Result "1-0"]\n'
    '[TimeControl "1800+20"]\n'
    '[UTCDate "2021.07.30"]\n'
    '[UTCTime "22:23:54"]\n'
    '\n'
    '1. e4 {[%clk 1:30:00]} e5 {[%clk 1:28:00]} 2. Nf3 {[%clk 1:29:00]} 1-0\n'
)

CHESSBASE_SAMPLE = (
    '[Event "Eastern Chess Congress"]\n'
    '[Site "?"]\n'
    '[Date "2022.10.28"]\n'
    '[White "Player A"]\n'
    '[Black "Player B"]\n'
    '[Result "1-0"]\n'
    '[ECO "C90"]\n'
    '\n'
    '1. e4 {[%emt 1:20:00]} e5 {[%emt 1:18:00]} 2. Nf3 {[%emt 1:21:00]} 1-0\n'
)

CHESSBASE_NO_CLOCK = (
    '[Event "Test Game"]\n'
    '[Result "1-0"]\n'
    '\n'
    '1. e4 e5 2. Nf3 1-0\n'
)


class TestConvertLichessToChessbase(TempFileMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.pgn = self.write_pgn("game.pgn", LICHESS_SAMPLE)

    def test_replaces_clk_with_emt(self):
        result = utils.convert_lichess_to_chessbase(self.pgn)
        self.assertNotIn("%clk", result)
        self.assertIn("%emt", result)

    def test_removes_utc_fields(self):
        result = utils.convert_lichess_to_chessbase(self.pgn)
        self.assertNotIn("UTCDate", result)
        self.assertNotIn("UTCTime", result)

    def test_preserves_other_headers(self):
        result = utils.convert_lichess_to_chessbase(self.pgn)
        self.assertIn('[Event "Rated Classical game"]', result)
        self.assertIn('[TimeControl "1800+20"]', result)

    def test_preserves_move_text(self):
        result = utils.convert_lichess_to_chessbase(self.pgn)
        self.assertIn("1. e4", result)
        self.assertIn("Nf3", result)


class TestConvertChessbaseToLichess(TempFileMixin, unittest.TestCase):
    def test_replaces_emt_with_clk(self):
        pgn = self.write_pgn("game.pgn", CHESSBASE_SAMPLE)
        result = utils.convert_chessbase_to_lichess(pgn)
        self.assertNotIn("%emt", result)
        self.assertIn("%clk", result)

    def test_inserts_time_control(self):
        pgn = self.write_pgn("game.pgn", CHESSBASE_SAMPLE)
        result = utils.convert_chessbase_to_lichess(pgn)
        self.assertIn('[TimeControl "', result)

    def test_no_clock_game_no_time_control(self):
        pgn = self.write_pgn("game.pgn", CHESSBASE_NO_CLOCK)
        result = utils.convert_chessbase_to_lichess(pgn)
        self.assertNotIn("TimeControl", result)

    def test_strips_newlines_in_move_text(self):
        pgn = self.write_pgn("game.pgn", CHESSBASE_SAMPLE)
        result = utils.convert_chessbase_to_lichess(pgn)
        lines = result.split("\n\n")
        for i in range(1, len(lines), 2):
            self.assertNotIn("\n", lines[i])


class TestClockToSeconds(unittest.TestCase):
    def test_one_hour(self):
        self.assertEqual(utils.clock_to_seconds("1:00:00"), "3600+0")

    def test_thirty_minutes(self):
        self.assertEqual(utils.clock_to_seconds("0:30:00"), "1800+0")

    def test_rounds_to_600(self):
        self.assertEqual(utils.clock_to_seconds("1:20:00"), "4800+0")

    def test_rounds_up_to_next_600(self):
        self.assertEqual(utils.clock_to_seconds("0:05:00"), "600+0")

    def test_exact_round_boundary(self):
        self.assertEqual(utils.clock_to_seconds("0:10:00"), "600+0")

    def test_classical_time_control(self):
        self.assertEqual(utils.clock_to_seconds("1:30:00"), "5400+0")


if __name__ == "__main__":
    unittest.main()