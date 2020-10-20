from boggle import Boggle
from flask import Flask, redirect, render_template, request, session, jsonify, flash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'akdjfadifkjaelk'


boggle_game = Boggle()


@app.route('/')
def show_homepage():
    """render the html board in the template"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    games_played = session.get('played', 0)

    return render_template('index.html', board=board, highscore=highscore, games_played=games_played)


@app.route('/check-word')
def check_word():
    word = request.args['word']
    board = session['board']

    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})


@app.route('/post-score', methods=['POST'])
def post_score():
    """at end of game, front end sends the score to the back end, which tests if it's higher than the current high_score, and then sends that back to front end"""
    score = request.json['score']

    highscore = session.get('highscore', 0)
    games_played = session.get('played', 0)

    session['played'] = games_played + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newhigh=score > highscore)
