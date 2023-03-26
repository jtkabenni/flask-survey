from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
@app.route("/")
def display_home():
  print (f"response length, {responses}, {len(responses)}")
  return render_template("base.html", title = satisfaction_survey.title, instructions = satisfaction_survey.instructions, )

@app.route("/start", methods=["POST"])
def start_survey():
    responses = []
    print (f"response length, {responses}, {len(responses)}")
    return redirect ("/question/0")

@app.route("/question/<int:question_number>")
def display_question(question_number):
  if question_number != len(responses):
    flash ("Don't skip ahead!!")
    return redirect(f"/question/{len(responses)}")
  return render_template("question.html",title = satisfaction_survey.title, question = satisfaction_survey.questions[len(responses)], question_number = len(responses), next_question = (len(responses) +1) )
  

@app.route("/answer", methods=["POST"])
def manage_answers():
  answer = request.form.get("answer")
  if answer:
    responses.append(answer)
  print(responses, len(responses), len(satisfaction_survey.questions))
  if len(responses) == len(satisfaction_survey.questions):
    return redirect("/complete")
  return redirect(f"/question/{len(responses)}")

@app.route("/complete")
def say_thanks():
  return render_template("complete.html")
