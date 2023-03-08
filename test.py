import os

print(os.getcwd())
os.chdir("/Flask_Web_Scrapper")
print(os.getcwd())
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
    except PermissionError:
        pass

# search("Flask_Web_Scrapper")
#import os
#import scipy.io
#import csv
#import pymysql
#
## 로컬 mysql과 커넥션 수행
#conn = pymysql.connect(host='127.0.0.1', user='root', password='153123gj@#', db='FLASK_test', charset='utf8')
#curs = conn.cursor()
#conn.commit()
#
## CSV 파일 경로...
#f = open(r'/Users/sunghoheo/Flask_Web_Scrapper/static/csv/java.csv')
#csvReader = csv.reader(f)
#
## 컬럼 매핑
#for row in csvReader:
#    Title = (row[0])
#    Company = (row[1])
#    Location = (row[2])
#    Link = (row[3])
#    print(Title)
#    print(Company)
#    print(Location)
#    print(Link)
#    sql = """insert into jobs (Title, Company, Location, Link) values (%s, %s, %s, %s) """
#    curs.execute(sql, (Title, Company, Location, Link ))
#
## DB의 변화 저장
#conn.commit()
#f.close()
#conn.close()