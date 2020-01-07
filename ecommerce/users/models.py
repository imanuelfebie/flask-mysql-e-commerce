from ecommerce import mysql


class Admin:

    def __init__(self):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'{self.username}'
    
    def get_object(self):
        mysql.reconnect()
        mysql.cursor.execute("SELECT * FROM admin WHERE id = 1")
        return mysql.cursor.fetchall()

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
        mysql.reconnect()
        mysql.cursor.execute('''INSERT INTO user (email, firstname, lastname, password) VALUES (
            %s, %s, %s, %s
        )''', (self.email, self.firstname, self.lastname, self.password))
        mysql.connect.commit()

    @classmethod
    def get(cls, id):
        '''Retrieve the user object by id'''
        mysql.reconnect()
        mysql.cursor.execute("SELECT * FROM user WHERE user_id = {}".format(int(id)))
        return mysql.cursor.fetchone()

    @staticmethod
    def filter_by(email):
        mysql.reconnect()
        user = mysql.cursor.execute('''SELECT * FROM user WHERE email LIKE (%s)''', (email))
        return user
