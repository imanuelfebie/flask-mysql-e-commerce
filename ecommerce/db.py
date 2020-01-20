from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

class Database:
    
    # establish connection to remote db
    connection = pymysql.connect(
            host=os.getenv('CLEARDB_DATABASE_URL'),
            user=os.getenv('CLEARDB_USERNAME'),
            password=os.getenv('CLEARDB_PASSWORD'),
            db=os.getenv('CLEARDB_DATABASE'),
            cursorclass=pymysql.cursors.DictCursor
            )

    @classmethod
    def reconnect(cls):
        '''Check's if there is a connection, if not it will reconnect to the database'''
        return Database.connection.ping(reconnect=True)
