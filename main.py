from flask import Flask,render_template

app = Flask("Flask_Web_Scrapper")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


app.run(host="127.0.0.1")