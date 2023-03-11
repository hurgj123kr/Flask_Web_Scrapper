import os
import pymysql
from dotenv import load_dotenv,find_dotenv
from flask import Flask,render_template, redirect, request, send_file
from flask.json import JSONEncoder
from scrapper import get_jobs 
from exporter import save_to_file as save_file

load_dotenv(find_dotenv())
conn = pymysql.connect(host='127.0.0.1', user='root', password=os.getenv('DB_PASSWORD'), db='FLASK_test', charset='utf8')
cursor = conn.cursor()
db = {}
application = Flask(__name__)

@application.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@application.route("/report", methods=["GET"])
def results():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_jobs(word)
            db[word] =jobs
            for job in jobs:
                    Title = (job['title']) 
                    Company = (job['company']) 
                    Location = (job['location'])
                    Link = (job['link'])
                    sql = """insert into jobs (Title, Company, Location, Link) values (%s, %s, %s, %s) """
                    cursor.execute(sql, (Title, Company, Location, Link ))              
    else:
        return redirect("/")
    conn.commit()
    conn.close()  
    return render_template("report.html",job=word,resultsNumber=len(jobs), jobs=jobs)

@application.route("/export", methods=["GET"])
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_file(jobs,word)
        return send_file(f"{word}.csv", mimetype="text/csv", as_attachment=True,attachment_filename=f"{word}.csv")
    except:
        return redirect('/')
        
if __name__ == '__main__':
    application.run(host="127.0.0.1")