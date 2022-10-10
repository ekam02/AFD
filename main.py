from flask import Flask, request, jsonify, render_template
from afd import *


app = Flask(__name__)


# bot = None
#
#
# def test():
bot = Bot(5, 'bacd')
bot.nodes['q0'].status = 1
bot.nodes['q2'].status = 1
bot.nodes['q4'].status = 1

bot.nodes['q0'].vertexes = {'b': 'q1', 'c': 'q3', 'd': 'q4'}
bot.nodes['q1'].vertexes = {'a': 'q2'}
bot.nodes['q2'].vertexes = {'b': 'q1', 'c': 'q3', 'd': 'q4'}
bot.nodes['q3'].vertexes = {'c': 'q3', 'd': 'q4'}
bot.nodes['q4'].vertexes = {'c': 'q3', 'd': 'q4'}


@app.route('/')
def index():
    return jsonify({})


@app.route('/test/')
def test():
    word = list(request.args.get('word', ''))
    steps, validation = bot.extended_transition(word)
    return render_template('output.html', steps=steps, validation=validation)

    # if request.method == 'POST':
    #     word = request.form.get('word')
    #     steps, validation = bot.extended_transition(word)
    #     return render_template('output.html', steps=steps, validation=validation)
    # if request.method == 'GET':
    #     return render_template('input.html')


if __name__ == '__main__':
    app.run(debug=True)
