import os
import pymysql
from dotenv import load_dotenv,find_dotenv
from flask import Flask,render_template, redirect, request, send_file, send_from_directory
from s3_con import s3_connection, s3_put_object
from scrapper import get_jobs 
from exporter import save_to_file as save_file

load_dotenv(find_dotenv())
conn = pymysql.connect(host=os.getenv('DB_HOST'), user='admin', password=os.getenv('DB_PASSWORD'), db='sys', charset='utf8')
cursor = conn.cursor()
db = {}
application = Flask(__name__)

s3 = s3_connection()

@application.route('/fileUpload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save("./temp")
    
    ret = s3_put_object(s3, os.getenv("AWS_S3_BUCKET_NAME"), "./temp", ".temp")
    if ret :
        print("파일 저장 성공")
    else:
        print("파일 저장 실패")


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