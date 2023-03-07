from flask import Flask,render_template, redirect, request, send_file
from scrapper import get_jobs 
from exporter import save_to_file as save_file

applcation = Flask(__name__)

fake_db = {}

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/report", methods=["GET"])
def results():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existing_jobs = fake_db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_jobs(word)
            fake_db[word] =jobs
    else:
        return redirect("/")
    return render_template("report.html",job=word,resultsNumber=len(jobs), jobs=jobs)

@app.route("/export", methods=["GET"])
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = fake_db.get(word)
        if not jobs:
            raise Exception()
        save_file(jobs,word)
        return send_file(f"{word}.csv", mimetype="text/csv", as_attachment=True,attachment_filename=f"{word}.csv")
    except:
        return redirect('/')
        
if __name__ == '__main__':
    applcation.run()