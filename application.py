import os
import mysql.connector
from dotenv import load_dotenv,find_dotenv
from flask import Flask,render_template, redirect, request, send_file, send_from_directory
from scrapper import get_jobs 
from exporter import save_to_file as save_file
from flask import Flask

load_dotenv(find_dotenv())
application = Flask(__name__)
application.config['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
application.config['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
application.config['AWS_S3_BUCKET_NAME'] = 'search-jobs'
application.config.from_object('config.Config')

conn = mysql.connector.connect(
    host=application.config['MYSQL_HOST'],
    database=application.config['MYSQL_DB'],
    user=application.config['MYSQL_USER'],
    password=application.config['MYSQL_PASSWORD']
)
cursor = conn.cursor()
db = {}


@application.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@application.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')    

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
    application.debug = True
    application.run()