from ecommerce import mysql


class Category:
    '''Category object'''
    
    def __init__(self, name):
        self.name = name;

    def __repr__(self):
        return f('Category: {self.name}')
    
    def create(self):
        '''Create new Category object'''

        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO catagory (name) VALUES (%s)''', (self.name))
        mysql.connection.commit()


class Product:
    pass
