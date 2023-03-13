import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())

class Config(object):

    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_DB = 'sys'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    ACL = 'public-read'