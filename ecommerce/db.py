from dotenv import load_dotenv
import pymysql
import os


load_dotenv()

class Database:

    def __init__(self):
        # Database credentials
        self.host = os.getenv('CLEARDB_DATABASE_URL')
        self.user = os.getenv('CLEARDB_USERNAME')
        self.password = os.getenv('CLEARDB_PASSWORD')
        self.db = os.getenv('CLEARDB_DATABASE')

    def connect(self):
        # connect to the database, also reconnects to prevent "OperationalErrors" during runtime
        connect = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                cursorclass=pymysql.cursors.DictCursor)  
        connect.ping(reconnect=True)
        return connect

        #self.cursor = self.connect.cursor()

    #def reconnect(self):
    #	self.connect.ping(reconnect=True)

