from dotenv import load_dotenv
import pymysql
import os


load_dotenv()

class Database:

    def __init__(self):
        host = os.getenv('CLEARDB_DATABASE_URL')
        user = os.getenv('CLEARDB_USERNAME')
        password = os.getenv('CLEARDB_PASSWORD')
        db = os.getenv('CLEARDB_DATABASE')

        self.connect = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                cursorclass=pymysql.cursors.DictCursor)  

        self.cursor = self.connect.cursor()

    def reconnect(self):
    	self.connect.ping(reconnect=True)

