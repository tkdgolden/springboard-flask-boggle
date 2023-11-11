from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route("/")
def index(): 
    session["high_score"] = 0
    session["games_played"] = 0
    session["board"] = boggle_game.make_board()
    session["score"] = 0
    session["guesses"] = []
    return render_template("index.html", board=session["board"])

@app.route("/check")
def check():
    guess = request.args.get("guess")
    response = boggle_game.check_valid_word(session["board"], guess)
    if response == "ok":
        if guess not in session["guesses"]:
            guesses = session["guesses"]
            guesses.append(guess)
            session["guesses"] = guesses
            session["score"] += len(guess)
        else:
            response = "duplicate-word"
    json_response = jsonify({"result": response, "score": session["score"]})
    return json_response

@app.route("/update_leaderboard")
def update_leaderboard():
    session["games_played"] += 1
    final_score = session["score"]
    high_score = session["high_score"]
    if (final_score > high_score):
        session["high_score"] = final_score
    json_response = jsonify({"games_played": session["games_played"], "high_score": session["high_score"]})
    return json_response