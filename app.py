from flask import Flask, request, session, render_template, redirect
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "blah"

# debug = DebugToolbarExtension(app)
curr_survey = surveys['satisfaction']
comments = []


@app.route('/')
def select_survey():
    '''Initial landing page that allows you to select a survey to take'''
    return render_template('select.html', surveys=surveys)


@app.route('/', methods=["POST"])
def redirect_selected_survey():
    '''Redirects to the survey endpoint'''
    selected = request.form['selected_survey']
    global curr_survey
    curr_survey = surveys[selected]
    return redirect(f'/{selected}')


@app.route('/<selected_survey>')
def start_survey(selected_survey):
    '''Generates the starter page for starting a survey'''

    session['survey'] = []
    return render_template(
        'survey.html',
        survey=selected_survey,
        title=curr_survey.title,
        instructions=curr_survey.instructions)


@app.route('/<selected_survey>/questions/<int:number>', methods=["POST"])
def question_page(selected_survey, number):
    '''Loops through each question and updates the survey answers in the session list.'''

    if not number == 0:
        survey = session['survey']
        survey.append(request.form['answer'])
        session['survey'] = survey
        comment = request.form.get('comment', None)

    if number < len(curr_survey.questions):
        return render_template(
            'questions.html',
            survey=selected_survey,
            comments=comments,
            question=curr_survey.questions[number],
            number=number + 1)
    else:
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    '''Generates a thanks page that shows your answers'''
    return render_template(
        'thanks.html',
        comments=comments,
        enum=enumerate(session['survey']),
        question=curr_survey.questions)
