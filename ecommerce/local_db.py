import pymysql


class Database:

    def __init__(self):
        host = 'us-cdbr-iron-east-05.cleardb.net'
        user = 'b5de033d9bb9f7'
        password = 'd746b139'
        db = 'heroku_7edc97b06ff109d'

        self.connect = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                cursorclass=pymysql.cursors.DictCursor)  

        self.cursor = self.connect.cursor()
