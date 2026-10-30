"""Characterization tests for maincode.py: every ending, saving and loading.

Each test plays the game with scripted answers and points the save path at a
temporary file, so the tracked savefile.txt is never touched.
"""

import io
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

import maincode


class GameTestCase(unittest.TestCase):

	def setUp(self):
		directory = tempfile.TemporaryDirectory()
		self.addCleanup(directory.cleanup)
		self.savepath = os.path.join(directory.name, "savefile.txt")
		patcher = mock.patch.object(maincode, "save", self.savepath)
		patcher.start()
		self.addCleanup(patcher.stop)

	def play(self, *answers):
		"""Run main() with the given answers; return everything it printed."""
		output = io.StringIO()
		with mock.patch("builtins.input", side_effect=list(answers)), redirect_stdout(output):
			with self.assertRaises(SystemExit):
				maincode.main()
		return output.getvalue()

	def writesave(self, contents):
		with open(self.savepath, "w") as savefile:
			savefile.write(contents)

	def readsave(self):
		with open(self.savepath) as savefile:
			return savefile.read()


class TestEndings(GameTestCase):

	def test_staying_outside_the_cave_ends_the_game(self):
		output = self.play("NO", "NO", "")
		self.assertIn("staring at the sun until you go blind", output)
		self.assertIn("Game over.", output)

	def test_leaving_the_chest_closed_ends_the_game(self):
		output = self.play("NO", "YES", "NO", "")
		self.assertIn("It eats you. Game over.", output)

	def test_going_down_the_hole_ends_the_game(self):
		output = self.play("NO", "YES", "YES", "DOWN", "")
		self.assertIn("You're trapped. Game over.", output)

	def test_leaving_the_cave_wins(self):
		output = self.play("NO", "YES", "YES", "LEAVE", "")
		self.assertIn("crack open a Pepsi", output)
		self.assertNotIn("Game over.", output)

	def test_answers_ignore_case_and_surrounding_spaces(self):
		output = self.play(" no ", "yes", " Yes", "leave ", "")
		self.assertIn("crack open a Pepsi", output)


class TestInvalidAnswers(GameTestCase):

	def test_invalid_answer_to_the_opening_question(self):
		output = self.play("MAYBE", "")
		self.assertIn("That wasn't an option!", output)
		self.assertNotIn("You come across a cave!", output)

	def test_invalid_answer_at_each_decision(self):
		for answers in (("NO", "MAYBE"), ("NO", "YES", "MAYBE"), ("NO", "YES", "YES", "MAYBE")):
			with self.subTest(answers=answers):
				output = self.play(*answers, "")
				self.assertIn("That wasn't an option!", output)

	def test_invalid_answer_keeps_an_earlier_save(self):
		self.writesave("seconddecision")
		output = self.play("YES", "MAYBE", "")
		self.assertIn("That wasn't an option!", output)
		self.assertEqual(self.readsave(), "seconddecision")


class TestSaving(GameTestCase):

	def test_starting_a_new_game_clears_an_existing_save(self):
		self.writesave("thirddecision")
		self.play("NO", "NO", "")
		self.assertEqual(self.readsave(), "")

	def test_save_records_the_decision_the_player_stopped_at(self):
		for answers, decision in (
				(("NO", "SAVE"), "firstdecision"),
				(("NO", "YES", "SAVE"), "seconddecision"),
				(("NO", "YES", "YES", "SAVE"), "thirddecision")):
			with self.subTest(decision=decision):
				self.play(*answers, "")
				self.assertEqual(self.readsave(), decision)


class TestLoading(GameTestCase):

	def test_loading_resumes_at_the_saved_decision(self):
		for decision, prompt in (
				("firstdecision", "You come across a cave!"),
				("seconddecision", "You find a treasure chest in the cave!"),
				("thirddecision", "There's a hole in the chest")):
			with self.subTest(decision=decision):
				self.writesave(decision)
				output = self.play("YES", "SAVE", "")
				self.assertIn("Loading up your save!", output)
				self.assertIn(prompt, output)
				# Saving again after a load records the same decision.
				self.assertEqual(self.readsave(), decision)

	def test_loading_skips_earlier_decisions(self):
		self.writesave("thirddecision")
		output = self.play("YES", "LEAVE", "")
		self.assertNotIn("You come across a cave!", output)
		self.assertIn("crack open a Pepsi", output)

	def test_empty_save_starts_from_the_beginning(self):
		self.writesave("")
		output = self.play("YES", "NO", "")
		self.assertIn("It doesn't look like you have a save", output)
		self.assertIn("You come across a cave!", output)

	def test_missing_save_starts_from_the_beginning(self):
		self.assertFalse(os.path.exists(self.savepath))
		output = self.play("YES", "NO", "")
		self.assertIn("It doesn't look like you have a save", output)
		self.assertIn("You come across a cave!", output)

	def test_save_surrounded_by_whitespace_still_loads(self):
		self.writesave("seconddecision\n")
		output = self.play("YES", "SAVE", "")
		self.assertIn("Loading up your save!", output)
		self.assertIn("You find a treasure chest in the cave!", output)

	def test_every_way_into_the_game_mentions_save(self):
		for contents in ("", "firstdecision", "seconddecision", "thirddecision"):
			with self.subTest(contents=contents):
				self.writesave(contents)
				output = self.play("YES", "SAVE", "")
				self.assertIn("Type SAVE at any time to SAVE and quit.", output)
		with self.subTest(contents="new game"):
			output = self.play("NO", "SAVE", "")
			self.assertIn("Type SAVE at any time to SAVE and quit.", output)

	def test_unrecognized_save_contents_end_the_program(self):
		self.writesave("fourthdecision")
		output = self.play("YES", "")
		self.assertIn("Your save file couldn't be read.", output)
		self.assertNotIn("That wasn't an option!", output)
		self.assertNotIn("Loading up your save!", output)

	def test_save_that_is_not_text_ends_the_program(self):
		with open(self.savepath, "wb") as savefile:
			savefile.write(b"\xff\xfe\x00")
		output = self.play("YES", "")
		self.assertIn("Your save file couldn't be read.", output)
		self.assertNotIn("Loading up your save!", output)

	def test_save_that_cannot_be_opened_ends_the_program(self):
		# A directory where the save file should be can't be opened for reading, as with a save file the player can't read.
		os.mkdir(self.savepath)
		output = self.play("YES", "")
		self.assertIn("Your save file couldn't be read.", output)
		self.assertNotIn("Loading up your save!", output)


class TestUnwritableSaveFile(GameTestCase):

	def setUp(self):
		super().setUp()
		# A save path inside a directory that doesn't exist can't be written, as in a read-only install.
		unwritable = os.path.join(os.path.dirname(self.savepath), "missing", "savefile.txt")
		patcher = mock.patch.object(maincode, "save", unwritable)
		patcher.start()
		self.addCleanup(patcher.stop)

	def play(self, *answers):
		"""Like GameTestCase.play, but the output also includes the prompts passed to input()."""
		remaining = list(answers)
		def answer(prompt=""):
			print(prompt)
			return remaining.pop(0)
		output = io.StringIO()
		with mock.patch("builtins.input", side_effect=answer), redirect_stdout(output):
			with self.assertRaises(SystemExit):
				maincode.main()
		return output.getvalue()

	def test_new_game_still_starts(self):
		output = self.play("NO", "YES", "YES", "LEAVE", "")
		self.assertIn("Your save file (savefile.txt beside maincode.py) can't be written", output)
		self.assertIn("crack open a Pepsi", output)

	def test_save_reports_that_the_game_was_not_saved(self):
		for answers in (("NO", "SAVE"), ("NO", "YES", "SAVE"), ("NO", "YES", "YES", "SAVE")):
			with self.subTest(answers=answers):
				output = self.play(*answers, "")
				self.assertIn("Your game couldn't be saved", output)
				self.assertNotIn("see you later!", output)


class TestRunningAsAScript(unittest.TestCase):

	def run_copy(self, answers):
		"""Run a copy of maincode.py from an unrelated working directory.

		Returns (the copy's directory, the working directory, the completed process).
		"""
		gamedirectory = tempfile.TemporaryDirectory()
		self.addCleanup(gamedirectory.cleanup)
		workingdirectory = tempfile.TemporaryDirectory()
		self.addCleanup(workingdirectory.cleanup)
		shutil.copy(maincode.__file__, gamedirectory.name)
		process = subprocess.run(
			[sys.executable, os.path.join(gamedirectory.name, "maincode.py")],
			input=answers, cwd=workingdirectory.name,
			capture_output=True, text=True, timeout=30)
		return gamedirectory.name, workingdirectory.name, process

	def test_script_plays_through_to_an_ending(self):
		_, _, process = self.run_copy("NO\nYES\nYES\nLEAVE\n\n")
		self.assertEqual(process.returncode, 0, process.stderr)
		self.assertIn("crack open a Pepsi", process.stdout)

	def test_save_is_written_beside_maincode_not_in_the_working_directory(self):
		gamedirectory, workingdirectory, process = self.run_copy("NO\nSAVE\n\n")
		self.assertEqual(process.returncode, 0, process.stderr)
		with open(os.path.join(gamedirectory, "savefile.txt")) as savefile:
			self.assertEqual(savefile.read(), "firstdecision")
		self.assertEqual(os.listdir(workingdirectory), [])

	def test_end_of_input_at_an_ending_exits_cleanly(self):
		_, _, process = self.run_copy("NO\nNO\n")
		self.assertEqual(process.returncode, 0, process.stderr)
		self.assertEqual(process.stderr, "")
		self.assertIn("Game over.", process.stdout)

	def test_end_of_input_at_a_decision_exits_cleanly(self):
		_, _, process = self.run_copy("NO\n")
		self.assertEqual(process.returncode, 0, process.stderr)
		self.assertEqual(process.stderr, "")
		self.assertIn("You come across a cave!", process.stdout)

	@unittest.skipIf(sys.platform == "win32", "SIGINT cannot be sent to a child process on Windows")
	def test_ctrl_c_at_a_prompt_exits_cleanly(self):
		gamedirectory = tempfile.TemporaryDirectory()
		self.addCleanup(gamedirectory.cleanup)
		shutil.copy(maincode.__file__, gamedirectory.name)
		process = subprocess.Popen(
			[sys.executable, os.path.join(gamedirectory.name, "maincode.py")],
			stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		self.addCleanup(process.kill)
		# The welcome line is flushed when the game waits for the first answer.
		self.assertIn("Welcome to Cave!", process.stdout.readline() + process.stdout.readline())
		process.send_signal(signal.SIGINT)
		_, stderr = process.communicate(timeout=30)
		self.assertEqual(process.returncode, 0, stderr)
		self.assertEqual(stderr, "")
		self.assertNotIn("savefile.txt", os.listdir(gamedirectory.name))

	def test_end_of_input_after_saving_keeps_the_save(self):
		gamedirectory, _, process = self.run_copy("NO\nYES\nSAVE\n")
		self.assertEqual(process.returncode, 0, process.stderr)
		with open(os.path.join(gamedirectory, "savefile.txt")) as savefile:
			self.assertEqual(savefile.read(), "seconddecision")


if __name__ == "__main__":
	unittest.main()
