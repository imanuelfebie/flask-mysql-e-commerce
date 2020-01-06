#from ecommerce import mysql
from ecommerce import mysql



class Category:
    '''Category object'''
    
    def __init__(self, name):
        self.name = name;

    def __repr__(self):
        return f('Category: {self.name}')
    
    def create(self):
        '''Create new Category object'''
        #sql = 'INSERT INTO category (name) VALUES {}'.format(self.name)
        mysql.reconnect()
        mysql.cursor.execute("INSERT INTO category (name) VALUES (%s)", (self.name))
        mysql.connect.commit()


    def objects_all():
        mysql.reconnect()
        mysql.cursor.execute("SELECT * FROM category")
        results = mysql.cursor.fetchall()
        return results

        
class Product:
    
    def __init__(self, name, description, stock, price, category_id):
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price
        self.category_id = category_id
        #self.available = True

    def objects_all():
        mysql.reconnect()
        mysql.cursor.execute("SELECT * FROM product")
        result = mysql.cursor.fetchall()
        return result
