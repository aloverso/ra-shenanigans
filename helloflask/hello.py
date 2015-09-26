from flask import Flask
from flask import request
from flask import render_template
import os
import sys

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    exact_flag = False
    if 'exact_flag' in request.form:
        exact_flag = True
    print exact_flag
    lines = "hello"
    letters = "abcdefghijklmnopqrstuvwxyz"
    all_songs = os.listdir(sys.path[0]+"/lyrics")

    search_term = text.lower()
    match_lines = []

    results = [] #list of dictionaries
    results_songs = []
    try:
        for song_file in all_songs:
            lines = []
            with app.open_resource("lyrics/"+song_file) as f:
                lines = list(f)
            for i in range(len(lines)):
                line = lines[i].lower()

                if search_term in line and line not in match_lines and i!=0:
                    context = line
                    context_arr = ["",lines[i],""]
                    if exact_flag:
                        index = context.index(search_term)
                        if index != 0 and context[index-1] in letters:
                            break
                        if index != len(context)-len(search_term) and context[index+len(search_term)] in letters:
                            break
                    match_lines.append(context)
                    if i != 0:
                        context = lines[i-1] + context
                        context_arr[0] = lines[i-1]
                    if i != len(lines)-1:
                        context += lines[i+1]
                        context_arr[2] = lines[i+1]
                    results.append({'title': lines[0] + 'contains a match!', 'body':{'line1':context_arr[0], 'line2':context_arr[1], 'line3':context_arr[2]}}) 
                    if lines[0] not in results_songs:
                    	results_songs.append(lines[0])
                    #results = results + (lines[0] + " contains a match!\n" + context) + "\n"
                    #print_match(lines[0],context)
    except:
        print 'My exception occurred, value:', sys.exc_info()

    return render_template("results.html",
                           title='Search Results for '+text,
                           search_term=text,
                           results=results,
                           count=len(results),
                           song_count=len(results_songs))

