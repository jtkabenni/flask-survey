from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secrets"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def display_home():
    """Display home page"""
    return render_template("base.html", survey=satisfaction_survey, )


@app.route("/start", methods=["POST"])
def start_survey():
    """Manage start survey post request"""
    session["responses"] = []
    return redirect("/question/0")


@app.route("/question/<int:question_number>")
def display_question(question_number):
    """Display next question in survey"""
    responses = session["responses"]
    if question_number != len(session["responses"]):
        flash("Don't skip ahead!!")
        return redirect(f"/question/{len(responses)}")
    return render_template("question.html", survey=satisfaction_survey, question=satisfaction_survey.questions[len(session["responses"])])


@app.route("/answer", methods=["POST"])
def manage_answers():
    """ Manage add answer post request"""
    answer = request.form.get("answer")
    responses = session["responses"]
    if answer:
        session["responses"].append(answer)
    session["responses"] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")

    return redirect(f"/question/{len(responses)}")


@app.route("/complete")
def say_thanks():
    """Display thanks/completed page after all questions are answered"""
    return render_template("complete.html", survey=satisfaction_survey)


@app.route("/answers")
def get_answers():
    return session["responses"]
