from flask import Blueprint, render_template, request, redirect
from .translator import translate as tl, prettier
import random

example_list = [
    "Product of a number, 5 less than 1, 1 and sum of 4, a number, and seventy seven, times 4",
    "y added to the product of 2, forty four, eight, and a number.",
    "2y plus the product of two, 4, eight and twice x",
    "Three diminished by the sum of two and four",
    "Quotient of a number and a sum of 4, a number, and 7, times 4"
]

views = Blueprint('views', __name__)
@views.route('/')
def index():
	return render_template('index.html')
    
@views.route('/translate')
def translate():
	example_sent = example_list[random.randint(0, len(example_list) - 1)]
	return render_template('translate.html', translation="", example_sent = example_sent, last_input = example_sent)

@views.route('/learn')
def learn():
	return render_template('learn.html')

@views.route('/layout')
def layout():
	return render_template('layout.html')

@views.route('/practice')
def practice():
	return render_template('practice.html')
    
@views.route('/the_team')
def the_team():
	return render_template('the_team.html')

@views.route('/_submit_sentence', methods=['POST'])
def submit_sentence():
    sentence = request.form.get('sentence')
    print(sentence)
    lis = tl(sentence)
    if type(lis) is list and all(lis):
        temp = "<p><b>Output:</b>"
        if len(lis) > 1:
            temp += "<br/>Ambiguous Sentence"
        temp += "</p>"
        temp += "<br/> <hr/>".join(["`"+prettier(i)+"`" for i in lis])
        lis = temp
    return lis