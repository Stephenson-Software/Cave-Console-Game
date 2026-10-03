"""Characterization tests for maincode.py: every ending, saving and loading.

Each test plays the game with scripted answers and points the save path at a
temporary file, so the tracked savefile.txt is never touched.
"""

import io
import os
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

	def test_unrecognized_save_contents_end_the_program(self):
		self.writesave("fourthdecision")
		output = self.play("YES", "")
		self.assertIn("That wasn't an option!", output)
		self.assertNotIn("Loading up your save!", output)


if __name__ == "__main__":
	unittest.main()
