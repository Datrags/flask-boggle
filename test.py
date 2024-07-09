from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_boggle(self):
        with self.client:
            resp = self.client.get('/boggle?w=5&h=5')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', resp.data)
            self.assertIn(b'Score:', resp.data)
            self.assertIn(b'Seconds Left:', resp.data)
    
    def test_home(self):
        with self.client:
            resp = self.client.get('/')

    def test_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "A", "K", "E", "R"], 
                                 ["C", "O", "T", "V", "T"], 
                                 ["D", "N", "J", "N", "R"], 
                                 ["Z", "A", "S", "T", "E"], 
                                 ["X", "A", "P", "T", "Q"]]
                
                resp = self.client.get('/check-word?word=monster')
                self.assertEqual(resp.json['result'], 'ok')
               
                resp = self.client.get('/check-word?word=maker')
                self.assertEqual(resp.json['result'], 'ok')
    
    def test_invalid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "A", "K", "E", "R"], 
                                 ["C", "O", "T", "V", "T"], 
                                 ["D", "N", "J", "N", "R"], 
                                 ["Z", "A", "S", "T", "E"], 
                                 ["X", "A", "P", "T", "Q"]]
                
                resp = self.client.get('/check-word?word=zoom')
                self.assertEqual(resp.json['result'], 'not-on-board')
    def test_fake_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "A", "K", "E", "R"], 
                                 ["C", "O", "T", "V", "T"], 
                                 ["D", "N", "J", "N", "R"], 
                                 ["Z", "A", "S", "T", "E"], 
                                 ["X", "A", "P", "T", "Q"]]
                
                resp = self.client.get('/check-word?word=zsfgasge')
                self.assertEqual(resp.json['result'], 'not-word')
                
    def test_big_board(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "A", "K", "E", "R", "D"], 
                                 ["C", "O", "T", "V", "T", "O"], 
                                 ["D", "N", "J", "N", "R", "G"], 
                                 ["Z", "A", "S", "T", "E", "X"], 
                                 ["X", "A", "P", "T", "Q", "X"],
                                 ["X", "A", "P", "T", "Q", "Y"],
                                 ["X", "A", "P", "T", "Q", "H"]]
                resp = self.client.get('/check-word?word=dog')
                self.assertEqual(resp.json['result'],'ok')