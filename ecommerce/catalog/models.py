#from ecommerce import mysql
from ecommerce import db


class Category:
    '''Category object'''
    
    def __init__(self, name):
        self.name = name;

    def __repr__(self):
        return f('Category: {self.name}')
    
    def create(self):
        '''Create new Category object'''
        

        #cur = mysql.connection.cursor()
        #cur.execute('''INSERT INTO category (name) VALUES (%s)''', (self.name))
        #mysql.connection.commit()
        #cur.close()
        pass

    def get_all():
        #cur = mysql.connection.cursor()
        #cur.execute("SELECT * FROM category")
        #object_list = cur.fetchall()

        #return str(object_list)
        pass



class Product:
    pass
