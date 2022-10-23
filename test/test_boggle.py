from typing import Dict, List
from unittest import TestCase
# from app import app
from flask import session
from boggle import Boggle


class Boggle_Tests(TestCase):

    @classmethod
    def setUpClass(cls):
        """setup a control board + reuseable game pieces"""
        cls.CONTROL_BOARD = [['V', 'K', 'F', 'E', 'D'],
                             ['O', 'B', 'B', 'W', 'R'],
                             ['T', 'C', 'U', 'X', 'W'],
                             ['E', 'U', 'G', 'W', 'E'],
                             ['E', 'M', 'Q', 'F', 'R']]
        cls.RESPONSES = ["not-word", "not-on-board", "ok"]
        cls.boggle_instance = Boggle()
        cls.boggle_board = cls.boggle_instance.make_board()

    def test_make_board(self):
        self.assertIsInstance(self.boggle_board, List)
        for row in self.boggle_board:
            self.assertEqual(len(row), 5)
            for char in row:
                self.assertIsInstance(char, str)
        # self.assertEqual(len(self.boggle_board), 5)

    def test_words(self):
        self.assertIsInstance(self.boggle_instance.words, List)

    def test_check_valid_word(self):
        self.assertEqual(self.boggle_instance.check_valid_word(
            self.CONTROL_BOARD, 'vote'), 'ok')
        # self.assertEqual(self.boggle_instance.check_valid_word(
        #     self.CONTROL_BOARD, 'VOTE'), 'ok')
        self.assertEqual(self.boggle_instance.check_valid_word(
            self.CONTROL_BOARD, 'votee'), 'not-word')
        self.assertEqual(self.boggle_instance.check_valid_word(
            self.CONTROL_BOARD, 'voter'), 'not-on-board')

    def test_find(self):
        """test the return value from find() function. isOnTheGameBoard=True else False"""
        # MUG and HUG should be capitalized to match the game board letters.*boggle.py line36*
        self.assertTrue(self.boggle_instance.find(self.CONTROL_BOARD, 'MUG'))
        self.assertFalse(self.boggle_instance.find(self.CONTROL_BOARD, 'HUG'))

    def test_find_from(self):
        """test not writen because I dont quite understand how the algorithm works"""
        print('testing')
