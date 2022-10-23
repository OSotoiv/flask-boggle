from crypt import methods
from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'FLASK-boggle'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar_debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def home():
    board = boggle_game.make_board()
    if not session.get('active_game'):
        session['active_game'] = True
        session['high_score'] = 0
    session['gameboard'] = board
    session['correct'] = []
    return render_template('game_on.html', board=board)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/dictionary')
def dictionary():
    return render_template('dictionary.html')


@app.route('/guess', methods=["POST"])
def guess():
    """handles users submitting word/guess"""
    # jsonify() will set Respons Header Content-Type -> application/json
    json_data = request.get_json()
    data = json.loads(json_data)
    word = data.get('guess')
    board = session.get('gameboard')
    res = boggle_game.check_valid_word(board, word)
    if res == 'ok':
        correct_list = session['correct']
        if word in correct_list:
            return jsonify({'result': 'already used'})
        correct_list.append(word)
        session['correct'] = correct_list
    return jsonify({'result': res})


@app.route('/record_score', methods=["POST"])
def record_score():
    """checks for highscore and records it to the session"""
    current_score = len(session['correct'])
    high_score = session['high_score']
    if int(current_score) > int(high_score):
        session['high_score'] = current_score
        return jsonify({'high_score': int(current_score)})
    return jsonify({'high_score': 0})
