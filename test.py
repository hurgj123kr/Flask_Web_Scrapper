import os
import scipy.io
import csv
import pymysql
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
conn = pymysql.connect(host='127.0.0.1', user='root', password=os.getenv('DB_PASSWORD'), db='FLASK_test', charset='utf8')
cursor = conn.cursor()
query = "SELECT Title,Company,Location,Link FROM jobs"
cursor.execute(query)
result_db = cursor.fetchall()
db = {}
#for i in range(1,len(result_db)):
#   db[i] = result_db[i]
#   print(db[i][3])
file_link = os.getenv("CSV_LINK")
def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for f in filenames:
            full_filename = os.path.join(dirname, f)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:            
                out = os.path.splitext(full_filename)[-1]
                if out == '.csv':
                    print(full_filename)
                    return full_filename
    except PermissionError:
        pass



# 로컬 mysql과 커넥션 수행
# conn = pymysql.connect(host='127.0.0.1', user='root', password=os.getenv('DB_PASSWORD'), db='FLASK_test', charset='utf8')
# cursor = conn.cursor()
# query = "SELECT Title,Company,Location,Link FROM jobs"
# cursor.execute(query)
# result = cursor.fetchall()
# print(result)



# cursor.execute(query)
# query = "SELECT Title,Company,Location,Link FROM jobs"
#csv 데이터 저장 할떄
# if len(result) != 0:
#    print(f"{result}:데이터 존재")
#    conn.close()
# else:
#    print(f"{result}:데이터 존재 안해")
#    csv 경로
# f = open(search(file_link))
# csvReader = csv.reader(f)
# print(csvReader)
#    컬럼 맵핑
#    for row in csvReader:
    #    Title = (row[0]) 
    #    Company = (row[1])
    #    Location = (row[2])
    #    Link = (row[3])
    #    sql = """insert into jobs (Title, Company, Location, Link) values (%s, %s, %s, %s) """
    #    cursor.execute(sql, (Title, Company, Location, Link ))
#    Db 변화된것 저장
#    conn.commit()
#    f.close()
#    conn.close()

