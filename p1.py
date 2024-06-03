from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# In-memory storage for polls
polls = {
    'favorite_color': {
        'question': 'What is your favorite color?',
        'options': ['Red', 'Green', 'Blue', 'Yellow'],
        'votes': [0, 0, 0, 0]
    }
}

@app.context_processor
def utility_processor():
    return dict(zip=zip)

@app.route('/')
def index():
    return render_template('index.html', polls=polls)

@app.route('/poll/<poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    poll = polls.get(poll_id)
    if not poll:
        return render_template('404.html'), 404

    if request.method == 'POST':
        option = request.form.get('option')
        if option:
            option_index = poll['options'].index(option)
            poll['votes'][option_index] += 1
            return redirect(url_for('results', poll_id=poll_id))

    return render_template('poll.html', poll_id=poll_id, poll=poll)

@app.route('/results/<poll_id>')
def results(poll_id):
    poll = polls.get(poll_id)
    if not poll:
        return render_template('404.html'), 404

    return render_template('results.html', poll_id=poll_id, poll=poll)

if __name__ == '__main__':
    app.run(debug=True)
