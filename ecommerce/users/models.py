# User model


class User:

    def __init__(self, email, firstname, password, address, avatar):
        self.email = email
        self.firstname = firstname
        self.password = password
        self.address = address
        self.avatar = avatar

        def __repr__(self):
            '''String representation of the User object'''
            return "<User: {}>".format(self.email)
