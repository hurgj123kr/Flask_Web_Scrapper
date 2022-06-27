from flask import Flask,render_template, redirect, request
from scrapper import get_jobs 

app = Flask("Flask_Web_Scrapper")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/report", methods=["GET"])
def results():
    word = request.args.get('word')
    if word:
        word = word.lower()
    else:
        return redirect("/")
    jobs = get_jobs(word)

    return render_template("report.html",job=word,resultsNumber=len(jobs))

app.run(host="127.0.0.1")