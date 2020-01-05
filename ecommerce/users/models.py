#from ecommerce import mysql

class User:
    '''User model that represents the User table of the database'''


    def __init__(self, email, firstname, lastname, password):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

    def __repr__(self):
            '''String representation of the User object'''
            return "<User: {}>".format(self.email)

    def create_object(self):
       # cur = mysql.connection.cursor()
       # cur.execute('''INSERT INTO user (email, firstname, lastname, password) VALUES (%s, %s, %s, %s)''', (self.email, self.firstname, self.lastname, self.password))

       # mysql.connection.commit()
       pass
