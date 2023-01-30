from flask import Blueprint, render_template, request
from .translator import translation
from .translator import prettier
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
	example_sent = example_list[random.randint(0, len(example_list) - 1)]
	return render_template('home.html', translation="", example_sent = example_sent, last_input = example_sent)

@views.route('/Translate')
def translate():
	example_sent = example_list[random.randint(0, len(example_list) - 1)]
	return render_template('translate.html', translation="", example_sent = example_sent, last_input = example_sent)

@views.route('/Learn')
def learn():
	return render_template('learn.html')

@views.route('/Practice')
def practice():
	return render_template('practice.html')
    
@views.route('/What_is_Transpose')
def what_is_transpose():
	return render_template('what_is_transpose.html')
    
@views.route('/Why_Transpose')
def why_transpose():
	return render_template('why_transpose.html')

@views.route('/How_Does_It_Work')
def how_does_it_work():
	return render_template('how_does_it_work.html')
    
@views.route('/How_To_Use_It')
def how_to_use_it():
	return render_template('how_to_use_it.html')

@views.route('/The_Team')
def the_team():
	return render_template('the_team.html')

@views.route('/_submit_sentence', methods=['POST'])
def submit_sentence():
	sentence = request.form.get('sentence')
	lis = translation(sentence)
	try: 
		lis = "<h5><b>Output:</b><br><br>" + (prettier(lis))
	except:
		if type(lis) is list and all(lis):
			temp = "<h5><b>Output:</b> <br><br> Ambiguous Sentence</h5>"
			temp += "<br>".join([prettier(i) for i in lis])
			lis = temp
	return lis
