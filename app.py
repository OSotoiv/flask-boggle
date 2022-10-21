from crypt import methods
import json
from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'FLASK-boggle'

boggle_game = Boggle()


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/start')
def start():
    board = boggle_game.make_board()
    session['gameboard'] = board
    session['correct'] = []
    # flash('New Game!', "success")
    return render_template('start.html', board=board)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/guess', methods=["POST"])
def guess():
    # jsonify() will set Respons Header Content-Type -> application/json
    word = request.get_json().get('guess')
    board = session.get('gameboard')
    res = boggle_game.check_valid_word(board, word)
    if res == 'ok':
        correct_list = session['correct']
        if word in correct_list:
            return jsonify({'result': 'already used'})
        correct_list.append(word)
        session['correct'] = correct_list
        print(correct_list)
    return jsonify({'result': res})
