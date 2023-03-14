from flask import Blueprint, render_template, request, redirect, json
from .translator import translate as tl, prettier
import random
import json, os

#top directory
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

#looks for the file phrases.json
#in static/json directory, using the top directory as a prefix
json_url = os.path.join(SITE_ROOT, "static/json", "phrases.json")

#json is loaded
data = json.load(open(json_url))
  
views = Blueprint('views', __name__)
@views.route('/')
def index():
	return render_template('index.html')
    
@views.route('/translate')
def translate():
	example_sent = data[random.randint(0, len(data) - 1)]
	return render_template('translate.html', example_list=sorted(data, key=str.casefold), example_sent = example_sent)

@views.route('/learn')
def learn():
	return render_template('learn.html')

@views.route('/layout')
def layout():
	return render_template('layout.html')

@views.route('/practice')
def practice():
	return render_template('practice.html')
    
@views.route('/about_us')
def about_us():
	return render_template('about_us.html')

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