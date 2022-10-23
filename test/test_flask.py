from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    # TODO -- write tests for every view function / feature!
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

    def test_home_route(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['active_game'], True)
            self.assertEqual(session['high_score'], 0)
            self.assertEqual(session['correct'], [])
            self.assertEqual(len(session['gameboard']), 5)

    def test_about_route(self):
        with app.test_client() as client:
            res = client.get('/about')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 id="boggle_heading">About</h1>', html)

    def test_dictionary_route(self):
        with app.test_client() as client:
            res = client.get('/dictionary')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 id="boggle_heading">Dictionary</h1>', html)

    def test_guess_route(self):
        """test the submiting the users guess to /guess (json) not (form)"""
        # this section does not test updating high_score
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['active_game'] = True
                change_session['high_score'] = 0
                change_session['correct'] = []
                change_session['gameboard'] = self.CONTROL_BOARD
            # should return result of 'ok' since vote is on the board and is a valid word
            res1 = client.post('/guess', json='{"guess": "vote"}')
            data1 = res1.json
            self.assertEqual(res1.status_code, 200)
            self.assertEqual(data1.get('result'), 'ok')
            # SHOULD update session list of correct words
            self.assertEqual(len(session['correct']), 1)
            self.assertEqual(session['correct'].index('vote'), 0)
            self.assertEqual(session['correct'].pop(), 'vote')

            # should return result of 'not-word' since votee is not a valid word
            res2 = client.post('/guess', json='{"guess": "votee"}')
            data2 = res2.json
            self.assertEqual(res2.status_code, 200)
            self.assertEqual(data2.get('result'), 'not-word')
            # should NOT update session list of correct words
            self.assertEqual(len(session['correct']), 1)

            # should return result of 'not-on-board' since voter is not on the CONTROL_BOARD
            res3 = client.post('/guess', json='{"guess": "voter"}')
            data3 = res3.json
            self.assertEqual(res3.status_code, 200)
            self.assertEqual(data3.get('result'), 'not-on-board')
            # should NOT update session list of correct words
            self.assertEqual(len(session['correct']), 1)

            # should return 'already used' since we have already submitted this word above
            res1 = client.post('/guess', json='{"guess": "vote"}')
            data1 = res1.json
            self.assertEqual(res1.status_code, 200)
            self.assertEqual(data1.get('result'), 'already used')
            # should NOT update session list of correct words
            self.assertEqual(len(session['correct']), 1)

    def test_record_score_high_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['active_game'] = True
                change_session['high_score'] = 2
                change_session['correct'] = ['vote', 'gum']
                change_session['gameboard'] = self.CONTROL_BOARD
            # at this point /record_score determins that 2 correct answers is not a new high score
            rec_res1 = client.post('/record_score')
            data1 = rec_res1.json
            # /record_score returns json{high_score} set to 0 which is Falsy
            self.assertFalse(data1.get('high_score'))
            # user now has 3 which is the new high score
            res = client.post('/guess', json='{"guess": "bug"}')
            self.assertEqual(len(session['correct']), 3)

            rec_res = client.post('/record_score')
            data = rec_res.json
            self.assertEqual(data.get('high_score'), 3)
            self.assertEqual(session['high_score'], 3)
