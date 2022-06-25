from flask import Flask,render_template, redirect, requests

app = Flask("Flask_Web_Scrapper")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/report", methods=["GET"])
def results():
    word = requests.args.get('word')
    if word:
        word = word.lower()
    else:
        return redirect("home.html")
    return render_template("report.html",job=word)

app.run(host="127.0.0.1")