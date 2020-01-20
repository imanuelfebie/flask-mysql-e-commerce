from flask import session


class LoginManager:

    def __init__(self, is_authenticated, user):
        self.is_authentication = session['is_authenticated']
        self.user = session['user'] 
