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
	example_sent = example_list[random.randint(0, len(example_list) - 1)]
	return render_template('index.html', translation="", example_sent = example_sent, last_input = example_sent)
    
@views.route('/translate') #only here for compatibility, should be deprecated later
def translate():
	return redirect("/")

@views.route('/learn')
def learn():
	return render_template('learn.html')

@views.route('/practice')
def practice():
	return render_template('practice.html')
    
@views.route('/what_is_transpose')
def what_is_transpose():
	return render_template('what_is_transpose.html')
    
@views.route('/why_transpose')
def why_transpose():
	return render_template('why_transpose.html')

@views.route('/how_does_it_work')
def how_does_it_work():
	return render_template('how_does_it_work.html')
    
@views.route('/how_to_use_it')
def how_to_use_it():
	return render_template('how_to_use_it.html')

@views.route('/the_team')
def the_team():
	return render_template('the_team.html')

@views.route('/_bar',)
def _bar():
	return render_template('_bar.html')

@views.route('/_bar2',)
def _bar2():
	return render_template('_bar2.html')

@views.route('/_submit_sentence', methods=['POST'])
def submit_sentence():
	sentence = request.form.get('sentence')
	print(sentence)
	lis = tl(sentence)
	try: 
		lis = "<p style = 'color: white'>Output:<br>" + (prettier(lis))
	except:
		if type(lis) is list and all(lis):
			temp = "<p style = 'color: white'><b>Output:</b><br> Ambiguous Sentence</p>"
			temp += "<br>".join([prettier(i) for i in lis])
			lis = temp
	return lis