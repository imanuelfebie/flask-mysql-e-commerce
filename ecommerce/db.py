from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

class Database:

    def __init__(self):
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')

        self.connect = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                cursorclass=pymysql.cursors.DictCursor)  

        self.cursor = self.connect.cursor()

  
