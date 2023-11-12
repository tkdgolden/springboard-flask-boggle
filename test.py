from unittest import TestCase
from app import app, no_duplicate, check
from flask import session


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_index(self):
    # / renders index page, not game board yet
    # initializes high_score and games_played to 0

        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="h1">Want to Play Boggle?</h1>', html)
            self.assertEqual(session['high_score'], 0)
            self.assertEqual(session['games_played'], 0)

    def test_new(self):
    # /new creates new board and renders board page
    # initializes score to 0 and guesses to empty array

        with app.test_client() as client:
            resp = client.get('/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="h1">Boggle</h1>', html)
            self.assertEqual(session['score'], 0)
            self.assertEqual(session['guesses'], [])

    def test_no_duplicate(self):
    # checks for guess in session["guesses"]
    # returns "ok" or "duplicate-word"

        with app.test_client() as client:
            client.get('/new')
            guesses = ["hero", "help", "cat"]

            self.assertEqual(no_duplicate("dog", guesses), "ok")
            self.assertEqual(no_duplicate("hero", guesses), "duplicate-word")
            self.assertEqual(no_duplicate("Help", guesses), "duplicate-word")

    def test_check(self):
    # check four responses: duplicate, not-word, not-on-board, ok
    # only ok should update score

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [['R', 'P', 'I', 'C', 'Q'], ['G', 'Q', 'N', 'R', 'H'], ['T', 'R', 'D', 'R', 'Z'], ['N', 'G', 'G', 'C', 'B'], ['C', 'F', 'Q', 'R', 'E']]
                change_session["guesses"] = ["reb"]
                change_session["score"] = 3

            # no score update on duplicate word
            resp = client.get('/check?guess=reb')
            self.assertEqual(resp.status_code, 200)
            resp = resp.get_json()
            self.assertEqual(resp["result"], "duplicate-word")
            self.assertEqual(resp["score"], 3)

            # no score update on invalid word
            resp = client.get('/check?guess=nir')
            self.assertEqual(resp.status_code, 200)
            resp = resp.get_json()
            self.assertEqual(resp["result"], "not-word")
            self.assertEqual(resp["score"], 3)

            # no score update on not on board
            resp = client.get('/check?guess=pink')
            self.assertEqual(resp.status_code, 200)
            resp = resp.get_json()
            self.assertEqual(resp["result"], "not-on-board")
            self.assertEqual(resp["score"], 3)

            # score update on ok word
            resp = client.get('/check?guess=pin')
            self.assertEqual(resp.status_code, 200)
            resp = resp.get_json()
            self.assertEqual(resp["result"], "ok")
            self.assertEqual(resp["score"], 6)

    def test_update_leaderboard(self):
    # increment games played
    # change high score if beaten
    # leave high score if not

        with app.test_client() as client:
            # didnt beat high score
            with client.session_transaction() as change_session:
                change_session["games_played"] = 2
                change_session["score"] = 20
                change_session["high_score"] = 30
            resp = client.get('/update_leaderboard')
            self.assertEqual(resp.status_code, 200)
            resp = resp.get_json()
            self.assertEqual(resp["games_played"], 3)
            self.assertEqual(resp["high_score"], 30)

            # did beat high score
            with client.session_transaction() as change_session:
                change_session["games_played"] = 2
                change_session["score"] = 40
                change_session["high_score"] = 30
            resp = client.get('/update_leaderboard')
            self.assertEqual(resp.status_code, 200)
            resp = resp.get_json()
            self.assertEqual(resp["games_played"], 3)
            self.assertEqual(resp["high_score"], 40)