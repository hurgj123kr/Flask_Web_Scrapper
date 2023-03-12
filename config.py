import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())

class Config(object):

    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_DB = 'sys'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    ACL = 'public-read'
    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
    AWS_S3_BUCKET_REGION = os.getenv('AWS_S3_BUCKET_REGION') 
    USE_S3 =True