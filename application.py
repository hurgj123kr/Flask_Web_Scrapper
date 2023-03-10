import os
from flask import Flask,render_template, redirect, request, send_file
from flask.json import JSONEncoder
from scrapper import get_jobs 
from exporter import save_to_file as save_file



result_db = {}

application = Flask(__name__)

@application.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@application.route("/report", methods=["GET"])
def results():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existing_jobs = result_db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_jobs(word)
            result_db[word] =jobs
    else:
        return redirect("/")
    return render_template("report.html",job=word,resultsNumber=len(jobs), jobs=jobs)

@application.route("/export", methods=["GET"])
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = result_db.get(word)
        if not jobs:
            raise Exception()
        save_file(jobs,word)
        return send_file(f"{word}.csv", mimetype="text/csv", as_attachment=True,attachment_filename=f"{word}.csv")
    except:
        return redirect('/')
        
if __name__ == '__main__':
    application.run(host="127.0.0.1")