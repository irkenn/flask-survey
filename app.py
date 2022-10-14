from urllib import response
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import current_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "there'sNoSpoon"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home():
    """Takes info from current survey var and builds a page with the title of the survey"""
    survey_title = current_survey.title
    return render_template("home.html", title=survey_title)

@app.route('/questions/<int:question_number>')
def questions(question_number):
    """This will retrieve the value as an inegrer and find the question that matches the
    index of that value"""
    
    if len(responses) == len(current_survey.questions):
        return render_template('thank-you.html')
    elif question_number <= len(current_survey.questions) and question_number == len(responses):
        current_question = current_survey.questions[question_number].question
        current_choices =  current_survey.questions[question_number].choices
        question_number += 1
        return render_template("questions.html", current_question=current_question, number=question_number, current_choices=current_choices)
    else:
        flash("You're trying to answer an invalid question, you will be redirected to your current question")
        return redirect('/questions/'+ str(len(responses))) 


@app.route('/answers/', methods=["GET", "POST"])
def answers():
    """This will retrieve the info from the form append it to the responses list
    and redirect to the questions page with a new question number"""
    
    data = request.args.to_dict()
    for key in data:
        responses.append(data[key])
    # next_question_url = '/questions/'+ str(len(responses))
    return redirect('/questions/'+ str(len(responses)))




#This is the previous working version
# @app.route('/questions/<int:question_number>')
# def questions(question_number):
#     current_question = current_survey.questions[question_number].question
#     current_choices =  current_survey.questions[question_number].choices
#     ##conditional to prevent from skipping question and redirect actions
#     ##al final del proceso
#     question_number += 1
#     return render_template("questions.html", current_question=current_question, number=question_number, current_choices=current_choices)
