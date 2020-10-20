from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        app.config['TESTING'] = True

    def test_home(self):
        """make sure homepage is rendered with html and check status code, and make sure board is in the session"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<button class="btn btn-success">GUESS!</button>', html)
            self.assertIn('board', session)

    def test_word_is_valid(self):
        """make sure valid word is counted if on board"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['B', 'R', 'E', 'A', 'D'],
                    ['B', 'R', 'E', 'A', 'D'],
                    ['B', 'R', 'E', 'A', 'D'],
                    ['B', 'R', 'E', 'A', 'D'],
                    ['B', 'R', 'E', 'A', 'D']]  # had to change the board temporarily to make sure i can test with non-random word
            response = client.get('/check-word?word=bread')
            self.assertEqual(response.json['result'], 'ok')

    def test_word_in_dictionary(self):
        """make sure that a valid word in the dictionary but not on board returns correct message"""

        with app.test_client() as client:
            client.get('/')  # reset the board from the session change earlier
            response = client.get('/check-word?word=hasenpfeffer')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_bad_word(self):
        """test a word that would be counted as invalid, like gibberish"""

        with app.test_client() as client:
            client.get('/')  # initialize a new board
            response = client.get('/check-word?word=asdfghjkllkjhgfs')

            self.assertEqual(response.json['result'], 'not-word')

    def test_score_posting(self):

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['highscore'] = 24
            response = client.post('/post-score',
                                   json={"score": 40})
            highscore = session['highscore']

            self.assertEqual(response.status_code, 200)
            self.assertEqual(highscore, 40)

    def test_games_played(self):
        with app.test_client() as client:
            client.get('/')
            with client.session_transaction() as change_session:
                change_session['played'] = 4
            response = client.post('post-score', json={"score": 40})

            games_played = session['played']

            self.assertEqual(response.status_code, 200)
            self.assertEqual(games_played, 5)
