from ecommerce import mysql

class Object:

    def __init__(self, table_name):
        self.table_name = table_name
    
    def create(self, *args, **kwargs):
        '''INSERT INTO table name'''
        #mysql.cursor.execute("INSERT INTO {} ({}) VALUES ({})".)
        pass

    def all(self):
        '''SELECT * FROM [table]'''
        mysql.cursor.execute("SELECT * FROM {}".format(self.table_name))
        return mysql.cursor.fetchall()


