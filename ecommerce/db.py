from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

class Database:

    def __init__(self):
        host = os.environ.get('CLEARDB_DATABASE_URL')
        #user = os.getenv('DB_USER')
        #password = os.getenv('DB_PASSWORD')
        #db = os.getenv('DB_DATABASE')

        self.connect = pymysql.connect(
                host=host,
                cursorclass=pymysql.cursors.DictCursor)  

        self.cursor = self.connect.cursor()

  
