#from ecommerce import mysql
from ecommerce import mysql

class Category:
    '''Category object'''
    
    def __init__(self, name):
        self.name = name

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
    
    def __init__(self, name, description, stock, price, available, category_id, store_id):
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price
        self.category_id = category_id
        self.available = available
        self.store_id = store_id
        #self.available = True

    def objects_all():
        mysql.reconnect()
        mysql.cursor.execute("SELECT * FROM product")
        result = mysql.cursor.fetchall()
        return result

    def create_object(self):
        mysql.reconnect()
        mysql.cursor.execute('''INSERT INTO product (name, description, stock, price, available, category_id, store_id) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )''', (self.name, self.description, self.stock, self.price, self.available, self.category_id, self.store_id))
        mysql.connect.commit()

class Basket:
    def __init__(self, name, description, stock, price, category_id,quantity):
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price
        self.category_id = category_id
        self.quantity=quantity
        #self.available = True

    def objects_all():
        mysql.reconnect()
        mysql.cursor.execute("update order_item as o inner join product as p on o.product_id=p.product_id set o.total_price = p.price * o.quantity")
        mysql.cursor.execute("SELECT * FROM basket join order_item join product where basket.order_item_id=order_item.order_item_id and order_item.product_id=product.product_id")
        result = mysql.cursor.fetchall()
        return result

class Total:
    def __init__(self, total):
        self.total= total

    def total_price():
        mysql.reconnect()
        mysql.cursor.execute("SELECT sum(total_price) as total from basket join order_item on basket.order_item_id=order_item.order_item_id")
        result=mysql.cursor.fetchall()
        return result

class Payment:
    def __init__(self,name):
        self.name=name

    def payment_method():
        mysql.reconnect()
        mysql.cursor.execute("SELECT * from payment_method")
        result=mysql.cursor.fetchall()
        return result
