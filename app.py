from flask import Flask, request, session, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "blah"

# debug = DebugToolbarExtension(app)
curr_survey = surveys['satisfaction']


@app.route('/')
def start_survey():
    session['survey'] = []
    return render_template(
        'survey.html',
        title=curr_survey.title,
        instructions=curr_survey.instructions)


@app.route('/questions/<int:number>', methods=["POST"])
def question_page(number):
    if not number == 0:
        survey = session['survey']
        survey.append(request.form['answer'])
        session['survey'] = survey

    if number < len(curr_survey.questions):
        return render_template(
            'questions.html',
            question=curr_survey.questions[number],
            number=number + 1)
    else:
        return render_template('thanks.html')
