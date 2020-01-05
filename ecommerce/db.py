import pymysql


class Database:

    def __init__(self):
        host = 'localhost'
        user = 'batman'
        password = 'password'
        db = 'ecommerce_db'

        self.connect = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db)

        self.cursor = self.connect.cursor()
