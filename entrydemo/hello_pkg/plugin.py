class BaseAuth:
    def authenticate(self, user, password):
        raise NotImplementedError


class SimpleAuth(BaseAuth):
    def authenticate(self, user, password):
        return user == "guest" and password == "123"


class AdminAuth(BaseAuth):
    def authenticate(self, user, password):
        return user == "admin" and password == "secret"