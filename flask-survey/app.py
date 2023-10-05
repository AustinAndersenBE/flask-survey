from flask import Flask, render_template, request, redirect, session, flash
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "Crunch225"

@app.route('/start', methods=['POST'])
def start_survey():
    """Initialize the session to track responses and start the survey."""
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/')
def show_survey():
    """Show the survey start page."""

    return render_template('survey_start.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get('responses')

    if (responses is None) or (qid != len(responses)) or (qid >= len(satisfaction_survey.questions)):
        flash("Invalid question. Redirecting...", "warning")
        return redirect(f'/questions/{len(responses)}')
    """Show current question."""
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question)

@app.route('/answer', methods=['POST'])
def handle_answer():
    """Save answer and redirect to next question."""

    answer = request.form['choice']

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    next_qid = len(responses)
    if next_qid >= len(satisfaction_survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{next_qid}')
    
@app.route('/thank-you')
def show_thank_you_page():
    """Show survey completion page."""

    return render_template('thank_you_page.html')

@app.route('/reset', methods=['POST'])
def reset_survey():
    """Reset the survey."""
    session['responses'] = []
    flash("Survey will be reset", "info")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
### to do: clear session after survey is completed