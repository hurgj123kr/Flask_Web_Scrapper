import csv

def save_to_file(jobs,word):
    file = open(f"{word}.csv",mode="w") #파일 저장 및 이 파일은 쓰기만 가능
    writer = csv.writer(file) # csv파일 읽기
    writer.writerow(['Title','Company','Location','Link']) # writer 행에 들어갈 내용
    for job in jobs:
        writer.writerow(list(job.values())) #  첫 행 밑에 들어갈 내용.
    return 

