from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
boggle_game = Boggle()

app = Flask(__name__)
app.secret_key = "peggyhill"

game = Boggle()

@app.route("/")
def index():
    return render_template('home.html')
@app.route("/boggle", methods=["GET"])
def boggle_page():
    print(request.args)
    x, y = request.args['w'], request.args['h']
    game = Boggle(int(x), int(y))
    board = game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("boggle.html", board=board, highscore=highscore, 
                           nplays=nplays)
@app.route("/check-word")
def check_word():
    "checks if word inputted is valid from form"

    word = request.args["word"]
    board = session["board"]
    response = game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)