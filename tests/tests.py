from unittest import TestCase
from main import *


class PlayfairTest(TestCase):
	def test_replace_language_specific_characters_english(self):
		self.assertEqual(filterKey("Joke", "en"), "IOKE")

	def test_replace_language_specific_characters_czech(self):
		self.assertEqual(filterKey("Quasimodo", "cs"), "OUASIMOD")

	def test_replace_language_specific_characters_invalid(self):
		with self.assertRaises(ValueError):
			filterKey("not important", "es")

	def test_filter_key_unicode(self):
		self.assertEqual(filterKey("Černá", "cs"), "CERNA")

	def test_filter_key_special_characters(self):
		self.assertEqual(filterKey("Huge World! ", "en"), "HUGEWORLD")

	def test_filter_key_duplicate_characters(self):
		self.assertEqual(filterKey("thebesttextever", "en"), "THEBSXVR")

	def test_generate_cipher_matrix_english(self):
		self.assertEqual(
			generateCipherMatrix("Monarchy", "en"), [
				["M", "O", "N", "A", "R"],
				["C", "H", "Y", "B", "D"],
				["E", "F", "G", "I", "K"],
				["L", "P", "Q", "S", "T"],
				["U", "V", "W", "X", "Z"]
			]
		)

	def test_generate_cipher_matrix_czech(self):
		self.assertEqual(
			generateCipherMatrix("Monarchie", "cs"), [
				["M", "O", "N", "A", "R"],
				["C", "H", "I", "E", "B"],
				["D", "F", "G", "J", "K"],
				["L", "P", "S", "T", "U"],
				["V", "W", "X", "Y", "Z"]
			]
		)

	def test_filter_plaintext(self):
		self.assertEqual(
			filterPlainText("Attack at 8 AM!", "en"),
			"ATTACKXSPACEXATXSPACEXXEIGHTXXSPACEXAM"
		)

	def test_convert_string_representations_back(self):
		self.assertEqual(
			convertStringRepresentationsBack("ATTACKXSPACEXATXSPACEXXEIGHTXXSPACEXAM"),
			"ATTACK AT 8 AM"
		)

	def test_fill_plain_text_with_extra_characters(self):
		self.assertEqual(
			fillPlainTextWithExtraCharacters("XXXWWWWW"),
			"XWXWXWWXWXWXWX"
		)

	def test_convert_text_to_digraphs(self):
		self.assertEqual(
			convertTextToDigraphs("ALLOWX"),
			["AL", "LO", "WX"]
		)

	def test_get_positionInmatrix(self):
		test_matrix: list[list[str]] = [
			["M", "O", "N", "A", "R"],
			["C", "H", "Y", "B", "D"],
			["E", "F", "G", "I", "K"],
			["L", "P", "Q", "S", "T"],
			["U", "V", "W", "X", "Z"]]
		self.assertEqual(
			getPositionInMatrix("Q", test_matrix),
			(3, 2)
		)

	def test_encrypt_english(self):
		self.assertEqual(
			encrypt("Gravity Falls", "Attack at dawn!", "en"),
			"GFFGBMZLNIDHWVLQHZRDOVNFAW"
		)

	def test_encrypt_czech(self):
		self.assertEqual(
			encrypt("Josef Čapek", "Zaútočte za úsvitu", "cs"),
			"WBMUJAYKSPKPKJYVPWPHPASYRFYDUM"
		)

	def test_decrypt_english(self):
		self.assertEqual(
			decrypt("Gravity Falls", "GFFGB MZLNI DHWVL QHZRD OVNFA W", "en"),
			"ATTACK AT DAWN"
		)

	def test_decrypt_czech(self):
		self.assertEqual(
			decrypt("Josef Čapek", "WBMUJ AYKSP KPKJY VPWPH PASYR FYDUM", "cs"),
			"ZAUTOCTE ZA USVITU"
		)
